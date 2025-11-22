#!/usr/bin/env python3
"""
Convenience script to run the Travel Planner Agent in different modes
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Travel Planner Agent")
    parser.add_argument(
        "--mode", 
        choices=["cli", "web", "demo"], 
        default="cli",
        help="Run mode: cli (default), web, or demo"
    )
    
    args = parser.parse_args()
    
    if args.mode == "cli":
        # Run CLI interface
        from cli import main as cli_main
        cli_main()
    elif args.mode == "web":
        # Run web interface
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    elif args.mode == "demo":
        # Run demo
        from main import demo
        demo()

if __name__ == "__main__":
    main()