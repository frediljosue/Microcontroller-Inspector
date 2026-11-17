"""Bugs found in real use, kept fixed: free-tier limits, overloaded models, shaky cameras, saved settings."""
from conftest import APP, inspection, gemini_body, gemini_error, mock_gemini, open_app, start_camera, text

OK = gemini_body(inspection(parts=[{"name": "ESP32 DevKit", "confidence": 0.93, "box": [0.4, 0.35, 0.7, 0.8]}]))
BUSY = gemini_error(503, "This model is currently experiencing high demand. Spikes in demand are usually temporary.")


def go_live(page, every="3"):
    page.evaluate(f"$('every').value = '{every}'")
    page.click("#liveBtn")


def test_hand_held_camera_still_triggers_checks(page):
    """Chrome's fake camera never stops moving, like a phone held in your hand."""
    calls = mock_gemini(page, lambda *a: (200, OK))
    open_app(page)
    start_camera(page)
    go_live(page)
    page.wait_for_timeout(8000)
    assert len(calls) >= 1, "live mode must not wait forever for a perfectly still picture"


def test_no_free_quota_switches_model(page):
    calls = mock_gemini(page, lambda m, b, n: (429, gemini_error(429, f"Quota exceeded, limit: 0, model: {m}", retry=31))
                        if m == "gemini-3.8-flash" else (200, OK))
    open_app(page, model="gemini-3.8-flash")
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_function("history.length === 1", timeout=8000)
    assert [c["model"] for c in calls][:2] == ["gemini-3.8-flash", "gemini-3.6-flash"]
    assert page.input_value("#model") == "gemini-3.6-flash"


def test_overloaded_model_switches(page):
    calls = mock_gemini(page, lambda m, b, n: (503, BUSY) if m == "gemini-3.8-flash" else (200, OK))
    open_app(page, model="gemini-3.8-flash")
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_function("history.length === 1", timeout=8000)
    assert calls[1]["model"] == "gemini-3.6-flash"
    assert "Looks good" in text(page, "#vt")


def test_all_models_overloaded_backs_off(page):
    calls = mock_gemini(page, lambda *a: (503, BUSY))
    open_app(page, model="gemini-3.8-flash")
    page.uncheck("#onlyChange")
    start_camera(page)
    go_live(page, "5")
    page.wait_for_timeout(9000)
    assert len(calls) == 3, "try each model once, then wait instead of hammering the service"
    err = text(page, "#errBox")
    assert "overloaded" in err and "Retrying in" in err


def test_error_shows_what_the_service_said(page):
    mock_gemini(page, lambda *a: (429, gemini_error(429, "Too many requests per minute")))
    open_app(page, model="my-own-model")  # not in the auto-switch list
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_selector("#errBox")
    assert "Too many requests per minute" in page.evaluate("$('errBox').textContent")


def test_old_storage_clash_is_cleaned_up(page):
    page.goto(APP)
    page.evaluate("""localStorage.setItem('wil.parts', '{"parts":[],"alias":[]}')""")
    page.reload()
    page.wait_for_timeout(300)
    assert page.input_value("#parts") == ""
