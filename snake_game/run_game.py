#!/usr/bin/env python3
"""
Snake Game Launcher
Simple script to run the Snake Game
"""

import sys
import os

# Add the parent directory to the path so we can import snake_game
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """Launch the Snake Game"""
    try:
        from snake_game.main import main as game_main

        game_main()
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure you're running this from the correct directory.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
