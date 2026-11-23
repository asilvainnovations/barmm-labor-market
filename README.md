# BARMM Labour Market Readiness

A mobile-first Progressive Web App for exploring the SIPP-aligned BARMM Labour Market Statistical Workbook.

## MTIT identity and circular logo

The application navigation, SVG icon, 192px PNG icon and 512px PNG icon all use the exact official MTIT seal image uploaded by the user. The source file is bundled locally at `assets/MTIT-logo.webp`; no external logo URL or substitute monogram is used. The logo is cached with the application shell for offline availability.

## Netlify deployment

This package includes `netlify.toml`. To deploy:

1. Extract the ZIP and upload the folder to a new Git repository, or connect the existing Git repository to Netlify.
2. In Netlify, choose **Add new site → Import an existing project** and select the repository.
3. Set **Base directory** to the repository root.
4. Leave **Build command** blank (no build step is required).
5. Set **Publish directory** to `.`.
6. Deploy the site. Netlify will serve the static PWA over HTTPS, enabling installation and service-worker features.

For a manual deploy, drag the extracted folder into Netlify's deploy area. Keep the relative folder structure unchanged.

## Run locally

Serve the repository root over HTTP:

```bash
python -m http.server 8080
```

Open `http://localhost:8080`. Service workers and installation features require localhost or HTTPS; opening `index.html` directly with `file://` is not supported.

## Included files

- `index.html` — dashboard and application interface
- `assets/workbook-data.json` — structured snapshot of the 13 workbook sheets
- `assets/mtit-icon.svg` — circular SVG icon using the official MTIT logo
- `assets/mtit-icon-192.png` and `assets/mtit-icon-512.png` — circular install icon fallbacks
- `manifest.webmanifest` — installable PWA metadata
- `sw.js` — application shell/data/icon cache
- `netlify.toml` — Netlify static deployment and cache headers
- `README.md` — deployment and application notes

## Data and storage model

Workbook data is a read-only JSON snapshot. The Investment & Workforce Project Register is stored locally in IndexedDB with a localStorage fallback. Records remain on the browser/device and are not synchronised across users. A shared multi-user database, authentication and role-based access require a separately configured backend.

## Analytical safeguards

- SIPP eligibility is not proof of a BARMM project, investment approval, financing, jobs or skills shortage.
- SIPP Workforce Map entries are indicative pathways inferred from activity descriptions; validate with project and employer evidence.
- Investment lead shares are not approved investments or confirmed job demand.
- Blank source values remain blank and must not be read as zero.
- GRDP 2024 shares and employment 2025 shares have different reference years and denominators; the comparison is descriptive, not a productivity ratio.
- TESDA's BARMM employment rate describes graduates in the labour force for the stated cohort, not all graduates or trainees.

## Source dataset

Generated from the user-supplied `BARMM_Labour_Market_Statistical_Workbook_SIPP_Aligned(1).xlsx`.
