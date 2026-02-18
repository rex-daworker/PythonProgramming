# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

"""
Class-based implementation for Task G: Reservation class and functions
that print reservation data according to requirements.
"""
from datetime import datetime
from typing import List


class Reservation:
    def __init__(self, fields: List[str]):
        # fields order in file: as documented in task
        self.reservationId = int(fields[0])
        self.name = fields[1]
        self.email = fields[2]
        self.phone = fields[3]
        self.reservationDate = datetime.strptime(fields[4], "%Y-%m-%d").date()
        self.reservationTime = datetime.strptime(fields[5], "%H:%M").time()
        self.durationHours = int(fields[6])
        self.price = float(fields[7])
        self.confirmed = True if fields[8].strip() == 'True' else False
        self.reservedResource = fields[9]
        self.createdAt = datetime.strptime(fields[10].strip(), "%Y-%m-%d %H:%M:%S")

    def revenue(self) -> float:
        return self.durationHours * self.price


def fetch_reservations(reservation_file: str) -> List[Reservation]:
    reservations: List[Reservation] = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                fields = line.split("|")
                reservations.append(Reservation(fields))
    return reservations


def confirmed_reservations(reservations: List[Reservation]) -> None:
    for r in reservations:
        if r.confirmed:
            print(f'- {r.name}, {r.reservedResource}, {r.reservationDate.strftime("%d.%m.%Y")} at {r.reservationTime.strftime("%H.%M")}')


def long_reservations(reservations: List[Reservation]) -> None:
    for r in reservations:
        if r.durationHours >= 3:
            print(f'- {r.name}, {r.reservationDate.strftime("%d.%m.%Y")} at {r.reservationTime.strftime("%H.%M")}, duration {r.durationHours} h, {r.reservedResource}')


def confirmation_statuses(reservations: List[Reservation]) -> None:
    for r in reservations:
        print(f'{r.name} → {"Confirmed" if r.confirmed else "NOT Confirmed"}')


def confirmation_summary(reservations: List[Reservation]) -> None:
    confirmed_count = sum(1 for r in reservations if r.confirmed)
    total = len(reservations)
    not_confirmed = total - confirmed_count
    print(f'- Confirmed reservations: {confirmed_count} pcs\n- Not confirmed reservations: {not_confirmed} pcs')


def total_revenue(reservations: List[Reservation]) -> None:
    revenue = sum(r.revenue() for r in reservations if r.confirmed)
    print(f'Total revenue from confirmed reservations: {revenue:.2f} €'.replace('.', ','))


def main() -> None:
    reservations = fetch_reservations("reservations.txt")
    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)


if __name__ == "__main__":
    main()
