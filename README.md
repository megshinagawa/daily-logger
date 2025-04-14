# Daily Journal and Habit Tracking System

A Python-based system for daily journaling and habit tracking, designed to help you maintain a structured daily log and track your habits effectively.

## Project Structure

The project consists of three main components:

1. **Configure Day (`configure_day/`)**
   - Sets up the daily note template
   - Configures habits and metrics to track
   - Creates the initial structure for each day's log

2. **Daily Logger (`daily_logger/`)**
   - Core functionality for logging daily thoughts and activities
   - Timestamp-based entry system
   - CLI interface for easy logging

3. **Habit Logger (`habit_logger/`)**
   - Tracks and manages habits
   - Provides habit completion status
   - CLI interface for habit management

## Getting Started

### Prerequisites

- Python 3.x
- Basic understanding of command-line interfaces

### Installation

1. Clone this repository
2. Navigate to the project directory
3. Ensure all Python dependencies are installed

## Usage

### Daily Setup

1. Start your day by running the configure_day script:
   ```bash
   python configure_day/configure_day.py
   ```
   This will create a new daily note with your configured habits and metrics.

### During the Day

1. Log your thoughts and activities using the daily logger:
   ```bash
   python daily_logger/daily_logger_cli.py
   ```
   This will allow you to add timestamped entries throughout your day.

2. Track your habits as you complete them:
   ```bash
   python habit_logger/habit_logger_cli.py
   ```
   Use this to mark habits as complete and track your progress.

## File Structure

Daily logs are stored in markdown format with the following structure:
- Date-based filenames
- Habits and metrics section
- Daily log section with timestamped entries

## Configuration

The project uses a centralized `settings.py` file in the root directory that contains all configuration settings for the entire project. You can customize:

### Directory and File Settings
- Base directory for all logs and configurations
- File paths for habit configuration

### Date and Time Formats
- Date format for file names
- Date format for headers
- Time format for log entries

### File Settings
- Default file extension
- Log file templates and formats

### Habit Logger Settings
- Section titles and formatting
- Property formatting
- Value formatting
- Name transformation settings

### Daily Logger Settings
- Header format for new log files
- Entry format for new thoughts

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
