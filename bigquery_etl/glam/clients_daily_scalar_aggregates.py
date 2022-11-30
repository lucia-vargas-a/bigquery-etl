#!/usr/bin/env python3
"""clients_daily_scalar_aggregates query generator."""
import argparse
import sys
from typing import Dict, List

from jinja2 import Environment, PackageLoader

from bigquery_etl.format_sql.formatter import reformat
from bigquery_etl.util.glam_probe_utils import (
    get_etl_excluded_probes_quickfix,
    probe_is_recent_glean,
    query_hotlist,
)

from .utils import get_schema, ping_type_from_table

ATTRIBUTES = ",".join(
    [
        "client_id",
        "ping_type",
        "submission_date",
        "os",
        "app_version",
        "app_build_id",
        "channel",
    ]
)


def render_main(**kwargs):
    """Create a SQL query for the clients_daily_scalar_aggregates dataset."""
    env = Environment(loader=PackageLoader("bigquery_etl", "glam/templates"))
    main_sql = env.get_template("clients_daily_scalar_aggregates_v1.sql")
    return reformat(main_sql.render(**kwargs))


def get_labeled_metrics_sql(
    probes: Dict[str, List[str]], value_type: str = "INT64"
) -> str:
    """Get the SQL for labeled scalar metrics."""
    probes_struct = []
    for metric_type, _probes in probes.items():
        for probe in _probes:
            probes_struct.append(
                f"('{probe}', '{metric_type}', metrics.{metric_type}.{probe})"
            )

    probes_struct.sort()
    probes_arr = ",\n".join(probes_struct)
    return probes_arr


def get_unlabeled_metrics_sql(probes: Dict[str, List[str]]) -> str:
    """Put together the subsets of SQL required to query scalars or booleans."""
    probe_structs = []
    for probe in probes.pop("boolean", []):
        probe_structs.append(
            (
                f"('{probe}', 'boolean', '', 'false', "
                f"SUM(CAST(NOT metrics.boolean.{probe} AS INT64)))"
            )
        )
        probe_structs.append(
            (
                f"('{probe}', 'boolean', '', 'true', "
                f"SUM(CAST(metrics.boolean.{probe} AS INT64)))"
            )
        )

    for metric_type, _probes in probes.items():
        # timespans are nested within an object that also carries the unit of
        # of time associated with the value
        suffix = ".value" if metric_type == "timespan" else ""
        for probe in _probes:
            for agg_func in ["max", "avg", "min", "sum"]:
                probe_structs.append(
                    (
                        f"('{probe}', '{metric_type}', '', '{agg_func}', "
                        f"{agg_func}(CAST(metrics.{metric_type}.{probe}{suffix} AS INT64)))"
                    )
                )
            probe_structs.append(
                f"('{probe}', '{metric_type}', '', 'count', "
                f"IF(MIN(metrics.{metric_type}.{probe}{suffix}) IS NULL, NULL, COUNT(*)))"
            )

    probe_structs.sort()
    probes_arr = ",\n".join(probe_structs)
    return probes_arr


def get_scalar_metrics(
    schema: Dict, scalar_type: str, product: str
) -> Dict[str, List[str]]:
    """Find all scalar probes in a Glean table.

    Metric types are defined in the Glean documentation found here:
    https://mozilla.github.io/glean/book/user/metrics/index.html
    """
    assert scalar_type in ("unlabeled", "labeled")
    metric_type_set = {
        "unlabeled": ["boolean", "counter", "quantity", "timespan"],
        "labeled": ["labeled_counter"],
    }
    scalars: Dict[str, List[str]] = {
        metric_type: [] for metric_type in metric_type_set[scalar_type]
    }
    excluded_metrics = get_etl_excluded_probes_quickfix("fenix")
    hotlist = query_hotlist()

    # Iterate over every element in the schema under the metrics section and
    # collect a list of metric names.
    for root_field in schema:
        if root_field["name"] != "metrics":
            continue
        for metric_field in root_field["fields"]:
            metric_type = metric_field["name"]
            if metric_type not in metric_type_set[scalar_type]:
                continue
            for field in metric_field["fields"]:
                if (
                    field["name"] in hotlist
                    or probe_is_recent_glean(field["name"], product)
                ) and field["name"] not in excluded_metrics:
                    scalars[metric_type].append(field["name"])
    return scalars


def main():
    """Print a clients_daily_scalar_aggregates query to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-parameterize",
        action="store_true",
        help="Generate a query without parameters",
    )
    parser.add_argument("--source-table", type=str, help="Name of Glean table")
    parser.add_argument(
        "--product",
        type=str,
        default="org_mozilla_fenix",
    )
    args = parser.parse_args()

    # If set to 1 day, then runs of copy_deduplicate may not be done yet
    submission_date = (
        "date_sub(current_date, interval 2 day)"
        if args.no_parameterize
        else "@submission_date"
    )
    header = (
        "-- Query generated by: python3 -m "
        "bigquery_etl.glam.clients_daily_scalar_aggregates "
        f"--source-table {args.source_table}"
        + (" --no-parameterize" if args.no_parameterize else "")
    )

    # This enables build_id filtering against Buildhub data
    # and filtering out of an erroneous version "1024" (see query template for details).
    # Only the desktop builds are reported to Buildhub
    filter_desktop_builds = True if args.product == "firefox_desktop" else False

    schema = get_schema(args.source_table)
    unlabeled_metric_names = get_scalar_metrics(schema, "unlabeled", args.product)
    labeled_metric_names = get_scalar_metrics(schema, "labeled", args.product)
    unlabeled_metrics = get_unlabeled_metrics_sql(unlabeled_metric_names).strip()
    labeled_metrics = get_labeled_metrics_sql(labeled_metric_names).strip()

    if not unlabeled_metrics and not labeled_metrics:
        print(header)
        print("-- Empty query: no probes found!")
        sys.exit(1)
    print(
        render_main(
            header=header,
            filter_desktop_builds=filter_desktop_builds,
            source_table=args.source_table,
            submission_date=submission_date,
            attributes=ATTRIBUTES,
            unlabeled_metrics=unlabeled_metrics,
            labeled_metrics=labeled_metrics,
            ping_type=ping_type_from_table(args.source_table),
        )
    )


if __name__ == "__main__":
    main()
