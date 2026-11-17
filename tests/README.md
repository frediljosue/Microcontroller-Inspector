# Tests

Browser tests for the Wiring Inspector, written with [Playwright](https://playwright.dev/python/) and pytest.
They run **fully offline**: no API key, no webcam, no phone needed.

| What's faked | How |
|---|---|
| Camera | Chrome's built-in fake camera, an animated pattern that never stops moving, like a hand-held phone |
| AI services | Every request to Gemini, Groq, Ollama, OpenRouter and Anthropic is answered by a mock |
| CDN libraries | PeerJS and the QR library are served from `tests/node_modules` |
| Phone ↔ laptop | A second browser page acts as the phone and connects through a local PeerJS server (`peer-server.js`) |

## Run them

```bash
cd tests
npm install                      # PeerJS, QR library, local signalling server
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v
```

To use your installed Chrome instead of Playwright's Chromium, set `CHROME_PATH`, for example `CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"`.

## What's covered

| File | Checks |
|---|---|
| `test_ai_services.py` | Each AI service gets the right request with an image, and its answer is shown. Model listing and the custom OpenAI-compatible option |
| `test_parts.py` | Detection, Yes / alternative / type-your-own / Not a part, names carried across checks, saved after reload, the "ask when less than" setting |
| `test_resilience.py` | Hand-held camera still triggers checks; no-quota and overloaded models switch automatically; all-busy backs off; real error text shown; old saved-settings clash cleaned up |
| `test_phone.py` | Phone layout fits the screen; QR → phone streams to the laptop → full-resolution still sent to the AI → verdict appears on the phone → disconnect noticed |

GitHub runs all of these on every push (see `.github/workflows/tests.yml`).
