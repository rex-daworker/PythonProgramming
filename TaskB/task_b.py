# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Rex Odomero Oghenerobo according to given task B

"""
A program that reads reservation data from a file
and prints them to the console using functions:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly rate: 19,95 €
Total price: 39,90 €
Paid: Yes
Venue: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com
"""

from datetime import datetime


def print_reservation_number(reservation: list) -> None:
    """Prints the reservation number."""
    number = int(reservation[0])
    print(f"Reservation number: {number}")


def print_booker(reservation: list) -> None:
    """Prints the name of the person who made the reservation."""
    booker = reservation[1]
    print(f"Booker: {booker}")


def print_date(reservation: list) -> None:
    """Prints the reservation date in DD.MM.YYYY format."""
    date = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    print(f"Date: {date.strftime('%d.%m.%Y')}")


def print_start_time(reservation: list) -> None:
    """Prints the start time in HH.MM format."""
    time = datetime.strptime(reservation[3], "%H:%M").time()
    print(f"Start time: {time.strftime('%H.%M')}")


def print_hours(reservation: list) -> None:
    """Prints the number of reserved hours."""
    hours = int(reservation[4])
    print(f"Number of hours: {hours}")


def print_hourly_rate(reservation: list) -> None:
    """Prints the hourly rate in European format."""
    rate = float(reservation[5])
    print(f"Hourly rate: {str(f'{rate:.2f}').replace('.', ',')} €")


def print_total_price(reservation: list) -> None:
    """Calculates and prints the total price."""
    hours = int(reservation[4])
    rate = float(reservation[5])
    total = hours * rate
    print(f"Total price: {str(f'{total:.2f}').replace('.', ',')} €")


def print_paid(reservation: list) -> None:
    """Prints whether the reservation is paid."""
    paid = reservation[6].strip().lower() == "true"
    print(f"Paid: {'Yes' if paid else 'No'}")


def print_venue(reservation: list) -> None:
    """Prints the reserved venue."""
    print(f"Venue: {reservation[7]}")


def print_phone(reservation: list) -> None:
    """Prints the phone number."""
    print(f"Phone: {reservation[8]}")


def print_email(reservation: list) -> None:
    """Prints the email address."""
    print(f"Email: {reservation[9]}")


def main():
    """Reads reservation data from a file and prints them using functions."""
    reservations = "reservations.txt"

    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip().split('|')

    print_reservation_number(reservation)
    print_booker(reservation)
    print_date(reservation)
    print_start_time(reservation)
    print_hours(reservation)
    print_hourly_rate(reservation)
    print_total_price(reservation)
    print_paid(reservation)
    print_venue(reservation)
    print_phone(reservation)
    print_email(reservation)


if __name__ == "__main__":
    main()
