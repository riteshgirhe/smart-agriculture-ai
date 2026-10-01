# AgriSense AI showcase plan

## Creative direction

Polished, quiet product film for LinkedIn. Let the real AgriSense AI screens carry the story, with restrained motion, clear scene labels where needed, and an optimistic instrumental bed. Use the React app's deep teal, cream, leaf green, and muted orange palette.

## Facts and capture notes

- AgriSense AI is an agriculture decision-support app with five prediction workflows and a weather panel.
- The actual React frontend was started from this project on `localhost:5174`; the unrelated process on port 5173 was not used.
- The local FastAPI service reported all five model artifacts available. The five model requests were submitted from the real UI using its own prefilled example rows.
- Captured outputs: crop recommendation **Rice**; fertilizer recommendation **MOP**; irrigation prediction **Low**; price prediction **₹2,334.68**; yield prediction **1.15 t/ha**. These are outputs from this local run, not general performance claims.
- The weather endpoint returned HTTP 503 because `OPENWEATHER_API_KEY` is not configured. Show the app's real weather-unavailable state; do not add weather readings or imply live weather was available.
- Remove the account badge from the capture to keep personal account details out of a public video. No application files are changed by this runtime-only capture adjustment.
- No GitHub URL is shown.

## Storyboard — 35 seconds, 4:5 vertical

| Time | Beat | Visual and on-screen copy |
| --- | --- | --- |
| 0–3s | Opening | Deep teal title card: “AgriSense AI” and “Smart Agriculture Decision Platform.” A subtle leaf-green line reveals the title. |
| 3–7s | Dashboard | Full-frame real dashboard capture; keep its actual health, model, weather, and workflow cards visible. |
| 7–10s | Weather | Real Weather page, including its current “Weather unavailable” configuration state. No fabricated readings. |
| 10–13s | Crop | Real Crop recommendation page after submission; model result shown: Rice. |
| 13–16s | Fertilizer | Real Fertilizer recommendation page after submission; model result shown: MOP. |
| 16–19s | Irrigation | Real Irrigation prediction page after submission; model result shown: Low. |
| 19–22s | Price | Real Price prediction page after submission; model result shown: ₹2,334.68. Keep its example inputs visible. |
| 22–25s | Yield | Real Yield prediction page after submission; model result shown: 1.15 t/ha. |
| 25–30s | Technology | Four clean type cards: React · FastAPI · Python · Machine Learning. These names are grounded in the project's source and README. |
| 30–35s | End card | “AgriSense AI” / “Smart Agriculture Decision Platform.” No repository URL. |

## Audio and delivery

Use the bundled instrumental “Happy Beats & Business Moves Vol. 1” at a low bed level, with a gentle fade under the end card. Credit Sascha Ende and the CC BY 4.0 source in the share copy. Do not use narration. Keep all important text inside LinkedIn's central safe area.

The requested feature list needs more time than brag's usual 15–25-second format. The user explicitly requested 30–45 seconds, so this cut uses 35 seconds to give every workflow a readable moment.
