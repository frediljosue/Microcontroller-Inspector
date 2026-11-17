# Changelog

## 2026-11-16

### Added
- **Full project docs:** getting started, phone camera, AI services, troubleshooting, how it works.
- **Offline browser tests** for every feature, run by GitHub Actions on every push.
- Part labels on the video now move out of each other's way.

### Fixed
- Pressing **Check now** after a model was busy now retries automatically. Before, it only retried in live mode.
- Labels of nearby parts no longer cover each other.

## 2026-11-16 · earlier

### Added
- **Phone as a wireless camera** over a QR code, with a full-resolution still for each check, the verdict on the phone, Flip, Light and screen wake lock.
- **Phone layout:** the video stays pinned at the top.
- **Automatic part detection** with confirm / correct question cards, saved between visits.
- **Free AI services:** Gemini, Groq, Ollama and any OpenAI-compatible API, alongside Anthropic Claude.
- **Automatic model switching** when a model has no free quota, has used up today's limit, or is overloaded.
- Errors show **what the service said**.

### Fixed
- Hand-held phones never counted as "steady". Steadiness now adapts to the camera's normal jitter and never waits more than 6 s.
- The parts list and the "Extra parts info" box were saved under the same name and overwrote each other.

## First version
- Live webcam checks with verdicts, issue boxes, history, spoken warnings and a token counter.
