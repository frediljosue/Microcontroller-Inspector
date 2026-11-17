# Contributing

Thanks for helping! Robotics Club members and anyone else are welcome.

## The basics

- **The app is one file:** `index.html`. Edit it, refresh the browser, and that's it. No build step.
- **Keep it one file.** It needs to work when someone double-clicks a downloaded copy. Libraries are loaded from a CDN only when needed, like PeerJS and the QR code for the phone link.
- **Never commit an API key.** The tests use fake keys and mocked services.

## Workflow

1. Fork the repo, or make a branch if you're a collaborator.
2. Make your change in `index.html`.
3. Run the tests. They take about a minute and need no API key:
   ```bash
   cd tests
   npm install
   pip install -r requirements.txt
   python -m playwright install chromium
   python -m pytest -v
   ```
4. If you changed behaviour, **add a test** in `tests/`. If you fixed a bug, add a test that would have caught it.
5. Open a pull request describing what changed and how you tested it. GitHub runs the tests automatically.

## Good first contributions

| Idea | Where |
|---|---|
| Always confirm power parts like regulators, buck converters and batteries | `needsConfirmation()` |
| Add a board: Teensy 4.1, Arduino Nano ESP32, Pi Zero 2 W… | `BOARDS` |
| Show how long each check took | `runCheck()` and the meter at the bottom |
| Smarter behaviour after many daily-limit errors | `onRateLimit()` |
| Translate the interface into Spanish | All visible text |

See [docs/how-it-works.md](docs/how-it-works.md) for a tour of the code.

## Style

- Plain JavaScript, no frameworks.
- Clear, friendly messages. Say **what happened** and **what to do**, in plain words.
- Safety first. When the AI is unsure about anything that could damage hardware, the app should say so, not guess.
