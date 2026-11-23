# BARMM Labour Market Readiness PWA

A mobile-first Progressive Web App for exploring the attached BARMM Labour Market Statistical Workbook (SIPP-aligned edition).

## Included
- `index.html` — application interface, dashboard and client-side logic
- `assets/workbook-data.json` — structured snapshot of all workbook sheets and records
- `manifest.webmanifest` — installable PWA manifest
- `sw.js` — static asset service worker for offline application shell/data
- `assets/icon.svg`, `icon-192.png`, `icon-512.png` — app icons

## Run locally
The app fetches JSON and registers a service worker, so serve it over HTTP rather than opening `index.html` with `file://`.

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Deploy
Upload the full directory contents to an HTTPS-enabled static host (GitHub Pages, Netlify, Vercel static hosting, or cPanel public web folder). Keep the relative folder structure unchanged.

## Data and storage model
- Workbook data is a read-only JSON snapshot bundled with the PWA. It contains the 13 workbook tabs and retains original columns, values and nulls.
- The Investment & Workforce Project Register is user-entered and stored locally in IndexedDB, with a localStorage fallback. Records stay on the device/browser and are not synchronised across users.
- CSV export is available for the SIPP map, workbook datasets and local project register.
- Dashboard charts use Chart.js from jsDelivr CDN. The app shell and workbook JSON are cached for offline access after the first successful load. For fully offline chart rendering, vendor the Chart.js library locally and add it to `sw.js` precache list.

## Production deployment considerations
This is a deployable static PWA prototype with a local database, not yet a multi-user hosted production system. Before official multi-user use:
1. Connect a managed backend database (for example Supabase/PostgreSQL) and define the final schema, indexes and migrations.
2. Implement authentication, role-based access and organisation/project-level authorisation.
3. Add server-side input validation, audit trails, backup/restore and retention rules.
4. Establish consent, data classification, privacy notices and access controls for personal or commercially sensitive project data.
5. Add automated tests, error monitoring, security headers, dependency pinning and a controlled deployment pipeline.
6. Confirm the agency's data-sharing and publication protocol.

## Analytical safeguards
- SIPP eligibility is not proof of a BARMM project, investment approval, financing, jobs or skills shortage.
- SIPP Workforce Map entries are indicative pathways inferred from activity descriptions; validate with project and employer evidence.
- Investment lead shares are not approved investments or confirmed job demand.
- Blank source values remain blank and must not be read as zero.
- GRDP 2024 shares and employment 2025 shares have different reference years and denominators; the comparison is descriptive, not a productivity ratio.
- TESDA's BARMM employment rate describes graduates in the labour force for the stated cohort, not all graduates or trainees.

## Source
The application dataset was generated from the user-attached file:
`BARMM_Labour_Market_Statistical_Workbook_SIPP_Aligned(1).xlsx`
