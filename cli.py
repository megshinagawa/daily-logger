#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path
import datetime
from daily_logger.logger import get_todays_logs, get_log_file_path

def run_configure_day():
    """Run the configure day module"""
    script_path = Path(__file__).parent / "configure_day" / "configure_day.py"
    subprocess.run([sys.executable, str(script_path)])

def run_daily_logger():
    """Run the daily logger module"""
    script_path = Path(__file__).parent / "daily_logger" / "daily_logger_cli.py"
    subprocess.run([sys.executable, str(script_path)])

def run_habit_logger():
    """Run the habit logger module"""
    script_path = Path(__file__).parent / "habit_logger" / "habit_logger_cli.py"
    subprocess.run([sys.executable, str(script_path)])

def view_logs(date=None):
    """View logs for a specific date or today"""
    if date:
        try:
            # Parse date in YYYYMMDD format
            date_obj = datetime.datetime.strptime(date, "%Y%m%d")
            file_path = Path(get_log_file_path(date_obj))
            if not file_path.exists():
                print(f"No logs found for {date}")
                return
            with open(file_path, "r", encoding="utf-8") as f:
                print(f.read())
        except ValueError:
            print("Invalid date format. Please use YYYYMMDD (e.g., 20240414)")
        except Exception as e:
            print(f"Error reading logs: {str(e)}")
    else:
        logs = get_todays_logs()
        if logs:
            print(logs)
        else:
            print("No logs found for today")

def main():
    parser = argparse.ArgumentParser(description="Daily Journal and Habit Tracking System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Configure day command
    subparsers.add_parser("configure", help="Configure the day's template and habits")

    # Daily logger command
    subparsers.add_parser("log", help="Log daily thoughts and activities")

    # Habit logger command
    subparsers.add_parser("habits", help="Track and manage habits")

    # View logs command
    view_parser = subparsers.add_parser("view", help="View logs")
    view_parser.add_argument("--date", help="Date to view logs for (YYYYMMDD)")

    args = parser.parse_args()

    if args.command == "configure":
        run_configure_day()
    elif args.command == "log":
        run_daily_logger()
    elif args.command == "habits":
        run_habit_logger()
    elif args.command == "view":
        view_logs(args.date)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 