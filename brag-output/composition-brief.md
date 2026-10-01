# Hyperframes Composition Brief: AgriSense AI

## Objective

Create a polished LinkedIn showcase using the actual running AgriSense AI interface and genuine predictions returned by its local FastAPI model service.

## Output

- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/agrisense-ai-linkedin.mp4`
- Poster frame: `brag-output/agrisense-ai-linkedin.jpg`
- Format: vertical 4:5, 1080 × 1350
- Duration: 35 seconds, 30 fps
- Encoding: MP4 / H.264 with fast-start metadata, stereo AAC if audio is included
- No GitHub URL.

## Source material

- Project root: `Smart-Agriculture-MLOps`
- Primary files read: `README.md`, `frontend/src/AgriSenseApp.jsx`, `frontend/src/styles.css`, `frontend/src/workbench.css`, `backend/app/main.py`, and `backend/app/api/routes/weather.py`.
- Actual UI captures: `assets/real-ui/01-dashboard.png` through `07-yield.png`.
- Product name: AgriSense AI.
- Subtitle: Smart Agriculture Decision Platform.
- The UI uses deep teal (`#193f43`), teal (`#2a5958`), lime (`#a8d879`), warm gray-green (`#f3f5f2`), and muted orange (`#e3a36f`).
- Display/body type should use system sans-serif fallbacks consistent with the app's Manrope and DM Sans styling.

## Grounding constraints

- Use the real captures as-is; do not recreate or simulate application screens.
- Prediction text is already present in each captured UI: Rice, MOP, Low, ₹2,334.68, and 1.15 t/ha.
- The Weather capture shows the real unavailable state because the weather provider is not configured. Do not add temperature, forecast, or other weather values.
- The technology names React, FastAPI, Python, and Machine Learning are supported by the real project.
- Do not show the account badge, unprovided repository URL, fabricated metrics, or unsupported feature claims.

## Storyboard

Use the timing and scene order in `brag-plan.md`. Keep each real UI screenshot full-frame at the 4:5 canvas aspect ratio; use gentle, seek-safe scale motion and restrained cuts. Opening and end card use the app's palette and the exact requested title/subtitle. Technology card is typography-only.

## Audio

- Music: bundled `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` by Sascha Ende.
- Attribution: “Happy Beats & Business Moves Vol. 1 by Sascha Ende — ende.app — CC BY 4.0.”
- Level: restrained instrumental bed, with a short fade-in and a fade through the final card.
- No voiceover. Avoid UI click sounds that could suggest interactions not shown.

## LinkedIn framing

Use 4:5 vertical framing, H.264 MP4, 30 fps, with titles and key content clear of the outer edges. LinkedIn's current help allows this aspect ratio, MP4, and 10–60 fps for uploaded videos. [LinkedIn video upload requirements](https://www.linkedin.com/help/linkedin/answer/a7174587)
