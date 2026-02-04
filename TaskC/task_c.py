# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task

# Copyright (c) 2026 ...
# Modified by Rex Odomero Oghenerobo according to given task

"""
A program that prints reservation information according to task requirements.
"""

from datetime import datetime
from typing import List

# Column headers (used only in Part A printing)
HEADERS = [
    "reservationId",
    "name",
    "email",
    "phone",
    "reservationDate",
    "reservationTime",
    "durationHours",
    "price",
    "confirmed",
    "reservedResource",
    "createdAt",
]


def convert_reservation_data(reservation: list) -> list:
    """
    Convert data types to meet program requirements

    Parameters:
     reservation (list): Unconverted reservation -> 11 columns

    Returns:
     converted (list): Converted data types
    """
    converted: list = []


    # 1) reservationId (str -> int)
    converted.append(int(reservation[0]))

    # 2) name (str)
    converted.append(reservation[1])

    # 3) email (str)
    converted.append(reservation[2])

    # 4) phone (str)
    converted.append(reservation[3])

    # 5) reservationDate (str -> date)
    converted.append(datetime.strptime(reservation[4], "%Y-%m-%d").date())

    # 6) reservationTime (str -> time)
    converted.append(datetime.strptime(reservation[5], "%H:%M").time())

    # 7) durationHours (str -> int)
    converted.append(int(reservation[6]))

    # 8) price (str -> float)
    converted.append(float(reservation[7]))

    # 9) confirmed (str -> bool)
    converted.append(reservation[8] == "True")

    # 10) reservedResource (str)
    converted.append(reservation[9])

    # 11) createdAt (str -> datetime)
    converted.append(datetime.strptime(reservation[10].strip(), "%Y-%m-%d %H:%M:%S"))

    return converted



def fetch_reservations(reservation_file: str) -> list:
    """
    Reads reservations from a file and converts each row.
    """
    reservations = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            fields = line.split("|")
            reservations.append(convert_reservation_data(fields))
    return reservations


# ---------------------- PART B FUNCTIONS ---------------------- #

def confirmed_reservations(reservations: List[List]) -> None:
    """
    Prints all confirmed reservations in required format.
    """
    print("1) Confirmed Reservations")
    for r in reservations:
        if r[8]:  # confirmed == True
            date_str = r[4].strftime("%d.%m.%Y")
            time_str = r[5].strftime("%H.%M")
            print(f"- {r[1]}, {r[9]}, {date_str} at {time_str}")
    print()


def long_reservations(reservations: List[List]) -> None:
    """
    Prints reservations with duration >= 3 hours.
    """
    print("2) Long Reservations (≥ 3 h)")
    for r in reservations:
        if r[6] >= 3:
            date_str = r[4].strftime("%d.%m.%Y")
            time_str = r[5].strftime("%H.%M")
            print(f"- {r[1]}, {date_str} at {time_str}, duration {r[6]} h, {r[9]}")
    print()


def confirmation_statuses(reservations: List[List]) -> None:
    """
    Prints each reservation's confirmation status.
    """
    print("3) Reservation Confirmation Status")
    for r in reservations:
        status = "Confirmed" if r[8] else "NOT Confirmed"
        print(f"- {r[1]} → {status}")
    print()


def confirmation_summary(reservations: List[List]) -> None:
    """
    Prints summary of confirmed vs not confirmed reservations.
    """
    print("4) Confirmation Summary")
    confirmed_count = sum(1 for r in reservations if r[8])
    not_confirmed_count = len(reservations) - confirmed_count

    print(f"- Confirmed reservations: {confirmed_count} pcs")
    print(f"- Not confirmed reservations: {not_confirmed_count} pcs")
    print()


def total_revenue(reservations: List[List]) -> None:
    """
    Calculates and prints total revenue from confirmed reservations.
    """
    print("5) Total Revenue from Confirmed Reservations")

    # Sum price only for confirmed reservations
    total = sum(r[7] for r in reservations if r[8])

    # Format with comma instead of dot
    amount_str = f"{total:.2f}".replace(".", ",")

    print(f"Total revenue from confirmed reservations: {amount_str} €")
    print()


# ---------------------- MAIN PROGRAM ---------------------- #

def main():
    """
    Loads reservations and prints all required outputs.
    """
    reservations = fetch_reservations("reservations.txt")

    # PART B – Required final output
    confirmed_reservations(reservations)
    long_reservations(reservations)
    confirmation_statuses(reservations)
    confirmation_summary(reservations)
    total_revenue(reservations)


if __name__ == "__main__":
    main()
