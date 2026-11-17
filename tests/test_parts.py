"""Automatic part detection and the confirm / correct question cards."""
from conftest import inspection, mock_gemini, gemini_body, open_app, start_camera

FIRST = [
    {"name": "Arduino Uno R3", "type": "board", "confidence": 0.97, "box": [0.05, 0.1, 0.4, 0.8]},
    {"name": "HC-SR04 ultrasonic sensor", "confidence": 0.62, "clue": "two silver transducers",
     "alternatives": ["RCWL-1601 ultrasonic sensor"], "box": [0.5, 0.15, 0.75, 0.35]},
    {"name": "220 Ω resistor", "confidence": 0.45, "alternatives": ["330 Ω resistor", "1 kΩ resistor"], "box": [0.55, 0.5, 0.62, 0.56]},
    {"name": "blue module", "confidence": 0.3, "box": [0.7, 0.6, 0.9, 0.85]},
    {"name": "white connector", "confidence": 0.4, "box": [0.42, 0.85, 0.5, 0.95]},
]
# The AI keeps using its *old* names on the second look; the app must still match them.
SECOND = [{"name": p["name"], "confidence": p["confidence"] + 0.05, "box": p["box"]} for p in FIRST[:4]]

CHIPS = "[...document.querySelectorAll('.chip')].map(e => e.textContent.replace(/\\s+/g, ' ').trim())"
QUESTIONS = "[...document.querySelectorAll('.pq .q')].map(e => e.textContent.trim())"


def card(name):
    return f".pq:has-text('{name}')"


def test_detect_confirm_correct_and_remember(page):
    calls = mock_gemini(page, lambda m, b, n: (200, gemini_body(inspection(parts=FIRST if n == 1 else SECOND))))
    open_app(page)
    start_camera(page)

    page.click("#nowBtn")
    page.wait_for_function("history.length === 1")
    assert len(page.evaluate(QUESTIONS)) == 4, "everything under 75% sure gets a question card"
    assert page.evaluate(CHIPS) == ["P1Arduino Uno R3 97%"]

    page.click(card("HC-SR04") + " button[data-a=yes]")
    page.click(card("220") + " button[data-v='330 Ω resistor']")
    page.click(card("blue module") + " button[data-a=other]")
    page.fill(card("blue module") + " input", "DHT11 temperature sensor")
    page.press(card("blue module") + " input", "Enter")
    page.click(card("white connector") + " button[data-a=ignore]")

    page.click("#nowBtn")
    page.wait_for_function("history.length === 2")
    prompt = calls[1]["body"]["contents"][0]["parts"][1]["text"]
    assert "PARTS CONFIRMED BY THE USER" in prompt and "DHT11 temperature sensor" in prompt
    assert 'you previously called it "blue module"' in prompt
    assert "IGNORE: white connector" in prompt

    assert page.evaluate(QUESTIONS) == [], "answered parts must not be asked again"
    chips = page.evaluate(CHIPS)
    assert "P4DHT11 temperature sensor ✓ you" in chips and "P3330 Ω resistor ✓ you" in chips

    page.reload()
    page.wait_for_timeout(300)
    assert page.evaluate(CHIPS) == chips, "confirmed parts survive a reload"


def test_threshold_always_ask(page):
    mock_gemini(page, lambda *a: (200, gemini_body(inspection(parts=FIRST[:1]))))
    open_app(page)
    page.select_option("#askBelow", "1.01")
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_function("history.length === 1")
    assert len(page.evaluate(QUESTIONS)) == 1, "'Always ask' asks even at 97%"


def test_detection_off(page):
    calls = mock_gemini(page, lambda *a: (200, gemini_body(inspection(parts=FIRST))))
    open_app(page)
    page.uncheck("#detect")
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_function("history.length === 1")
    assert "parts_detected" not in calls[0]["body"]["contents"][0]["parts"][1]["text"]
    assert page.evaluate(QUESTIONS) == []
