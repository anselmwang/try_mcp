#!/usr/bin/env python3
"""
Main entry point for 1A2B Number Guessing Game

A CLI-based Bulls and Cows number guessing game.
"""

import sys
from game.game_engine import GameState
from game.validator import InputValidator
from game.display import GameDisplay


class Game1A2B:
    """Main game controller for the 1A2B number guessing game."""

    def __init__(self):
        """Initialize the game."""
        self.game_state = GameState()
        self.validator = InputValidator()
        self.display = GameDisplay()

    def run(self):
        """Run the main game loop."""
        self.display.show_welcome()

        while True:
            self.play_single_game()

            # Ask if player wants to play again
            if not self.ask_play_again():
                break

        self.display.show_goodbye()

    def play_single_game(self):
        """Play a single game session."""
        self.game_state.reset_game()
        self.display.show_game_start()

        while not self.game_state.is_won:
            # Get player's guess
            guess = self.get_valid_guess()

            # Process the guess
            feedback = self.game_state.make_guess(guess)

            # Show feedback
            self.display.show_feedback(guess, feedback)

            # Check if game is won
            if self.game_state.is_won:
                self.display.show_victory(
                    self.game_state.attempt_count, self.game_state.secret
                )
            else:
                # Show game history every few attempts
                if self.game_state.attempt_count % 3 == 0:
                    history = self.game_state.get_game_history()
                    self.display.show_game_history(history)

    def get_valid_guess(self) -> str:
        """
        Get a valid guess from the player.

        Returns:
            str: A valid 4-digit guess
        """
        while True:
            try:
                prompt = self.display.show_guess_prompt(
                    self.game_state.attempt_count + 1
                )
                user_input = input(prompt)

                # Validate the input
                validation_result = self.validator.validate_guess(user_input)
                is_valid, cleaned_guess, error_message = validation_result

                if is_valid:
                    return cleaned_guess
                else:
                    self.display.show_error(error_message)

            except KeyboardInterrupt:
                print("\n\n👋 游戏被中断，再见！")
                sys.exit(0)
            except EOFError:
                print("\n\n👋 游戏结束，再见！")
                sys.exit(0)

    def ask_play_again(self) -> bool:
        """
        Ask the player if they want to play again.

        Returns:
            bool: True if player wants to play again
        """
        while True:
            try:
                prompt = self.display.show_play_again_prompt()
                user_input = input(prompt)

                validation_result = self.validator.validate_yes_no(user_input)
                is_valid, is_yes, error_message = validation_result

                if is_valid:
                    return is_yes
                else:
                    self.display.show_error(error_message)

            except KeyboardInterrupt:
                print("\n\n👋 游戏被中断，再见！")
                return False
            except EOFError:
                print("\n\n👋 游戏结束，再见！")
                return False


def main():
    """Main entry point."""
    try:
        game = Game1A2B()
        game.run()
    except Exception as e:
        print(f"\n❌ 游戏发生错误: {e}")
        print("🔧 请检查游戏文件是否完整")
        sys.exit(1)


if __name__ == "__main__":
    main()
