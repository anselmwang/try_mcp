"""
Input Validator for 1A2B Number Guessing Game

Handles validation of user input to ensure it meets game requirements.
"""

import re
from typing import Tuple


class InputValidator:
    """Validates user input for the 1A2B game."""

    @staticmethod
    def validate_guess(user_input: str) -> Tuple[bool, str, str]:
        """
        Validate a user's guess input.

        Args:
            user_input: The raw input from the user

        Returns:
            Tuple[bool, str, str]: (is_valid, cleaned_input, error_message)
                - is_valid: True if input is valid
                - cleaned_input: The cleaned 4-digit string (empty if invalid)
                - error_message: Error description (empty if valid)
        """
        # Clean the input - remove whitespace
        cleaned = user_input.strip()

        # Check if input is empty
        if not cleaned:
            return False, "", "输入不能为空，请输入4位数字"

        # Check if input contains only digits
        if not re.match(r"^\d+$", cleaned):
            return False, "", "输入只能包含数字，请输入4位数字"

        # Check if input is exactly 4 digits
        if len(cleaned) != 4:
            return False, "", f"输入必须是4位数字，您输入了{len(cleaned)}位"

        # Check for duplicate digits
        if len(set(cleaned)) != 4:
            return False, "", "4位数字不能重复，请输入4个不同的数字"

        return True, cleaned, ""

    @staticmethod
    def validate_yes_no(user_input: str) -> Tuple[bool, bool, str]:
        """
        Validate yes/no input from user.

        Args:
            user_input: The raw input from the user

        Returns:
            Tuple[bool, bool, str]: (is_valid, is_yes, error_message)
                - is_valid: True if input is valid
                - is_yes: True if user chose yes
                - error_message: Error description (empty if valid)
        """
        cleaned = user_input.strip().lower()

        if not cleaned:
            return False, False, "请输入 y/yes 或 n/no"

        yes_options = ["y", "yes", "是", "1"]
        no_options = ["n", "no", "否", "0"]

        if cleaned in yes_options:
            return True, True, ""
        elif cleaned in no_options:
            return True, False, ""
        else:
            return False, False, "请输入 y/yes 或 n/no"
