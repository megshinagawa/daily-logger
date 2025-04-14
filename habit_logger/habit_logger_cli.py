#!/usr/bin/env python3
import os
import json
import datetime
import argparse
import sys
from pathlib import Path

# Import settings
try:
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (one level up)
    project_root = os.path.dirname(current_dir)
    # Add project root to Python path
    sys.path.append(project_root)
    from settings import (
        BASE_DIR, HABIT_CONFIG_FILE, DATE_FORMAT, HEADER_DATE_FORMAT, FILE_EXTENSION,
        DAILY_LOG_TITLE, HABIT_PROPERTY_FORMAT, METRIC_PROPERTY_FORMAT,
        UNIT_PROPERTY_FORMAT, TRUE_VALUE, FALSE_VALUE,
        LOWERCASE_PROPERTY_NAMES, REPLACE_SPACES_WITH_UNDERSCORES
    )
except ImportError as e:
    print(f"Error importing settings: {e}")
    print("Settings file not found. Please ensure settings.py exists in the project root.")
    sys.exit(1)


class HabitTracker:
    def __init__(self, config_file=None, data_dir=None):
        """Initialize the habit tracker with optional custom config file and data directory"""
        self.config_file = config_file or HABIT_CONFIG_FILE
        self.data_dir = data_dir or BASE_DIR
        self.habits = []
        self.metrics = []
        
        # Create data directory if it doesn't exist
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        # Create parent directory for config file if it doesn't exist
        Path(os.path.dirname(self.config_file)).mkdir(parents=True, exist_ok=True)
        
        # Load or create config
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default if not exists"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.habits = config.get('habits', [])
                self.metrics = config.get('metrics', [])
        else:
            # Create default config
            self.save_config()
    
    def save_config(self):
        """Save current configuration to file"""
        config = {
            'habits': self.habits,
            'metrics': self.metrics
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def format_property_name(self, name):
        """Format a property name according to settings"""
        result = name
        if LOWERCASE_PROPERTY_NAMES:
            result = result.lower()
        if REPLACE_SPACES_WITH_UNDERSCORES:
            result = result.replace(' ', '_')
        return result
    
    def add_habit(self, name, description=""):
        """Add a new habit to track"""
        if name in [h['name'] for h in self.habits]:
            print(f"Habit '{name}' already exists!")
            return False
        
        self.habits.append({
            'name': name,
            'description': description,
            'created_at': datetime.datetime.now().isoformat()
        })
        self.save_config()
        print(f"Added new habit: {name}")
        return True
    
    def add_metric(self, name, unit="", description=""):
        """Add a new metric to track"""
        if name in [m['name'] for m in self.metrics]:
            print(f"Metric '{name}' already exists!")
            return False
        
        self.metrics.append({
            'name': name,
            'unit': unit,
            'description': description,
            'created_at': datetime.datetime.now().isoformat()
        })
        self.save_config()
        print(f"Added new metric: {name}")
        return True
    
    def remove_habit(self, name):
        """Remove a habit"""
        initial_count = len(self.habits)
        self.habits = [h for h in self.habits if h['name'] != name]
        
        if len(self.habits) < initial_count:
            self.save_config()
            print(f"Removed habit: {name}")
            return True
        else:
            print(f"Habit '{name}' not found!")
            return False
    
    def remove_metric(self, name):
        """Remove a metric"""
        initial_count = len(self.metrics)
        self.metrics = [m for m in self.metrics if m['name'] != name]
        
        if len(self.metrics) < initial_count:
            self.save_config()
            print(f"Removed metric: {name}")
            return True
        else:
            print(f"Metric '{name}' not found!")
            return False
    
    def list_habits(self):
        """List all habits"""
        if not self.habits:
            print("No habits configured. Add some with 'add-habit'.")
            return
        
        print("\nConfigured Habits:")
        print("------------------")
        for habit in self.habits:
            print(f"- {habit['name']}: {habit['description']}")
    
    def list_metrics(self):
        """List all metrics"""
        if not self.metrics:
            print("No metrics configured. Add some with 'add-metric'.")
            return
        
        print("\nConfigured Metrics:")
        print("------------------")
        for metric in self.metrics:
            unit_str = f" ({metric['unit']})" if metric['unit'] else ""
            print(f"- {metric['name']}{unit_str}: {metric['description']}")
    
    def get_log_file_path(self, date):
        """Get the path to the log file for a specific date"""
        date_str = date.strftime(DATE_FORMAT)
        return os.path.join(self.data_dir, f"{date_str}.md")
    
    def read_log_content(self, file_path):
        """Read the content of a log file if it exists"""
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r') as f:
            return f.read()
    
    def update_property_value(self, content, property_name, new_value):
        """Update a property value in the content"""
        lines = content.split('\n')
        
        # Find the property line
        property_line = -1
        for i, line in enumerate(lines):
            if line.startswith(f"{property_name}::"):
                property_line = i
                break
        
        if property_line != -1:
            # Update existing property
            lines[property_line] = f"{property_name}:: {new_value}"
        else:
            # If property not found, append to the end
            lines.append(f"{property_name}:: {new_value}")
        
        return '\n'.join(lines)
    
    def log_entry(self, date=None):
        """Log a new entry for the given date (or today)"""
        if date is None:
            date = datetime.date.today()
        
        # Get habits and metrics data
        habit_data = {}
        for habit in self.habits:
            response = input(f"Did you complete '{habit['name']}' today? (y/n): ").strip().lower()
            habit_data[habit['name']] = response == 'y'
        
        metric_data = {}
        for metric in self.metrics:
            unit_text = f" ({metric['unit']})" if metric['unit'] else ""
            while True:
                response = input(f"Enter value for '{metric['name']}'{unit_text}: ").strip()
                try:
                    # Try to convert to number, but keep as string if it fails
                    if response:
                        float(response)  # Just check if convertible
                    metric_data[metric['name']] = response
                    break
                except ValueError:
                    print(f"Please enter a valid number for {metric['name']}")
        
        # Get log file path
        file_path = self.get_log_file_path(date)
        file_exists = os.path.exists(file_path)
        
        # Read existing content if file exists
        content = self.read_log_content(file_path)
        
        # If file doesn't exist, create initial content
        if content is None:
            date_str = date.strftime(HEADER_DATE_FORMAT)
            content = DAILY_LOG_TITLE.format(date=date_str)
        
        # Update habit values
        for habit in self.habits:
            status = TRUE_VALUE if habit_data.get(habit['name'], False) else FALSE_VALUE
            property_name = self.format_property_name(habit['name'])
            content = self.update_property_value(content, property_name, status)
        
        # Update metric values
        for metric in self.metrics:
            value = metric_data.get(metric['name'], "")
            property_name = self.format_property_name(metric['name'])
            content = self.update_property_value(content, property_name, value)
            
            # Add unit property if specified
            if metric['unit']:
                unit_property_name = f"{property_name}_unit"
                content = self.update_property_value(content, unit_property_name, metric['unit'])
        
        # Write the updated content
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"\nLog saved to {file_path}")
        if not file_exists:
            print(f"Created new log file for {date.strftime(DATE_FORMAT)}")
        return True
    
    def view_log(self, date=None):
        """View log for a specific date"""
        if date is None:
            date = datetime.date.today()
        
        file_path = self.get_log_file_path(date)
        if not os.path.exists(file_path):
            print(f"No log found for {date.strftime(DATE_FORMAT)}")
            return False
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        print(f"\n{'='*50}")
        print(content)
        print(f"{'='*50}")
        return True
    
    def list_logs(self):
        """List all available logs"""
        log_files = [f for f in os.listdir(self.data_dir) if f.endswith('.md')]
        
        if not log_files:
            print("No logs found.")
            return
        
        log_files.sort(reverse=True)  # Sort in descending order (newest first)
        print("\nAvailable Logs:")
        print("--------------")
        for log_file in log_files:
            date_str = log_file.replace('.md', '')
            print(f"- {date_str}")


def parse_date(date_str):
    """Parse date string in the configured format"""
    try:
        return datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    except ValueError:
        print(f"Invalid date format: {date_str}. Please use {DATE_FORMAT}.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Track daily habits and metrics")
    
    # Global options
    parser.add_argument('--config', help=f'Path to config file (default: {HABIT_CONFIG_FILE})')
    parser.add_argument('--data-dir', help=f'Path to data directory (default: {BASE_DIR})')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add habit command
    add_habit_parser = subparsers.add_parser('add-habit', help='Add a new habit to track')
    add_habit_parser.add_argument('name', help='Name of the habit')
    add_habit_parser.add_argument('--description', '-d', help='Description of the habit', default='')
    
    # Add metric command
    add_metric_parser = subparsers.add_parser('add-metric', help='Add a new metric to track')
    add_metric_parser.add_argument('name', help='Name of the metric')
    add_metric_parser.add_argument('--unit', '-u', help='Unit of the metric', default='')
    add_metric_parser.add_argument('--description', '-d', help='Description of the metric', default='')
    
    # Remove commands
    remove_habit_parser = subparsers.add_parser('remove-habit', help='Remove a habit')
    remove_habit_parser.add_argument('name', help='Name of the habit to remove')
    
    remove_metric_parser = subparsers.add_parser('remove-metric', help='Remove a metric')
    remove_metric_parser.add_argument('name', help='Name of the metric to remove')
    
    # List commands
    subparsers.add_parser('list-habits', help='List all habits')
    subparsers.add_parser('list-metrics', help='List all metrics')
    subparsers.add_parser('list-logs', help='List all available logs')
    
    # Log command
    log_parser = subparsers.add_parser('log', help='Create a new log entry')
    log_parser.add_argument('--date', '-d', help=f'Date for the log ({DATE_FORMAT})', default=None)
    
    # View command
    view_parser = subparsers.add_parser('view', help='View a log entry')
    view_parser.add_argument('--date', '-d', help=f'Date to view ({DATE_FORMAT})', default=None)
    
    args = parser.parse_args()
    
    # Initialize tracker with custom config and data directory if provided
    tracker = HabitTracker(config_file=args.config, data_dir=args.data_dir)
    
    if args.command == 'add-habit':
        tracker.add_habit(args.name, args.description)
    elif args.command == 'add-metric':
        tracker.add_metric(args.name, args.unit, args.description)
    elif args.command == 'remove-habit':
        tracker.remove_habit(args.name)
    elif args.command == 'remove-metric':
        tracker.remove_metric(args.name)
    elif args.command == 'list-habits':
        tracker.list_habits()
    elif args.command == 'list-metrics':
        tracker.list_metrics()
    elif args.command == 'list-logs':
        tracker.list_logs()
    elif args.command == 'log':
        date = datetime.date.today() if args.date is None else parse_date(args.date)
        tracker.log_entry(date)
    elif args.command == 'view':
        date = datetime.date.today() if args.date is None else parse_date(args.date)
        tracker.view_log(date)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
