# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by Rex Odomero Oghenerobo according to given task E

"""
Task E - Three Weeks of Electricity Consumption and Production (kWh) to a File

This program reads electricity consumption and production data from three weekly CSV files,
calculates daily summaries, and writes a formatted report to a text file.
All values are converted from Wh to kWh using Finnish formatting conventions.
"""

from datetime import datetime, date
from typing import List, Dict, Tuple


def read_data(filename: str) -> List:
    """
    Reads a CSV file and returns the rows as a list of dictionaries.
    
    Args:
        filename: Path to the CSV file to read
        
    Returns:
        A list of dictionaries, where each dictionary represents one row with keys:
        'timestamp', 'cons_p1', 'cons_p2', 'cons_p3', 'prod_p1', 'prod_p2', 'prod_p3'
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        # Skip header line
        for line in lines[1:]:
            line = line.strip()
            if line:
                parts = line.split(';')
                if len(parts) == 7:
                    data.append({
                        'timestamp': parts[0],
                        'cons_p1': float(parts[1]),
                        'cons_p2': float(parts[2]),
                        'cons_p3': float(parts[3]),
                        'prod_p1': float(parts[4]),
                        'prod_p2': float(parts[5]),
                        'prod_p3': float(parts[6])
                    })
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except ValueError as e:
        print(f"Error parsing file '{filename}': {e}")
        return []
    
    return data


def calculate_daily_summaries(data: List) -> Dict:
    """
    Calculates daily summaries for consumption and production by phase.
    
    Groups hourly data by date and sums up consumption and production for each phase.
    
    Args:
        data: List of dictionaries containing hourly measurement data
        
    Returns:
        A dictionary with dates as keys and daily summaries as values,
        each containing consumption and production totals for phases 1-3 (in Wh)
    """
    daily_summaries = {}
    
    for record in data:
        dt = datetime.fromisoformat(record['timestamp'])
        day = dt.date()
        
        if day not in daily_summaries:
            daily_summaries[day] = {
                'cons_p1': 0.0,
                'cons_p2': 0.0,
                'cons_p3': 0.0,
                'prod_p1': 0.0,
                'prod_p2': 0.0,
                'prod_p3': 0.0
            }
        
        # Add hourly values to daily totals
        daily_summaries[day]['cons_p1'] += record['cons_p1']
        daily_summaries[day]['cons_p2'] += record['cons_p2']
        daily_summaries[day]['cons_p3'] += record['cons_p3']
        daily_summaries[day]['prod_p1'] += record['prod_p1']
        daily_summaries[day]['prod_p2'] += record['prod_p2']
        daily_summaries[day]['prod_p3'] += record['prod_p3']
    
    return daily_summaries


def convert_wh_to_kwh_and_format(value_wh: float) -> str:
    """
    Converts a value from Wh to kWh and formats it with Finnish conventions.
    
    Args:
        value_wh: Value in Watt-hours
        
    Returns:
        Formatted string with comma as decimal separator and two decimal places
    """
    value_kwh = value_wh / 1000.0
    value_str = f"{value_kwh:.2f}"
    value_str = value_str.replace(".", ",")
    return value_str


def get_finnish_weekday(day: date) -> str:
    """
    Returns the Finnish name of the weekday for a given date.
    
    Args:
        day: A date object
        
    Returns:
        The Finnish name of the weekday (Monday, Tuesday, etc.)
    """
    finnish_weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    return finnish_weekdays[day.weekday()]


def format_date(day: date) -> str:
    """
    Formats a date according to Finnish conventions (dd.mm.yyyy).
    
    Args:
        day: A date object
        
    Returns:
        Formatted date string in dd.mm.yyyy format
    """
    return f"{day.day:02d}.{day.month:02d}.{day.year}"


def format_report_row(day: date, summary: Dict) -> str:
    """
    Formats a single day's summary as a report row.
    
    Args:
        day: A date object for the day
        summary: Dictionary containing daily consumption and production totals (in Wh)
        
    Returns:
        A formatted string representing one row of the report
    """
    weekday = get_finnish_weekday(day)
    date_str = format_date(day)
    
    cons_p1 = convert_wh_to_kwh_and_format(summary['cons_p1'])
    cons_p2 = convert_wh_to_kwh_and_format(summary['cons_p2'])
    cons_p3 = convert_wh_to_kwh_and_format(summary['cons_p3'])
    
    prod_p1 = convert_wh_to_kwh_and_format(summary['prod_p1'])
    prod_p2 = convert_wh_to_kwh_and_format(summary['prod_p2'])
    prod_p3 = convert_wh_to_kwh_and_format(summary['prod_p3'])
    
    row = f"{weekday:<11}{date_str:<15}{cons_p1:>8}  {cons_p2:>8}  {cons_p3:>8}      {prod_p1:>8}  {prod_p2:>8}  {prod_p3:>8}"
    
    return row


def write_report(filename: str, weekly_data: Dict) -> None:
    """
    Writes a formatted report to a text file.
    
    Creates a clear, well-structured report with sections for each week,
    including daily summaries with proper headings and separators.
    
    Args:
        filename: Path to the output report file
        weekly_data: Dictionary with week numbers as keys and daily summaries as values
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("=" * 85 + "\n")
        file.write("ELECTRICITY CONSUMPTION AND PRODUCTION REPORT - WEEKS 41, 42, 43\n")
        file.write("=" * 85 + "\n\n")
        
        for week_num in sorted(weekly_data.keys()):
            daily_summaries = weekly_data[week_num]
            
            # Write week heading
            file.write(f"Week {week_num} electricity consumption and production (kWh, by phase)\n")
            file.write("-" * 85 + "\n")
            file.write("Day        Date            Consumption [kWh]            Production [kWh]\n")
            file.write("                           v1       v2       v3           v1       v2       v3\n")
            file.write("-" * 85 + "\n")
            
            # Write daily rows
            sorted_days = sorted(daily_summaries.keys())
            for day in sorted_days:
                summary = daily_summaries[day]
                row = format_report_row(day, summary)
                file.write(row + "\n")
            
            file.write("-" * 85 + "\n\n")
        
        # Optional: Add total summary for all weeks
        file.write("=" * 85 + "\n")
        file.write("TOTAL SUMMARY - ALL WEEKS (41, 42, 43)\n")
        file.write("=" * 85 + "\n\n")
        
        total_cons_p1 = 0.0
        total_cons_p2 = 0.0
        total_cons_p3 = 0.0
        total_prod_p1 = 0.0
        total_prod_p2 = 0.0
        total_prod_p3 = 0.0
        
        for week_num in sorted(weekly_data.keys()):
            for day, summary in weekly_data[week_num].items():
                total_cons_p1 += summary['cons_p1']
                total_cons_p2 += summary['cons_p2']
                total_cons_p3 += summary['cons_p3']
                total_prod_p1 += summary['prod_p1']
                total_prod_p2 += summary['prod_p2']
                total_prod_p3 += summary['prod_p3']
        
        total_cons = total_cons_p1 + total_cons_p2 + total_cons_p3
        total_prod = total_prod_p1 + total_prod_p2 + total_prod_p3
        
        file.write(f"Total Consumption (all phases): {convert_wh_to_kwh_and_format(total_cons)} kWh\n")
        file.write(f"  - Phase 1: {convert_wh_to_kwh_and_format(total_cons_p1)} kWh\n")
        file.write(f"  - Phase 2: {convert_wh_to_kwh_and_format(total_cons_p2)} kWh\n")
        file.write(f"  - Phase 3: {convert_wh_to_kwh_and_format(total_cons_p3)} kWh\n\n")
        
        file.write(f"Total Production (all phases): {convert_wh_to_kwh_and_format(total_prod)} kWh\n")
        file.write(f"  - Phase 1: {convert_wh_to_kwh_and_format(total_prod_p1)} kWh\n")
        file.write(f"  - Phase 2: {convert_wh_to_kwh_and_format(total_prod_p2)} kWh\n")
        file.write(f"  - Phase 3: {convert_wh_to_kwh_and_format(total_prod_p3)} kWh\n")


def main() -> None:
    """
    Main function: reads data from three weekly CSV files, computes daily summaries,
    and writes a formatted report to a file.
    
    Processes weeks 41, 42, and 43 electricity consumption and production data,
    converting from Wh to kWh and applying Finnish formatting conventions.
    """
    # Define CSV files to process
    csv_files = {
        41: 'week41.csv',
        42: 'week42.csv',
        43: 'week43.csv'
    }
    
    # Dictionary to store weekly data
    weekly_data = {}
    
    # Process each week
    for week_num, filename in csv_files.items():
        print(f"Processing {filename}...")
        
        # Read data from CSV file
        data = read_data(filename)
        
        if data:
            # Calculate daily summaries
            daily_summaries = calculate_daily_summaries(data)
            weekly_data[week_num] = daily_summaries
            print(f"  ✓ Week {week_num}: {len(daily_summaries)} days processed")
        else:
            print(f"  ✗ Week {week_num}: No data found")
    
    # Write report to file
    print("\nWriting report to summary.txt...")
    write_report('summary.txt', weekly_data)
    print("✓ Report successfully written to summary.txt")
    print("\nTask completed!")


if __name__ == "__main__":
    main()
