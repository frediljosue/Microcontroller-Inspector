# Microcontroller Detector · Live Wiring Inspector

A single-page web app that watches your breadboard through a camera and has an AI check the wiring before you power it on.

**Open it:** https://frediljosue.github.io/Microcontroller-detector/

## What it does
- **Live checks:** watches the camera and runs a check whenever the board changes and your hands are out of the way.
- **Verdicts:** OK / check before powering / **do NOT power on**, with numbered boxes drawn on the problems and a concrete fix for each.
- **Automatic part detection:** names the parts it sees and asks you to confirm when it isn't sure. Your answers are treated as fact on later checks.
- **Phone as a wireless camera:** click **📱 Use phone camera** on the laptop, scan the QR code, and the phone streams to the laptop over WebRTC. For each check, the phone also sends a full-resolution still.
- **Free AI options:** Google Gemini (free key), Groq (free key), Ollama (local, offline, no key), any OpenAI-compatible service, or Anthropic Claude (paid).

## Privacy
Everything runs in your browser. API keys are typed into your own browser and only sent to the AI service you choose. They are never in this repo. Phone video goes directly between your devices; PeerJS's public server only helps them find each other.

## Run it locally
Open `index.html` in Chrome or Edge on a laptop. Phones need the online (https) copy above.
