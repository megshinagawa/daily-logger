#!/usr/bin/env python3
"""
Daily Thought Logger Module

Core functionality for logging thoughts and ideas with timestamps.
"""

import os
import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import (
    BASE_DIR, 
    DATE_FORMAT, 
    TIME_FORMAT, 
    FILE_EXTENSION,
    DAILY_LOG_HEADER,
    DAILY_ENTRY_TEMPLATE
)

def ensure_log_directory():
    """Creates the log directory if it doesn't exist."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def get_log_file_path(date=None):
    """
    Returns the path to the log file for the given date (or today by default).
    
    Args:
        date: A datetime object representing the date (default: current date)
    
    Returns:
        str: Path to the log file
    """
    if date is None:
        date = datetime.datetime.now()
    
    # Format filename according to settings
    file_name = f"{date.strftime(DATE_FORMAT)}{FILE_EXTENSION}"
    return os.path.join(BASE_DIR, file_name)

def initialize_log_file(file_path, date):
    """
    Initializes a log file with header if it doesn't exist.
    
    Args:
        file_path: Path to the log file
        date: A datetime object representing the date
    """
    if not os.path.exists(file_path):
        ensure_log_directory()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(DAILY_LOG_HEADER.format(date=date.strftime(DATE_FORMAT)))

def add_thought(thought, date=None):
    """
    Adds a timestamped thought to the log file.
    
    Args:
        thought: The thought or idea to log
        date: A datetime object for the log date (default: current date/time)
    
    Returns:
        str: Path to the log file where the thought was saved
    """
    now = datetime.datetime.now()
    if date is None:
        date = now
    
    file_path = get_log_file_path(date)
    initialize_log_file(file_path, date)
    
    # Format the entry with timestamp according to settings
    formatted_entry = DAILY_ENTRY_TEMPLATE.format(
        time=now.strftime(TIME_FORMAT),
        thought=thought
    )
    
    # Append the entry to the file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(formatted_entry)
    
    return file_path

def get_todays_logs():
    """
    Retrieves today's logs as a string.
    
    Returns:
        str: The contents of today's log file, or None if no logs exist
    """
    file_path = get_log_file_path()
    
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
