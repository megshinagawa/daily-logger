#!/usr/bin/env python3
"""
Daily Thought Logger CLI

Command-line interface for the thought logger module.
"""

import sys
import argparse
import logger

def interactive_mode():
    """Run the logger in interactive mode."""
    print("Daily Thought Logger - Interactive Mode")
    print("Enter your thoughts (type 'exit', 'quit', or press Ctrl+C to exit):")
    
    try:
        while True:
            thought = input("> ").strip()
            
            if thought.lower() in ("exit", "quit"):
                break
            
            if thought:
                file_path = logger.add_thought(thought)
                print(f"Thought logged to {file_path}")
            
    except KeyboardInterrupt:
        print("\nExiting interactive mode...")

def view_today_logs():
    """View today's logs."""
    logs = logger.get_todays_logs()
    
    if logs is None:
        print("No logs for today yet.")
    else:
        print(logs)

def main():
    """Main function to run the CLI tool."""
    parser = argparse.ArgumentParser(description="Log your daily thoughts and ideas with timestamps.")
    
    # Define the subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add a thought
    add_parser = subparsers.add_parser("add", help="Add a new thought")
    add_parser.add_argument("thought", nargs="+", help="The thought or idea to log")
    
    # View today's thoughts
    subparsers.add_parser("view", help="View today's thoughts")
    
    # Interactive mode
    subparsers.add_parser("interactive", help="Run in interactive mode")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no arguments are provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Execute the appropriate command
    if args.command == "add":
        thought = " ".join(args.thought)
        file_path = logger.add_thought(thought)
        print(f"Thought logged to {file_path}")
    
    elif args.command == "view":
        view_today_logs()
    
    elif args.command == "interactive":
        interactive_mode()

if __name__ == "__main__":
    main()
