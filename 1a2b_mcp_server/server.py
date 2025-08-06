#!/usr/bin/env python3
"""
1A2B Number Guessing Game MCP Server

A MCP server that wraps the existing 1A2B CLI game,
providing remote access via MCP tools while keeping
the original CLI functionality intact.
"""

import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# 添加原游戏目录到Python路径
current_dir = Path(__file__).parent
game_dir = current_dir.parent / "1a2b_mcp"
sys.path.insert(0, str(game_dir))

# 导入原有游戏组件
from game.game_engine import GameState
from game.validator import InputValidator

# 初始化MCP服务器
mcp = FastMCP("1a2b-game-server")


class Game1A2BServer:
    """1A2B游戏MCP服务器包装器"""

    def __init__(self):
        self.current_game: Optional[GameState] = None
        self.validator = InputValidator()

    def _ensure_game_exists(self):
        """确保有活跃的游戏会话"""
        if self.current_game is None:
            raise ValueError("没有活跃的游戏！请先使用 start_game 开始新游戏")

    def start_new_game(self):
        """开始新游戏"""
        self.current_game = GameState()
        return True


# 全局游戏服务器实例
game_server = Game1A2BServer()


@mcp.tool()
async def start_game() -> str:
    """开始一个新的1A2B猜数字游戏

    注意：开始新游戏会自动结束当前进行中的游戏

    Returns:
        游戏开始信息和规则说明
    """
    game_server.start_new_game()

    return """🎯 1A2B猜数字游戏已开始！

游戏规则：
- 请猜一个4位不重复数字（0-9）
- A = 数字和位置都正确的个数  
- B = 数字正确但位置错误的个数
- 目标是获得 4A0B（完全正确）

示例：
- 如果答案是 1234，你猜 1672 → 1A1B
- 1在正确位置(A)，2存在但位置错误(B)

现在开始猜测吧！使用 make_guess 工具提交你的猜测。"""


@mcp.tool()
async def make_guess(guess: str) -> str:
    """提交一个4位数字猜测

    Args:
        guess: 4位不重复数字（如"1234"）

    Returns:
        猜测反馈结果
    """
    try:
        game_server._ensure_game_exists()

        # 使用原有验证逻辑
        validation_result = game_server.validator.validate_guess(guess)
        is_valid, cleaned_guess, error_message = validation_result

        if not is_valid:
            return f"❌ 输入错误: {error_message}"

        # 使用原有游戏逻辑处理猜测
        feedback = game_server.current_game.make_guess(cleaned_guess)

        # 格式化返回结果
        result = f"🎯 猜测: {cleaned_guess} → {feedback}"

        if game_server.current_game.is_won:
            attempts = game_server.current_game.attempt_count
            result += f"\n\n🎉 恭喜！您用 {attempts} 次猜对了！"

            # 根据尝试次数给出评价（复用原有逻辑）
            if attempts <= 5:
                result += "\n🌟 太棒了！您是猜数字高手！"
            elif attempts <= 8:
                result += "\n👍 很不错的表现！"
            elif attempts <= 12:
                result += "\n✅ 不错，继续努力！"
            else:
                result += "\n💪 虽然用了很多次，但坚持就是胜利！"
        else:
            result += f"\n📊 当前尝试次数: {game_server.current_game.attempt_count}"

        return result

    except Exception as e:
        return f"❌ 错误: {str(e)}"


@mcp.tool()
async def get_game_status() -> str:
    """获取当前游戏的状态信息

    Returns:
        当前游戏状态、尝试次数、历史记录等
    """
    try:
        game_server._ensure_game_exists()
        game = game_server.current_game

        status = """📊 游戏状态报告
        
🎮 游戏状态: {} 
🔢 尝试次数: {}
📝 猜测历史数量: {}

""".format(
            "已结束 🎉" if game.is_won else "进行中 🎯",
            game.attempt_count,
            len(game.guesses),
        )

        if game.is_won:
            status += f"🏆 谜底: {game.secret}\n"

        return status

    except Exception as e:
        return f"❌ 错误: {str(e)}"


@mcp.tool()
async def show_history() -> str:
    """显示当前游戏的所有猜测历史

    Returns:
        格式化的猜测历史记录
    """
    try:
        game_server._ensure_game_exists()
        game = game_server.current_game

        if not game.guesses:
            return "📝 还没有任何猜测记录"

        history = "📋 猜测历史记录:\n\n"
        history += "序号 | 猜测 | 反馈\n"
        history += "-----|------|-----\n"

        for i, (guess, feedback) in enumerate(game.guesses, 1):
            history += f" {i:2d}  | {guess} | {feedback}\n"

        return history

    except Exception as e:
        return f"❌ 错误: {str(e)}"


@mcp.tool()
async def reveal_answer() -> str:
    """揭示当前游戏的答案并结束游戏

    Returns:
        游戏答案和统计信息
    """
    try:
        game_server._ensure_game_exists()
        game = game_server.current_game

        result = f"""🔍 答案揭示

🏆 正确答案: {game.secret}
🔢 尝试次数: {game.attempt_count}
📊 猜测历史: {len(game.guesses)} 次

游戏已结束。使用 start_game 开始新游戏。"""

        return result

    except Exception as e:
        return f"❌ 错误: {str(e)}"


def main():
    """主入口点"""
    mcp.run()


if __name__ == "__main__":
    main()
