# Calendar Splitter

Splits your U of A med school ICS feed into three separate calendars by title,
so each can be given its own color when subscribed to on iPhone/Apple Calendar:

- `output/mandatory.ics` — titles containing "C1"
- `output/self_directed.ics` — titles containing "[C3] SELF-DIRECTED LEARNING"
- `output/other.ics` — everything else

A GitHub Actions workflow re-fetches and re-splits the feed every hour and
commits the results back to this repo, so the three output files stay in
sync with the source automatically — no computer needs to stay on.

## Setup (one-time)

1. Create a new **public** GitHub repository (e.g. `med-calendar-split`).
2. Upload all the files in this folder to that repo, preserving the folder
   structure (`.github/workflows/split-calendar.yml`, `scripts/split_ics.py`,
   `requirements.txt`, `output/.gitkeep`).
3. In the repo, go to **Settings → Secrets and variables → Actions → New
   repository secret**:
   - Name: `ICS_SOURCE_URL`
   - Value: your private ICS URL (the one with your token in it — this stays
     secret and is never written into any file in the repo)
4. Go to the **Actions** tab and enable workflows if prompted. Then run the
   `Split calendar by category` workflow once manually (Actions tab → select
   the workflow → **Run workflow**) to generate the first set of output files.
5. Once it succeeds, your three calendar files will be available at:
   - `https://raw.githubusercontent.com/<your-username>/<repo-name>/main/output/mandatory.ics`
   - `https://raw.githubusercontent.com/<your-username>/<repo-name>/main/output/self_directed.ics`
   - `https://raw.githubusercontent.com/<your-username>/<repo-name>/main/output/other.ics`

## Subscribing on iPhone

For each of the 3 URLs above:

1. Settings → Calendar → Accounts → Add Account → Other → Add Subscribed
   Calendar.
2. Paste the URL.
3. After adding, go to Settings → Calendar → your new subscribed calendar →
   pick a color.

Repeat for all three. iOS will periodically refresh each one on its own
schedule (usually every few hours; not instant, but automatic).

## Notes

- The workflow runs hourly. If you need a fresher refresh, edit the cron
  schedule in `.github/workflows/split-calendar.yml`.
- If UAlberta's calendar server ever blocks requests from GitHub's servers,
  the workflow run will fail — check the Actions tab if the output files
  stop updating.
- Because the repo is public, event titles/times are technically visible to
  anyone who finds the repo (not indexed or listed anywhere though).
