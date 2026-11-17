# AI services

Pick one in **Service** at the top of the left panel. Every service gets the same photo and the same instructions, and returns the same kind of answer. They differ in cost, speed and how well they read small details.

| Service | Cost | Key | Speed | Reads small labels | Your photos go to |
|---|---|---|---|---|---|
| **Google Gemini** | Free tier with daily limits | Yes, free | 2–8 s | Good | Google |
| **Groq** | Free tier with daily limits | Yes, free | 1–3 s | OK | Groq |
| **Ollama** | Free, unlimited | No | 10–60 s+ | Weakest | **Nowhere**, it runs on your laptop |
| **OpenRouter / OpenAI-compatible** | Many `:free` models | Yes | Varies | Varies | That service |
| **Anthropic Claude** | Paid credits | Yes | 3–10 s | Best | Anthropic |

> Speeds are rough estimates and depend on the model, your connection and how busy the service is.

> **Model names change often.** Press **List** next to **Model** to see what your key can use right now.

---

## Google Gemini · recommended free option

1. Go to **[aistudio.google.com](https://aistudio.google.com)** and sign in.
2. Click **Get API key → Create API key** and copy it.
3. In the app, choose **Google Gemini** and paste the key.

**Limits.** The free tier has per-minute and per-day request limits. Set **Check at most every** to 10 s for long sessions.

**Automatic fallbacks.** If a model has no free quota, has used up today's limit, or is overloaded, the app **switches to the next model by itself** and tries again: `gemini-3.8-flash` → `gemini-3.6-flash` → `gemini-3.5-flash-lite`. If every model is busy, it waits and tells you why.

**Privacy.** Google may use content sent on the **free tier** to improve its products. Don't point the camera at anything private.

## Groq · fastest free option

1. Go to **[console.groq.com](https://console.groq.com)** and sign up.
2. Open **API Keys → Create API Key** and copy it. It starts with `gsk_`.
3. Choose **Groq** in the app and paste it. Press **List** and pick a model that supports images.

Groq is very fast but reads fine breadboard details less reliably than Gemini.

## Ollama · free, offline, private

Runs a vision model on your own laptop. No key, no limits, and nothing leaves your computer. It needs a reasonably strong laptop: 8–16 GB RAM, and a graphics card makes it much faster.

1. Install from **[ollama.com](https://ollama.com)**.
2. Download a vision model in a terminal:
   ```bash
   ollama pull qwen3-vl:8b      # better
   ollama pull gemma3:4b        # lighter, for weaker laptops
   ```
3. **Allow the app to talk to Ollama.** Browsers block this by default.
   - **Windows:** run `setx OLLAMA_ORIGINS "*"` in a terminal, then **quit Ollama from the system tray and open it again**.
   - **macOS:** run `launchctl setenv OLLAMA_ORIGINS "*"`, then restart Ollama.
   - **Linux:** add `Environment="OLLAMA_ORIGINS=*"` to the Ollama service, then restart it.
4. In the app choose **Ollama**, press **List**, and pick your model.

> ⚠️ `OLLAMA_ORIGINS="*"` lets any web page you open talk to your local Ollama. On a shared computer, set it to the exact site instead, for example `https://frediljosue.github.io`.

## OpenRouter or another OpenAI-compatible service

1. Get a key at **[openrouter.ai/keys](https://openrouter.ai/keys)**.
2. Choose **Other OpenAI-compatible**. The address is already set to OpenRouter.
3. Press **List**. Image-capable models are shown, with `:free` ones first.

Any service that speaks the OpenAI chat-completions format with image input works. Change **Server address** to point at it.

## Anthropic Claude · most accurate, paid

1. Go to **[platform.claude.com](https://platform.claude.com)**, add prepaid credits, and create an API key. It starts with `sk-ant-`.
2. Choose **Anthropic Claude** and paste it.

This is separate from a claude.ai chat subscription, so API use is billed on its own. The token counter at the bottom right shows how much each session uses.

---

## Keeping your key safe

- The key lives only in the box on the page, and in your browser's storage if you tick **Remember**.
- It is sent only to the service you picked, never to this repo or anyone else.
- Never commit a key to GitHub or share a screenshot that shows it. If one leaks, delete it in that service's dashboard and make a new one.

Next: [Troubleshooting →](troubleshooting.md)
