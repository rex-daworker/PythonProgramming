# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Rex Odomero Oghenerobo according to given task F



from datetime import datetime, date


def read_data(filename: str) -> list:
    """Reads a CSV file and returns the rows in a suitable structure."""
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            # Skip the header row
            next(file)
            for line in file:
                parts = line.strip().split(";")
                if len(parts) >= 4:
                    time_str = parts[0].strip()
                    consumption_str = parts[1].strip().replace(",", ".")
                    production_str = parts[2].strip().replace(",", ".")
                    temp_str = parts[3].strip().replace(",", ".")
                    
                    try:
                        time_obj = datetime.fromisoformat(time_str)
                        consumption = float(consumption_str)
                        production = float(production_str)
                        temperature = float(temp_str)
                        
                        data.append({
                            "time": time_obj,
                            "consumption": consumption,
                            "production": production,
                            "temperature": temperature
                        })
                    except (ValueError, AttributeError):
                        continue
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    
    return data


def show_main_menu() -> str:
    """Prints the main menu and returns the user selection as a string."""
    while True:
        print("\nChoose a report type:")
        print("1) Daily summary for a date range")
        print("2) Monthly summary for one month")
        print("3) Full year 2025 summary")
        print("4) Exit the program")
        
        choice = input("Your choice: ").strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


def show_sub_menu() -> str:
    """Prints the submenu after a report and returns the user selection."""
    while True:
        print("\nWhat would you like to do next?")
        print("1) Write the report to the file report.txt")
        print("2) Create a new report")
        print("3) Exit")
        
        choice = input("Your choice: ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def format_date(d: date) -> str:
    """Formats a date object as dd.mm.yyyy string."""
    return f"{d.day}.{d.month}.{d.year}"


def format_number(value: float) -> str:
    """Formats a float to two decimals with comma as separator."""
    return f"{value:.2f}".replace(".", ",")


def parse_date_input(date_str: str) -> date:
    """Parses a date string in dd.mm.yyyy format and returns a date object."""
    parts = date_str.strip().split(".")
    if len(parts) != 3:
        raise ValueError("Invalid date format")
    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
    return date(year, month, day)


def get_daily_data(data: list, day: date) -> list:
    """Returns all hourly records for a specific day."""
    daily = []
    for record in data:
        if record["time"].date() == day:
            daily.append(record)
    return daily


def get_monthly_data(data: list, month: int, year: int) -> list:
    """Returns all hourly records for a specific month and year."""
    monthly = []
    for record in data:
        if record["time"].month == month and record["time"].year == year:
            monthly.append(record)
    return monthly


def create_daily_report(data: list) -> list[str]:
    """Builds a daily report for a selected date range."""
    lines = []
    
    while True:
        try:
            start_date_str = input("Enter start date (dd.mm.yyyy): ")
            start_date = parse_date_input(start_date_str)
            break
        except (ValueError, IndexError):
            print("Invalid date format. Please use dd.mm.yyyy")
    
    while True:
        try:
            end_date_str = input("Enter end date (dd.mm.yyyy): ")
            end_date = parse_date_input(end_date_str)
            break
        except (ValueError, IndexError):
            print("Invalid date format. Please use dd.mm.yyyy")
    
    # Filter data for the date range
    range_data = []
    for record in data:
        rec_date = record["time"].date()
        if start_date <= rec_date <= end_date:
            range_data.append(record)
    
    # Calculate totals and average
    total_consumption = sum(r["consumption"] for r in range_data)
    total_production = sum(r["production"] for r in range_data)
    
    if range_data:
        avg_temperature = sum(r["temperature"] for r in range_data) / len(range_data)
    else:
        avg_temperature = 0.0
    
    # Build report lines
    lines.append("-" * 53)
    lines.append(f"Report for the period {format_date(start_date)}–{format_date(end_date)}")
    lines.append("- Total consumption: " + format_number(total_consumption) + " kWh")
    lines.append("- Total production: " + format_number(total_production) + " kWh")
    lines.append("- Average temperature: " + format_number(avg_temperature) + " °C")
    lines.append("-" * 53)
    
    return lines


def create_monthly_report(data: list) -> list[str]:
    """Builds a monthly summary report for a selected month."""
    lines = []
    
    while True:
        try:
            month_input = input("Enter month number (1–12): ").strip()
            month = int(month_input)
            if 1 <= month <= 12:
                break
            else:
                print("Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 12.")
    
    # Get month name
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month]
    
    # Filter data for the month
    monthly_data = get_monthly_data(data, month, 2025)
    
    # Calculate totals and average
    total_consumption = sum(r["consumption"] for r in monthly_data)
    total_production = sum(r["production"] for r in monthly_data)
    
    if monthly_data:
        avg_temperature = sum(r["temperature"] for r in monthly_data) / len(monthly_data)
    else:
        avg_temperature = 0.0
    
    # Build report lines
    lines.append("-" * 53)
    lines.append(f"Report for the month: {month_name}")
    lines.append("- Total consumption: " + format_number(total_consumption) + " kWh")
    lines.append("- Total production: " + format_number(total_production) + " kWh")
    lines.append("- Average temperature: " + format_number(avg_temperature) + " °C")
    lines.append("-" * 53)
    
    return lines


def create_yearly_report(data: list) -> list[str]:
    """Builds a full-year summary report."""
    lines = []
    
    # Calculate totals and average
    total_consumption = sum(r["consumption"] for r in data)
    total_production = sum(r["production"] for r in data)
    
    if data:
        avg_temperature = sum(r["temperature"] for r in data) / len(data)
    else:
        avg_temperature = 0.0
    
    # Build report lines
    lines.append("-" * 53)
    lines.append("Report for the year: 2025")
    lines.append("- Total consumption: " + format_number(total_consumption) + " kWh")
    lines.append("- Total production: " + format_number(total_production) + " kWh")
    lines.append("- Average temperature: " + format_number(avg_temperature) + " °C")
    lines.append("-" * 53)
    
    return lines


def print_report_to_console(lines: list[str]) -> None:
    """Prints report lines to the console."""
    for line in lines:
        print(line)


def write_report_to_file(lines: list[str]) -> None:
    """Writes report lines to the file report.txt."""
    try:
        with open("report.txt", "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print("Report written to report.txt")
    except IOError as e:
        print(f"Error writing to file: {e}")


def main() -> None:
    """Main function: reads data, shows menus, and controls report generation."""
    db = read_data("2025.csv")
    
    if not db:
        print("Error: Could not load data from 2025.csv")
        return
    
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            report = create_daily_report(db)
        elif choice == "2":
            report = create_monthly_report(db)
        elif choice == "3":
            report = create_yearly_report(db)
        elif choice == "4":
            print("Thank you! Bye!")
            break
        else:
            continue
        
        # Print report to console
        print_report_to_console(report)
        
        # Show sub-menu
        while True:
            sub_choice = show_sub_menu()
            
            if sub_choice == "1":
                write_report_to_file(report)
                break
            elif sub_choice == "2":
                break
            elif sub_choice == "3":
                print("Thank you! Bye!")
                return


if __name__ == "__main__":
    main()