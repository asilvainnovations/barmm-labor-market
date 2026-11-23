# BARMM Labour Market Readiness PWA

A mobile-first Progressive Web App for exploring the SIPP-aligned BARMM Labour Market Statistical Workbook.

## MTIT identity and circular logo

The application navigation now displays the official Ministry of Trade, Investments and Tourism (MTIT) logo in a circular frame. The circular SVG PWA icon also references the official asset supplied in the project repository:

`assets/MTIT-logo.webp` in `https://github.com/asilvainnovations/barmm-labor-market`

The 192px and 512px PNG fallbacks use a circular MTIT monogram treatment. The app header and SVG icon load the official WebP from the repository's raw asset URL; an internet connection is therefore required to retrieve the logo on a fresh install. The remaining application shell and workbook data are cached for offline use.

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
