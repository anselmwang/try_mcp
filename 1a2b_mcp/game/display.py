"""
Display Module for 1A2B Number Guessing Game

Handles all CLI output formatting and user interface elements.
"""

from typing import List, Tuple


class GameDisplay:
    """Handles CLI display and formatting for the game."""

    @staticmethod
    def show_welcome():
        """Display the game welcome screen and rules."""
        print("=" * 60)
        print("🎯 欢迎来到 1A2B 猜数字游戏！")
        print("=" * 60)
        print()
        print("📋 游戏规则：")
        print("• 电脑会生成一个由4个不重复数字组成的秘密数字")
        print("• 您需要猜出这个4位数字")
        print("• 每次猜测后，您会收到 XA YB 格式的提示：")
        print("  - A (公牛)：位置和数字都正确的个数")
        print("  - B (母牛)：数字正确但位置错误的个数")
        print("• 当您得到 4A0B 时，恭喜您猜对了！")
        print()
        print("📝 示例：")
        print("  如果谜底是 1234：")
        print("  • 猜 5678 → 0A0B (没有数字正确)")
        print("  • 猜 1672 → 1A1B (1在正确位置，2在错误位置)")
        print("  • 猜 1243 → 2A2B (1,4在正确位置，2,3在错误位置)")
        print("  • 猜 1234 → 4A0B (全部正确！)")
        print()
        print("🚀 让我们开始游戏吧！")
        print("-" * 60)

    @staticmethod
    def show_game_start():
        """Display game start message."""
        print("\n🎲 电脑已经想好了一个4位数字...")
        print("💭 请开始您的猜测吧！（输入4个不重复的数字）")
        print()

    @staticmethod
    def show_guess_prompt(attempt_number: int) -> str:
        """
        Display the guess input prompt.

        Args:
            attempt_number: Current attempt number

        Returns:
            str: The prompt message
        """
        return f"第 {attempt_number} 次猜测，请输入4位数字: "

    @staticmethod
    def show_feedback(guess: str, feedback: str):
        """
        Display feedback for a guess.

        Args:
            guess: The player's guess
            feedback: The feedback in XA YB format
        """
        print(f"🔍 您的猜测: {guess} → 结果: {feedback}")

    @staticmethod
    def show_error(error_message: str):
        """
        Display an error message.

        Args:
            error_message: The error message to display
        """
        print(f"❌ 错误: {error_message}")

    @staticmethod
    def show_game_history(history: List[Tuple[str, str]]):
        """
        Display the game history.

        Args:
            history: List of (guess, feedback) tuples
        """
        if not history:
            print("📋 暂无猜测记录")
            return

        print("\n📋 猜测历史：")
        print("-" * 30)
        for i, (guess, feedback) in enumerate(history, 1):
            print(f"{i:2d}. {guess} → {feedback}")
        print("-" * 30)

    @staticmethod
    def show_victory(attempt_count: int, secret: str):
        """
        Display victory message.

        Args:
            attempt_count: Number of attempts taken
            secret: The secret number that was guessed
        """
        print("\n🎉" + "=" * 50 + "🎉")
        print("🏆 恭喜您！猜对了！")
        print(f"🎯 谜底是: {secret}")
        print(f"📊 您总共用了 {attempt_count} 次猜测")

        # Give performance feedback
        if attempt_count <= 5:
            print("🌟 太棒了！您是猜数字高手！")
        elif attempt_count <= 8:
            print("👍 很不错的表现！")
        elif attempt_count <= 12:
            print("✅ 不错，继续努力！")
        else:
            print("💪 虽然用了很多次，但坚持就是胜利！")

        print("🎉" + "=" * 50 + "🎉")

    @staticmethod
    def show_play_again_prompt() -> str:
        """
        Display play again prompt.

        Returns:
            str: The prompt message
        """
        return "\n🔄 要再玩一局吗？(y/yes 或 n/no): "

    @staticmethod
    def show_goodbye():
        """Display goodbye message."""
        print("\n👋 感谢游玩 1A2B 猜数字游戏！")
        print("🎯 期待下次再见！")
        print("=" * 40)

    @staticmethod
    def clear_screen():
        """Clear the screen (optional feature)."""
        import os

        os.system("cls" if os.name == "nt" else "clear")
