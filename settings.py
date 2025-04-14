#!/usr/bin/env python3
"""
Consolidated Settings for the Daily Project

This file contains all configuration settings for the project's components:
- Daily Logger
- Habit Logger
- Day Configuration
"""

import os

# ===== Directory and File Settings =====
# Base directory for all logs and configurations
BASE_DIR = os.path.join(os.path.expanduser("~"), "Obsidian", "EPSILON-ALPHA", "04 periodic", "01 daily")

# File paths
HABIT_CONFIG_FILE = os.path.join(BASE_DIR, "habit_config.json")

# ===== Date and Time Formats =====
# Date format for file names
DATE_FORMAT = "%Y%m%d"
# Date format for headers
HEADER_DATE_FORMAT = "%A, %B %d, %Y"
# Time format for log entries
TIME_FORMAT = "%H:%M"

# ===== File Settings =====
FILE_EXTENSION = ".md"

# ===== Daily Logger Settings =====
# Header format for new log files
DAILY_LOG_HEADER = "## Daily Log\n"
# Entry format for new thoughts
DAILY_ENTRY_TEMPLATE = "`{time}`\n{thought}\n\n"

# ===== Habit Logger Settings =====
# Section titles
DAILY_LOG_TITLE = "## Habits & Metrics\n"

# Property formatting
HABIT_PROPERTY_FORMAT = "{name}:: {value}\n"
METRIC_PROPERTY_FORMAT = "{name}:: {value}\n"
UNIT_PROPERTY_FORMAT = "{name}_unit:: {value}\n"

# Value formatting
TRUE_VALUE = "true"
FALSE_VALUE = "false"

# Name transformation settings
LOWERCASE_PROPERTY_NAMES = True
REPLACE_SPACES_WITH_UNDERSCORES = True 