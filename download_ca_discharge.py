"""
Update all USGS daily discharge (parameter 00060) for California from
the USGS Water Data APIs (api.waterdata.usgs.gov/ogcapi/v1).

The full record of every station lives in the repository's nightly dataset
archive; each run applies only what USGS added or changed since the previous
run (see waterdata.py). Outputs:

  data/csv/USGS_<site>.csv         long-format CSV: site_no, date, stat_cd,
                                   discharge_cfs, qualifiers, method_id, method_desc
  data/raw/ca_sites_expanded.rdb  site metadata (legacy RDB column layout)
  data/raw/series.json             in-scope daily series (method_id = time series id)
  data/state/sync_state.json       sync watermark and reconcile position
"""

import os

import waterdata

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE_FIPS = "06"
USER_AGENT = "CA-discharge-research/2.0 (+https://github.com/j-evaristo/ca-streamflow; contact: evaristo@uga.edu)"
OBSOLETE = ["ca_series_catalog.rdb"]   # legacy WaterServices files no longer produced


def main():
    pipeline = waterdata.Pipeline(
        ROOT, "streamflow", STATE_FIPS, ["00060"], USER_AGENT,
        rdb_files={"ca_sites_expanded.rdb": "state"},
        reconcile_bins=10)
    pipeline.run()
    for name in OBSOLETE:
        path = os.path.join(ROOT, "data", "raw", name)
        if os.path.exists(path):
            os.remove(path)


if __name__ == "__main__":
    main()
