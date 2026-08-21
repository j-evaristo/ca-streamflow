# California USGS Streamflow Data & Explorer

**Evaristo Critical Zone Hydrology Lab · University of Georgia**

Complete daily discharge (streamflow) record for every USGS gaging station in
California, plus an interactive offline viewer.

**Source:** USGS National Water Information System (NWIS) daily-values web
service (`waterservices.usgs.gov/nwis/dv`), parameter code **00060**
(discharge, cubic feet per second).

## Contents

| Path | What it is |
|---|---|
| `ca_streamflow_explorer.html` | **Interactive viewer** — open directly in any browser (no server needed). Keep the `data/` folder next to it. |
| `data/csv/USGS_<site>.csv` | Daily values per station: `site_no, date, stat_cd, discharge_cfs, qualifiers, method_id, method_desc`. |
| `data/sites_metadata.csv` | One row per station: name, coordinates, county, HUC, drainage area, altitude, period of record, counts. |
| `data/raw/` | Original USGS site file, series catalog, and raw daily-values responses (provenance). |
| `data/sites_index.js`, `data/sites/` | Compact data files used by the viewer. |
| `download_ca_discharge.py` | Script that downloads the data (re-run to refresh). |
| `build_viewer_data.py` | Script that rebuilds the viewer data files from the CSVs. |

## Viewer features

- Search box + sortable station list and a clickable California map
- Full-period hydrograph with drag-to-zoom overview strip, range presets,
  linear/log scale, crosshair readout (mouse or arrow keys)
- Summary tiles, seasonal (monthly) flow regime, flow duration curve on a
  normal-probability scale, and annual water-year means — all recomputed for
  the selected date range
- Data tables (annual / monthly / flow percentiles), CSV downloads for any
  station or the current station list, light/dark themes
- Deep links: `ca_streamflow_explorer.html#site=11447650`

## Refreshing the data

```
python download_ca_discharge.py   # refreshes the site catalog + re-downloads all daily values through today
python build_viewer_data.py       # rebuilds the viewer data files
```

The included GitHub Actions workflow (`.github/workflows/update-data.yml`)
runs these automatically every day and deploys to GitHub Pages, and also
publishes the complete CSV archive as the `dataset` release.

**Multi-method sites:** a few stations report the same statistic through more
than one measurement method (e.g. "[Generation]" vs "[Generation + Bypass]").
The CSVs keep every method, labeled by `method_id`/`method_desc`; the viewer
plots one canonical series per statistic — the most complete method's record,
gap-filled from the others.

**Note:** recent values are provisional and subject to revision by USGS.
Cite as: U.S. Geological Survey, National Water Information System (NWISWeb).
