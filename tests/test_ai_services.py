"""Every AI service sends the right request and its answer is shown."""
import json

import pytest

from conftest import CORS, inspection, mock_gemini, gemini_body, open_app, start_camera, text

RESULT = inspection("warning", "Servo + goes to 3.3V.", issues=[
    {"severity": "warning", "title": "Servo on 3.3V", "where": "red wire", "fix": "Move to 5V", "box": [0.6, 0.5, 0.8, 0.7]}])
J = json.dumps(RESULT)

SERVICES = {
    # provider: (url pattern, mocked reply, key, expected model)
    "gemini": ("https://generativelanguage.googleapis.com/**", gemini_body(RESULT), "AIzaTEST000000", "gemini-3.8-flash"),
    "groq": ("https://api.groq.com/**", {"choices": [{"message": {"content": "```json\n" + J + "\n```"}}],
                                         "usage": {"prompt_tokens": 800, "completion_tokens": 150}}, "gsk_TEST000000", "qwen/qwen3.8-27b"),
    "ollama": ("http://localhost:11434/**", {"message": {"content": J}, "prompt_eval_count": 700, "eval_count": 120}, None, "qwen3-vl:8b"),
    "anthropic": ("https://api.anthropic.com/**", {"content": [{"type": "text", "text": J}],
                                                   "usage": {"input_tokens": 1600, "output_tokens": 300}}, "sk-ant-TEST000000", "claude-haiku-5-5"),
}


@pytest.mark.parametrize("provider", SERVICES)
def test_service_round_trip(page, provider):
    pattern, reply, key, model = SERVICES[provider]
    seen = []

    def handler(route):
        seen.append(route.request)
        route.fulfill(status=200, headers=CORS, content_type="application/json", body=json.dumps(reply))

    page.route(pattern, handler)
    open_app(page, provider=provider, key=key)
    assert page.input_value("#model") == model
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_function("history.length === 1")

    assert "Check before powering" in text(page, "#vt")
    assert "Servo on 3.3V" in text(page, "#report")
    assert len(seen) == 1
    body = json.loads(seen[0].post_data)
    assert "/9j/" in json.dumps(body), "a JPEG image must be sent (base64 JPEGs start with /9j/)"
    if provider == "anthropic":
        assert seen[0].headers["anthropic-dangerous-direct-browser-access"] == "true"


def test_ollama_needs_no_key(page):
    open_app(page, provider="ollama", key=None)
    assert page.evaluate("$('keyRow').style.display") == "none"


def test_list_models_filters_gemini(page):
    mock_gemini(page, lambda *a: (200, {}))
    open_app(page)
    page.click("#loadModels")
    page.wait_for_function("$('modelNote').textContent.includes('found')")
    options = page.evaluate("[...$('modelList').options].map(o => o.value)")
    assert options == ["gemini-3.8-flash"], "image-generation models must be filtered out"


def test_openai_compatible_custom_service(page):
    page.route("https://openrouter.ai/**", lambda r: r.fulfill(status=200, headers=CORS, content_type="application/json",
                                                               body=json.dumps({"choices": [{"message": {"content": J}}]})))
    open_app(page, provider="custom", key="sk-or-TEST0000", model="qwen/qwen3-vl:free")
    start_camera(page)
    page.click("#nowBtn")
    page.wait_for_function("history.length === 1")
    assert "Check before powering" in text(page, "#vt")
