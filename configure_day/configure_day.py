import os
from datetime import datetime
import pathlib
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import BASE_DIR, DATE_FORMAT, FILE_EXTENSION, HABIT_CONFIG_FILE, DAILY_LOG_TITLE, DAILY_LOG_HEADER

def create_daily_note():
    """
    Create a daily note with template values if it doesn't already exist.
    """
    # Get today's date
    today = datetime.now()
    date_str = today.strftime(DATE_FORMAT)
    filename = f"{date_str}{FILE_EXTENSION}"
    
    # Create the notes directory if it doesn't exist
    pathlib.Path(BASE_DIR).mkdir(parents=True, exist_ok=True)
    
    # Full path to the note file
    note_path = os.path.join(BASE_DIR, filename)
    
    # Check if today's note already exists
    if os.path.exists(note_path):
        print(f"Daily note for {date_str} already exists at {note_path}")
        return note_path
    
    # Read habits and metrics from JSON file
    habits_section = []
    metrics_section = []
    
    if os.path.exists(HABIT_CONFIG_FILE):
        with open(HABIT_CONFIG_FILE, 'r') as f:
            config = json.load(f)
            
            # Process habits
            for habit in config.get('habits', []):
                habits_section.append(f"{habit['name'].lower()}:: false")
            
            # Process metrics
            for metric in config.get('metrics', []):
                unit = f" ({metric['unit']})" if metric['unit'] else ""
                metrics_section.append(f"{metric['name'].lower()}{unit}:: ")
    
    # Template for the daily note
    template = f"""# {date_str}

{DAILY_LOG_TITLE}
{chr(10).join(habits_section) if habits_section else "- No habits configured"}
{chr(10).join(metrics_section) if metrics_section else "- No metrics configured"}

{DAILY_LOG_HEADER}
"""
    
    # Create the note with the template
    with open(note_path, 'w') as f:
        f.write(template)
    
    print(f"Created daily note for {date_str} at {note_path}")
    return note_path

if __name__ == "__main__":
    create_daily_note()