"""
Game Engine for 1A2B Number Guessing Game

Contains the core game logic including secret generation,
guess validation, and feedback calculation.
"""

import random
from typing import List, Tuple, Dict


class SecretGenerator:
    """Generates secret numbers for the game."""

    @staticmethod
    def generate_secret() -> str:
        """
        Generate a 4-digit secret number with unique digits.

        Returns:
            str: A 4-digit string with unique digits
        """
        digits = list(range(10))  # 0-9
        secret_digits = random.sample(digits, 4)
        return "".join(map(str, secret_digits))


class GameLogic:
    """Handles game logic and feedback calculation."""

    @staticmethod
    def calculate_feedback(secret: str, guess: str) -> str:
        """
        Calculate the XA YB feedback for a guess.

        Args:
            secret: The secret 4-digit number
            guess: The player's guess

        Returns:
            str: Feedback in "XA YB" format
        """
        if len(secret) != 4 or len(guess) != 4:
            raise ValueError("Both secret and guess must be 4 digits")

        # Calculate A (Bulls) - correct digit in correct position
        bulls = sum(1 for i in range(4) if secret[i] == guess[i])

        # Calculate B (Cows) - correct digit in wrong position
        secret_counts: Dict[str, int] = {}
        guess_counts: Dict[str, int] = {}

        # Count digits in both secret and guess (excluding bulls)
        for i in range(4):
            if secret[i] != guess[i]:  # Don't count bulls
                secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1
                guess_counts[guess[i]] = guess_counts.get(guess[i], 0) + 1

        # Calculate cows by finding common digits
        cows = 0
        for digit in guess_counts:
            if digit in secret_counts:
                cows += min(secret_counts[digit], guess_counts[digit])

        return f"{bulls}A{cows}B"

    @staticmethod
    def is_winning_guess(feedback: str) -> bool:
        """
        Check if the feedback indicates a winning guess.

        Args:
            feedback: The feedback string (e.g., "4A0B")

        Returns:
            bool: True if the guess is correct (4A0B)
        """
        return feedback == "4A0B"


class GameState:
    """Manages the state of a single game session."""

    def __init__(self):
        """Initialize a new game state."""
        self.secret = SecretGenerator.generate_secret()
        self.guesses: List[Tuple[str, str]] = []  # (guess, feedback)
        self.attempt_count = 0
        self.is_won = False

    def make_guess(self, guess: str) -> str:
        """
        Process a player's guess and return feedback.

        Args:
            guess: The player's 4-digit guess

        Returns:
            str: Feedback in "XA YB" format
        """
        self.attempt_count += 1
        feedback = GameLogic.calculate_feedback(self.secret, guess)
        self.guesses.append((guess, feedback))

        if GameLogic.is_winning_guess(feedback):
            self.is_won = True

        return feedback

    def get_game_history(self) -> List[Tuple[str, str]]:
        """
        Get the history of guesses and feedback.

        Returns:
            List[Tuple[str, str]]: List of (guess, feedback) tuples
        """
        return self.guesses.copy()

    def reset_game(self):
        """Reset the game state for a new game."""
        self.secret = SecretGenerator.generate_secret()
        self.guesses = []
        self.attempt_count = 0
        self.is_won = False
