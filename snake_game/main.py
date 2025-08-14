"""
Snake Game Main Module
Main game loop and application entry point
"""

import time
import sys
from typing import Optional

from .game import GameState, GameDisplay, InputHandler, Direction


class SnakeGame:
    """Main Snake Game controller"""

    def __init__(self, width: int = 30, height: int = 20):
        """Initialize the game"""
        self.width = width
        self.height = height
        self.game_state = None
        self.display = GameDisplay()
        self.input_handler = InputHandler()
        self.running = False
        self.paused = False

    def run(self):
        """Main game entry point"""
        try:
            self._show_start_menu()
            if self._start_new_game():
                self._game_loop()
        except KeyboardInterrupt:
            self._handle_exit()
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Game terminated.")

    def _show_start_menu(self):
        """Show start menu and handle navigation"""
        while True:
            self.display.show_start_screen()

            with self.input_handler:
                key = self.input_handler.wait_for_key()

            if key == "q":
                sys.exit(0)
            elif key == "i":
                self._show_instructions()
            else:
                break

    def _show_instructions(self):
        """Show instructions screen"""
        self.display.show_instructions()

        with self.input_handler:
            self.input_handler.wait_for_key()

    def _start_new_game(self) -> bool:
        """Initialize a new game"""
        try:
            self.game_state = GameState(self.width, self.height)
            self.running = True
            self.paused = False
            return True
        except Exception as e:
            print(f"Failed to start game: {e}")
            return False

    def _game_loop(self):
        """Main game loop"""
        last_move_time = 0

        with self.input_handler:
            while self.running and self.game_state:
                current_time = time.time()

                # Handle input
                self._handle_input()

                # Update game state if not paused
                if not self.paused:
                    move_delay = self.game_state.get_speed()

                    if current_time - last_move_time >= move_delay:
                        # Update game state
                        if not self.game_state.update():
                            # Game over
                            self._handle_game_end()
                            break

                        # Check for level completion
                        if (
                            self.game_state.foods_eaten
                            >= self.game_state.foods_per_level
                        ):
                            if (
                                self.game_state.level
                                > self.game_state.level_manager.get_max_level()
                            ):
                                # Game won
                                self._handle_game_end()
                                break
                            else:
                                # Level completed, show transition
                                self._handle_level_complete()

                        # Render game
                        self.display.render_game(self.game_state)
                        last_move_time = current_time

                # Small delay to prevent high CPU usage
                time.sleep(0.01)

    def _handle_input(self):
        """Handle user input"""
        key = self.input_handler.get_key()

        if key is None:
            return

        if key == "q":
            self.running = False
        elif key == "p":
            self._toggle_pause()
        elif not self.paused:
            # Movement keys
            if key == "w":
                self.game_state.change_snake_direction(Direction.UP)
            elif key == "s":
                self.game_state.change_snake_direction(Direction.DOWN)
            elif key == "a":
                self.game_state.change_snake_direction(Direction.LEFT)
            elif key == "d":
                self.game_state.change_snake_direction(Direction.RIGHT)

    def _toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused

        if self.paused:
            self.display.show_pause_screen(self.game_state)
        else:
            # Clear any pending input and resume
            self.input_handler.flush_input()

    def _handle_level_complete(self):
        """Handle level completion"""
        self.display.show_level_complete(self.game_state)

        # Wait for user to continue
        with self.input_handler:
            self.input_handler.wait_for_key()

    def _handle_game_end(self):
        """Handle game over or victory"""
        self.display.show_game_over(self.game_state)

        print("\nPress any key to continue...")
        with self.input_handler:
            self.input_handler.wait_for_key()

        # Ask if player wants to play again
        self._ask_play_again()

    def _ask_play_again(self):
        """Ask player if they want to play again"""
        while True:
            self.display.clear_screen()
            print("🐍 SNAKE GAME 🐍")
            print("=" * 50)
            print()
            print("Would you like to play again?")
            print()
            print("Y - Play Again")
            print("N - Quit")
            print("I - View Instructions")
            print()
            print("=" * 50)

            with self.input_handler:
                key = self.input_handler.wait_for_key()

            if key == "y":
                if self._start_new_game():
                    self._game_loop()
                break
            elif key == "n" or key == "q":
                self.running = False
                break
            elif key == "i":
                self._show_instructions()

    def _handle_exit(self):
        """Handle clean exit"""
        self.display.clear_screen()
        print("\n🐍 Thanks for playing Snake Game! 🐍")
        print("Goodbye!")


def main():
    """Main function for running the game"""
    print("🐍 Snake Game Initializing... 🐍")

    # Game settings
    game_width = 30
    game_height = 15

    # Create and run game
    game = SnakeGame(game_width, game_height)
    game.run()


if __name__ == "__main__":
    main()
