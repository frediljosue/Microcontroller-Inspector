"""Shared helpers for the Wiring Inspector browser tests.

Everything runs offline:
  * the camera is Chrome's built-in fake camera (an animated test pattern),
  * every AI service is mocked with page.route(), so no API key is needed,
  * PeerJS and the QR library are served from tests/node_modules,
  * the phone-camera test talks to a local PeerJS server (tests/peer-server.js).
"""
import json
import os
import pathlib
import socket
import subprocess
import time

import pytest
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
APP = (ROOT / "index.html").as_uri()
NODE_MODULES = HERE / "node_modules"

CHROME_ARGS = [
    "--use-fake-device-for-media-stream",
    "--use-fake-ui-for-media-stream",
    # Let two pages in the same browser reach each other and the local test server.
    "--disable-features=WebRtcHideLocalIpsWithMdns,LocalNetworkAccessChecks,"
    "PrivateNetworkAccessRespectPreflightResults,PrivateNetworkAccessSendPreflights",
]
CORS = {"access-control-allow-origin": "*"}


# ── browser ──────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(pw):
    exe = os.environ.get("CHROME_PATH")  # optional: use an installed Chrome instead of Playwright's
    b = pw.chromium.launch(executable_path=exe or None, args=CHROME_ARGS)
    yield b
    b.close()


@pytest.fixture(scope="session")
def devices(pw):
    return pw.devices


def new_page(browser, **ctx):
    """A page with camera permission whose JavaScript errors are collected in page.errors."""
    context = browser.new_context(permissions=["camera"], **({"viewport": {"width": 1500, "height": 900}} | ctx))
    page = context.new_page()
    page.errors = []
    page.on("pageerror", lambda e: page.errors.append(str(e)))
    return page


@pytest.fixture
def page(browser):
    p = new_page(browser)
    yield p
    assert p.errors == [], f"JavaScript errors: {p.errors}"
    p.context.close()


# ── offline copies of the CDN libraries ──────────────────────────────────
def serve_libs(page):
    files = {
        "peerjs": NODE_MODULES / "peerjs/dist/peerjs.min.js",
        "qrcode-generator": NODE_MODULES / "qrcode-generator/qrcode.js",
    }

    def handler(route):
        for name, path in files.items():
            if name in route.request.url:
                return route.fulfill(status=200, content_type="application/javascript", body=path.read_text())
        route.abort()

    page.route("https://cdn.jsdelivr.net/**", handler)


# ── AI mocks ─────────────────────────────────────────────────────────────
def inspection(verdict="ok", summary="Looks fine.", issues=(), parts=(), **extra):
    """A result in the JSON shape the app asks the AI for."""
    return {"verdict": verdict, "summary": summary, "safe_to_power": verdict == "ok", "issues": list(issues),
            "changes": [], "looks_correct": [], "could_not_verify": [], "better_photo_tips": "",
            "parts_detected": list(parts), **extra}


def gemini_body(result):
    return {"candidates": [{"content": {"parts": [{"text": json.dumps(result)}]}}],
            "usageMetadata": {"promptTokenCount": 1000, "candidatesTokenCount": 250}}


def mock_gemini(page, respond):
    """respond(model, request_json, call_number) -> (status, body_dict). Returns the list of calls made."""
    calls = []

    def handler(route):
        url = route.request.url
        if "/models?" in url or url.rstrip("/").endswith("/models"):
            return route.fulfill(status=200, headers=CORS, content_type="application/json", body=json.dumps(
                {"models": [{"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["generateContent"]},
                            {"name": "models/gemini-3.1-flash-image", "supportedGenerationMethods": ["generateContent"]}]}))
        model = url.split("/models/")[1].split(":")[0]
        body = json.loads(route.request.post_data)
        calls.append({"model": model, "body": body})
        status, payload = respond(model, body, len(calls))
        route.fulfill(status=status, headers=CORS, content_type="application/json", body=json.dumps(payload))

    page.route("https://generativelanguage.googleapis.com/**", handler)
    return calls


def gemini_error(code, message, retry=None):
    err = {"error": {"code": code, "message": message, "status": "RESOURCE_EXHAUSTED" if code == 429 else "UNAVAILABLE"}}
    if retry:
        err["error"]["details"] = [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": f"{retry}s"}]
    return err


# ── app helpers ──────────────────────────────────────────────────────────
def open_app(page, query="", provider="gemini", key="AIzaTESTKEY0000000000", model=None):
    page.goto(APP + query)
    page.wait_for_timeout(300)
    page.select_option("#provider", provider)
    if key and provider != "ollama":
        page.fill("#key", key)
        page.dispatch_event("#key", "input")
    if model:
        page.fill("#model", model)
        page.dispatch_event("#model", "input")


def start_camera(page):
    page.click("#camBtn")
    page.wait_for_function("video.videoWidth > 0", timeout=5000)


def text(page, selector):
    return page.evaluate(f"(document.querySelector({json.dumps(selector)}) || {{}}).innerText || ''")


# ── local PeerJS signalling server ───────────────────────────────────────
@pytest.fixture(scope="session")
def peer_server():
    if not (NODE_MODULES / "peer").exists():
        pytest.skip("run `npm install` in tests/ first")
    proc = subprocess.Popen(["node", str(HERE / "peer-server.js")], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", 9000), timeout=0.2).close()
            break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("PeerJS test server did not start")
    yield "?peerHost=127.0.0.1&peerPort=9000&peerPath=/myapp"
    proc.kill()
