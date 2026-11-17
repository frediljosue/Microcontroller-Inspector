# Getting started

This guide takes you from nothing to a live check of your board in about five minutes.

**You need:** a laptop with Chrome or Edge, a camera that is either the laptop webcam, a USB webcam, or your phone, and a free AI key. Gemini is used below.

---

## Step 1 · Get a free Gemini API key

1. Go to **[aistudio.google.com](https://aistudio.google.com)** and sign in with a Google account.
2. Click **Get API key**, then **Create API key**.
3. Copy the key. It starts with `AIza`.

> 💡 Prefer something else? Groq is just as quick to set up, and Ollama needs no key at all. See [ai-services.md](ai-services.md).

## Step 2 · Open the app

Open **[frediljosue.github.io/Microcontroller-detector](https://frediljosue.github.io/Microcontroller-detector/)** in Chrome or Edge on your laptop.

You can also download `index.html` and double-click it. It works the same on a laptop, but the phone camera needs the online version.

## Step 3 · Fill in the left panel

### 1 · AI that looks at the camera
| Setting | What to do |
|---|---|
| **Service** | Leave it on **Google Gemini** |
| **API key** | Paste your key. Tick **Remember on this computer** only on your own laptop |
| **Model** | Leave the default. If it ever says a model isn't found, press **List** and pick one |

### 2 · What are you wiring?
| Setting | What to do |
|---|---|
| **Board** | Pick your microcontroller. This gives the AI the right voltages and pin rules |
| **Extra parts info** | Optional. Parts are detected automatically. Use this for things the camera can't see, like "the module under the servo is a DHT22" |
| **Connections you intend to make** | Optional but powerful. One per line, such as `Servo signal → D9`. The AI then checks your wiring **against your plan**, not just for general mistakes |

### 3 · Live settings
| Setting | Default | Meaning |
|---|---|---|
| **Check at most every** | 5–10 s | The shortest time between checks. Longer saves free-tier requests |
| **Only check when the board changes** | On | No change means no request |
| **Wait until my hands are out of the way** | On | Waits for a steady picture, but never more than 6 s |
| **Say danger warnings out loud** | Off | Speaks "Stop. Do not power on." |
| **Mark problems on the video** | On | Numbered boxes around issues |
| **Auto-detect parts** | On | Names every part it sees |
| **Label detected parts on the video** | On | P1, P2… labels on the video |
| **Ask me to confirm a part when the AI is less than** | 75% sure | When to show a question card |

## Step 4 · Start the camera

- **Laptop webcam:** click **Start camera** and allow camera access.
- **Phone:** click **📱 Use phone camera** and scan the QR code. See [phone-camera.md](phone-camera.md).

**Camera position matters more than anything else.** Mount it straight above the board, use bright light without glare, and put the board on a flat, plain surface. A soft blanket or a busy background makes pins hard to read.

## Step 5 · Go live

Press **Go live**. The status box at the top right of the video shows what's happening:

| Status | Meaning |
|---|---|
| `watching · no change` | Nothing changed since the last check, so nothing is sent |
| `change seen · waiting for steady view` | Hold still for a second |
| `Checking…` | The AI is looking now, usually 2–8 s with Gemini |
| `next check in 4 s` | Waiting out the "check at most every" time |

**Check now** always runs a check immediately.

## Step 6 · Read the results

**The banner over the video:**

| Banner | Meaning |
|---|---|
| 🟢 **Looks good** | Nothing dangerous found |
| 🟡 **Check before powering** | Something is wrong or doesn't match your plan |
| 🔴 **Do NOT power on** | Something could damage a part |
| 🔵 **Need a clearer view** | It couldn't see well enough. Follow the camera tip |

**The right panel:**
- **Parts in view.** Chips for identified parts, plus yellow **"Is this a …?"** cards for unsure ones.
  - **Yes** confirms its guess.
  - **Another name** picks one of its alternatives.
  - **Something else…** lets you type the real name.
  - **Not a part** hides it.
  - Click any chip later to change your answer. **Reset** clears all parts for a new project.
- **Latest check.** Each issue with *where* it is and the *fix*, plus what was verified and what couldn't be verified.
- **History.** Click a thumbnail to see an older check.

## Tips for good results

- Write your intended connections. A check against a plan is far more useful than a general look.
- Answer the part questions. One answer fixes the identification for the whole session.
- Keep wires short and spread out, so the camera can follow them.
- If a pin is hidden, the AI says *couldn't verify*. Move the camera rather than trusting a guess.
- Always finish with a multimeter continuity check before powering anything expensive.

Next: [Phone camera →](phone-camera.md)
