# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Rex Odomero Oghenerobo according to given task D

from __future__ import annotations
import csv
from datetime import datetime, date
from typing import Dict, List


FINNISH_WEEKDAYS = {
    0: "maanantai",
    1: "tiistai",
    2: "keskiviikko",
    3: "torstai",
    4: "perjantai",
    5: "lauantai",
    6: "sunnuntai",
}


def read_data(filename: str) -> List[Dict]:
    """
    Reads the CSV file and returns a list of dictionaries.
    Each dictionary contains:
        - date (datetime.date)
        - consumption phases v1, v2, v3 (Wh)
        - production phases v1, v2, v3 (Wh)
    """
    rows = []

    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # skip header

        for line in reader:
            timestamp_str = line[0]
            dt = datetime.fromisoformat(timestamp_str)
            d = dt.date()

            # Convert strings to integers (Wh)
            cons1 = int(line[1])
            cons2 = int(line[2])
            cons3 = int(line[3])
            prod1 = int(line[4])
            prod2 = int(line[5])
            prod3 = int(line[6])

            rows.append({
                "date": d,
                "cons": [cons1, cons2, cons3],
                "prod": [prod1, prod2, prod3],
            })

    return rows


def compute_daily_totals(rows: List[Dict]) -> Dict[date, Dict[str, List[float]]]:
    """
    Groups hourly rows by date and sums consumption and production.
    Returns a dictionary:
        { date: { "cons": [kWh1, kWh2, kWh3], "prod": [kWh1, kWh2, kWh3] } }
    """
    daily: Dict[date, Dict[str, List[float]]] = {}

    for row in rows:
        d = row["date"]

        if d not in daily:
            daily[d] = {
                "cons": [0.0, 0.0, 0.0],
                "prod": [0.0, 0.0, 0.0],
            }

        # Add Wh → convert to kWh
        for i in range(3):
            daily[d]["cons"][i] += row["cons"][i] / 1000
            daily[d]["prod"][i] += row["prod"][i] / 1000

    return daily


def format_kwh(value: float) -> str:
    """
    Formats a kWh value with two decimals and a comma as decimal separator.
    """
    return f"{value:.2f}".replace(".", ",")


def print_report(daily: Dict[date, Dict[str, List[float]]]) -> None:
    """
    Prints the weekly electricity report in a clean table format.
    """
    print("Week 42 electricity consumption and production (kWh, by phase)\n")
    print("Day           Date         Consumption [kWh]                 Production [kWh]")
    print("             (dd.mm.yyyy)  v1       v2       v3              v1      v2      v3")
    print("-" * 80)

    for d in sorted(daily.keys()):
        weekday = FINNISH_WEEKDAYS[d.weekday()]
        date_str = d.strftime("%d.%m.%Y")

        cons = daily[d]["cons"]
        prod = daily[d]["prod"]

        cons_fmt = [format_kwh(x) for x in cons]
        prod_fmt = [format_kwh(x) for x in prod]

        print(
            f"{weekday:<12} {date_str:<12} "
            f"{cons_fmt[0]:>7}  {cons_fmt[1]:>7}  {cons_fmt[2]:>7}      "
            f"{prod_fmt[0]:>7} {prod_fmt[1]:>7} {prod_fmt[2]:>7}"
        )


def main() -> None:
    """
    Main function: reads data, computes daily totals, and prints the report.
    """
    filename = "week42.csv"
    rows = read_data(filename)
    daily_totals = compute_daily_totals(rows)
    print_report(daily_totals)


if __name__ == "__main__":
    main()
