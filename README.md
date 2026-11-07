# kids-display-feed

Tiny public feed for the kids' wall display (the Frameo frame running Kids Display).

The frame is an old Android device whose browser can't reach Google's servers, so
it can't read the Google Sheet directly. Instead:

1. **`Kids Display - Feed`** Google Sheet (in Drive, filled from Kids Pulse) is the
   source — only kid-safe events (games, special days, bring-$, dress-up days). No
   grades, lunch balances, or attendance.
2. The **nightly GitHub Action** (`.github/workflows/sync-feed.yml`) runs `sync.py`,
   which reads that sheet and writes **`feed.json`**.
3. The frame fetches `feed.json` from `raw.githubusercontent.com` — which it *can*
   reach — and shows the events.

To change what the kids see, edit the Google Sheet. The display updates within a day
(or run the Action manually from the Actions tab).
