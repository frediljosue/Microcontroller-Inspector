# Troubleshooting

When something fails, the red box in the right panel says what happened. Click **What the service said** under it to see the AI service's own message. Most answers are below.

## Camera

| Problem | Fix |
|---|---|
| Nothing happens on **Start camera**, or *permission blocked* | Click the camera icon at the right end of the address bar → **Always allow** → reload |
| No permission prompt on **Windows** | **Settings → Privacy & security → Camera**: turn on *Camera access* and *Let desktop apps access your camera* |
| *Couldn't open the camera* | Another app is using it. Close Zoom, Teams or the Camera app |
| Black picture | Check for a privacy shutter or a camera-off key, often an F-key with a camera icon |
| Wrong camera | Pick it in **Camera** under *Live settings* |

## Phone camera

| Problem | Fix |
|---|---|
| Phone says *Camera not available* | Open the **https://** link from the QR code, not a downloaded file. Use Chrome or Safari |
| Stuck on *Waiting for your phone to scan…* or *Connecting…* | Campus Wi-Fi often blocks device-to-device video. **Turn on your phone's hotspot** and connect the laptop to it |
| *Laptop page not found* on the phone | The laptop page was closed or reloaded. Click **📱 Use phone camera** again and rescan |
| *Add the online address to make the QR code* | You opened a downloaded file. Paste `https://frediljosue.github.io/Microcontroller-detector/`, or just open that link instead |
| Laptop shows *The phone disconnected* | The phone locked or the browser went to the background. Keep the page open on the phone |

## AI errors

| Message | What it means | Fix |
|---|---|---|
| *is overloaded right now. Switched to …* | That model is busy on the service's side | Nothing. The app already switched models |
| *The AI service is overloaded right now* | Every model in the list is busy | Wait a minute, or switch **Service** |
| *No free quota on …* or *Daily free limit reached* | That model's free requests are used up | The app switches automatically. If all are used, wait until tomorrow or use another service |
| *Too many requests per minute* | Checks are too frequent for the free tier | Set **Check at most every** to 10 s or 20 s |
| *The service rejected your API key* | Wrong or deleted key | Paste it again. Make sure you copied all of it |
| *Model "…" was not found* | Model names change | Press **List** and pick one |
| *Couldn't reach the service* | No internet, or a network filter | Check the connection. Some school networks block AI services |
| *Can't reach Ollama* | Ollama isn't running, or `OLLAMA_ORIGINS` isn't set | See the Ollama steps in [ai-services.md](ai-services.md) |

## Live mode

| Problem | Fix |
|---|---|
| Stays on `change seen · waiting for steady view` | Hold the camera still for a second. It never waits more than 6 s anyway |
| Stays on `watching · no change` | Nothing changed enough. Press **Check now** |
| Checks too often or too rarely | Change **Check at most every** |

## Results

| Problem | Fix |
|---|---|
| Wrong part name | Answer the question card, or click the part's chip and correct it |
| Keeps asking about parts it should know | Lower **Ask me to confirm…** to 60% |
| Never asks, but gets parts wrong | Raise it to 90% or **Always ask** |
| *Need a clearer view* | Follow the camera tip. Usually: mount higher, straight down, more light, plain background |
| Misses a mistake you can see | Write your **intended connections**. Checking against a plan is far more reliable |

## Still stuck?

[Open an issue](https://github.com/frediljosue/Microcontroller-detector/issues/new/choose) with a screenshot of the red error box and the **What the service said** text. **Hide your API key** in any screenshot.
