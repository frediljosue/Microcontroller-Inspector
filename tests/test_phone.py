"""Phone layout, and the phone-as-wireless-camera link over a QR code."""
import base64
import json
import struct

from conftest import APP, CORS, inspection, gemini_body, new_page, open_app, serve_libs, start_camera, text

DANGER = inspection("danger", "LED has no resistor.", issues=[
    {"severity": "critical", "title": "LED without resistor", "where": "row 12", "fix": "add 220 Ω", "box": [0.3, 0.3, 0.5, 0.5]}],
    parts=[{"name": "blue module", "confidence": 0.3, "alternatives": ["DHT11"], "box": [0.6, 0.6, 0.8, 0.8]}])


def jpeg_size(b64):
    d, i = base64.b64decode(b64), 2
    while i < len(d):
        marker, length = d[i + 1], struct.unpack(">H", d[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC2):
            h, w = struct.unpack(">HH", d[i + 5:i + 9])
            return w, h
        i += 2 + length


def test_phone_layout_fits_the_screen(browser, devices):
    page = new_page(browser, **devices["Pixel 7"])
    open_app(page)
    start_camera(page)
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "no sideways scrolling"
    assert page.evaluate("getComputedStyle(document.querySelector('.stage')).position") == "sticky"
    assert page.errors == []


def test_phone_camera_end_to_end(browser, devices, peer_server):
    phone_html = (APP.replace("file://", ""))
    sent_images = []

    def ai(route):
        sent_images.append(json.loads(route.request.post_data)["contents"][0]["parts"][0]["inline_data"]["data"])
        route.fulfill(status=200, headers=CORS, content_type="application/json", body=json.dumps(gemini_body(DANGER)))

    # laptop
    laptop = new_page(browser)
    serve_libs(laptop)
    laptop.route("https://generativelanguage.googleapis.com/**", ai)
    open_app(laptop, query=peer_server)
    laptop.click("#phoneBtn")
    laptop.wait_for_function("peer && peer.open", timeout=5000)
    assert laptop.is_visible("#needUrl"), "a local file must ask where the online copy lives"
    # Phones need a secure page; http://localhost counts as secure, so the test serves the phone page there.
    laptop.evaluate("LS.set('onlineUrl', 'http://localhost:8765/index.html'); $('needUrl').style.display = 'none'; showQR(peer.id)")
    link = laptop.evaluate("$('qrLink').textContent")
    assert "?cam=wil-" in link and laptop.evaluate("!!document.querySelector('#qr svg')")

    # phone
    phone = new_page(browser, **devices["iPhone 13"])
    serve_libs(phone)
    phone.route("http://localhost:8765/**", lambda r: r.fulfill(status=200, content_type="text/html", body=open(phone_html).read()))
    phone.goto(link)
    assert phone.evaluate("document.body.classList.contains('phone-mode')")
    phone.tap("#pStart")
    phone.wait_for_function("$('pPill').textContent.includes('Connected')", timeout=10000)
    laptop.wait_for_function("phoneSource && video.videoWidth > 0", timeout=10000)
    assert laptop.is_hidden("#phoneModal")

    # a check uses the phone's full-resolution still, and the verdict goes back to the phone
    laptop.click("#nowBtn")
    laptop.wait_for_function("history.length === 1", timeout=10000)
    w, h = jpeg_size(sent_images[0])
    assert max(w, h) == 1600, f"expected the phone's 1600px still, got {w}x{h}"
    phone.wait_for_function("$('pVerdict').style.display === 'block'")
    banner = text(phone, "#pVerdict")
    assert "Do NOT power on" in banner and "LED without resistor" in banner and "1 part to confirm" in banner

    # stopping on the phone is noticed by the laptop
    phone.tap("#pStop")
    laptop.wait_for_function("!phoneSource", timeout=5000)
    assert "phone disconnected" in text(laptop, "#errBox")
    assert laptop.errors == [] and phone.errors == []
