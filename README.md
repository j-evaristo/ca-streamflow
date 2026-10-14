# California USGS Streamflow Data & Explorer

**Evaristo Critical Zone Hydrology Lab**

Complete daily discharge (streamflow) record for every USGS gaging station in
California, plus an interactive offline viewer. Tidal stations also carry
tide-filtered daily discharge - the meaningful measure of net flow where the
tide reverses the current - including the Sacramento-San Joaquin Delta
stations that publish only tide-filtered flow.

**Source:** USGS Water Data APIs (`api.waterdata.usgs.gov`), daily values of
parameter code **00060** (discharge) and, at tidal stations, **72137**
(tide-filtered discharge), in cubic feet per second, updated nightly.

## Contents

| Path | What it is |
|---|---|
| `ca_streamflow_explorer.html` | **Interactive viewer** — open directly in any browser (no server needed). Keep the `data/` folder next to it. |
| `data/csv/USGS_<site>.csv` | Daily values per station: `site_no, date, stat_cd, discharge_cfs, qualifiers, method_id, method_desc, parm_cd` (`method_id` is the USGS time-series id; `parm_cd` 00060 = discharge, 72137 = tide-filtered discharge). |
| `data/sites_metadata.csv` | One row per station: name, coordinates, county, HUC, drainage area, altitude, period of record, counts. |
| `data/raw/` | Station metadata from the USGS Water Data APIs (legacy RDB column layout) and the daily time series included (`series.json`). |
| `data/state/sync_state.json` | Nightly update watermark and reconcile position. |
| `data/sites_index.js`, `data/sites/` | Compact data files used by the viewer. |
| `download_ca_discharge.py`, `waterdata.py` | Scripts that update the data from the USGS Water Data APIs. |
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
python download_ca_discharge.py   # applies everything USGS changed since the last run
python build_viewer_data.py       # rebuilds the viewer data files
```

The included GitHub Actions workflow (`.github/workflows/update-data.yml`)
runs these automatically every day and deploys to GitHub Pages, and also
publishes the complete CSV archive as the `dataset` release.

**Multi-method sites:** a few stations report the same statistic through more
than one measurement method (e.g. "[Generation]" vs "[Generation + Bypass]").
The CSVs keep every series, labeled by `method_id`/`method_desc`; the viewer
plots one canonical series per statistic — the most complete method's record,
gap-filled from the others.

## Data source and update method

Data come from the USGS Water Data APIs (`api.waterdata.usgs.gov/ogcapi/v1`),
which replaced the legacy WaterServices (decommissioned 2027-02-22). The full
record of every station is kept in the nightly `dataset` release; each night's
run applies only what USGS added or changed since the previous run (new days,
approvals and revisions of any age, withdrawn values) and re-reads a rolling
slice of stations in full, so every record is re-verified against USGS about
every two months. See `waterdata.py`.

The legacy WaterServices served about 210,000 values that the new APIs do
not (mostly approved history before a series' current period of record).
They are kept, marked by a legacy `method_id` rather than a USGS time-series id,
and the final WaterServices-era archive is preserved unchanged as the
`legacy-final` release.

**Note:** recent values are provisional and subject to revision by USGS.
Cite as: U.S. Geological Survey, National Water Information System, accessed
via the USGS Water Data APIs.
