#!/usr/bin/env python3
"""
迷宫游戏 - CLI版本
玩家可以选择迷宫大小，通过WASD键控制角色移动
"""

import random
import os
import sys
from typing import List, Tuple, Optional

# 只在非Windows系统导入termios和tty
if os.name != "nt":
    try:
        import tty
        import termios
    except ImportError:
        pass


class MazeGame:
    def __init__(self):
        self.maze = []
        self.width = 0
        self.height = 0
        self.player_pos = [1, 1]  # [row, col]
        self.start_pos = [1, 1]
        self.end_pos = [0, 0]

        # 迷宫符号
        self.WALL = "█"
        self.PATH = " "
        self.PLAYER = "●"
        self.START = "S"
        self.END = "E"

    def clear_screen(self):
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")

    def get_char(self):
        """获取单个字符输入（无需回车）"""
        if os.name == "nt":  # Windows
            try:
                import msvcrt

                return msvcrt.getch().decode("utf-8").lower()
            except ImportError:
                # 如果msvcrt不可用，使用常规输入
                return input("请输入命令 (w/a/s/d/q): ").lower()
        else:  # Unix/Linux/Mac
            try:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.cbreak(fd)
                    ch = sys.stdin.read(1).lower()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
            except (ImportError, NameError):
                # 如果termios/tty不可用，使用常规输入
                return input("请输入命令 (w/a/s/d/q): ").lower()

    def generate_maze(self, width: int, height: int):
        """生成迷宫使用递归回溯算法"""
        # 确保宽度和高度为奇数
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1

        # 初始化迷宫，全部为墙
        self.maze = [[self.WALL for _ in range(self.width)] for _ in range(self.height)]

        # 开始位置
        start_row, start_col = 1, 1
        self.maze[start_row][start_col] = self.PATH
        self.start_pos = [start_row, start_col]
        self.player_pos = [start_row, start_col]

        # 递归回溯生成迷宫
        self._carve_path(start_row, start_col)

        # 设置终点（右下角）
        self.end_pos = [self.height - 2, self.width - 2]
        self.maze[self.end_pos[0]][self.end_pos[1]] = self.PATH

    def _carve_path(self, row: int, col: int):
        """递归雕刻路径"""
        # 四个方向：上、右、下、左
        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # 检查新位置是否在边界内且为墙
            if (
                0 < new_row < self.height - 1
                and 0 < new_col < self.width - 1
                and self.maze[new_row][new_col] == self.WALL
            ):

                # 雕刻路径
                self.maze[new_row][new_col] = self.PATH
                self.maze[row + dr // 2][col + dc // 2] = self.PATH

                # 递归
                self._carve_path(new_row, new_col)

    def display_maze(self):
        """显示迷宫"""
        self.clear_screen()
        print("迷宫游戏 - 使用 WASD 移动，Q 退出")
        print("-" * (self.width + 2))

        for i, row in enumerate(self.maze):
            line = "|"
            for j, cell in enumerate(row):
                if [i, j] == self.player_pos:
                    line += self.PLAYER
                elif [i, j] == self.start_pos:
                    line += self.START if [i, j] != self.player_pos else self.PLAYER
                elif [i, j] == self.end_pos:
                    line += self.END if [i, j] != self.player_pos else self.PLAYER
                else:
                    line += cell
            line += "|"
            print(line)

        print("-" * (self.width + 2))
        print(f"位置: ({self.player_pos[0]}, {self.player_pos[1]})")
        print("目标: 到达右下角的 E")

    def is_valid_move(self, row: int, col: int) -> bool:
        """检查移动是否有效"""
        return (
            0 <= row < self.height
            and 0 <= col < self.width
            and self.maze[row][col] != self.WALL
        )

    def move_player(self, direction: str) -> bool:
        """移动玩家"""
        row, col = self.player_pos

        if direction == "w":  # 上
            new_row, new_col = row - 1, col
        elif direction == "s":  # 下
            new_row, new_col = row + 1, col
        elif direction == "a":  # 左
            new_row, new_col = row, col - 1
        elif direction == "d":  # 右
            new_row, new_col = row, col + 1
        else:
            return False

        if self.is_valid_move(new_row, new_col):
            self.player_pos = [new_row, new_col]
            return True
        return False

    def is_game_won(self) -> bool:
        """检查是否获胜"""
        return self.player_pos == self.end_pos

    def get_maze_size(self) -> Tuple[int, int]:
        """获取用户输入的迷宫大小"""
        while True:
            try:
                print("选择迷宫大小:")
                print("1. 小 (11x11)")
                print("2. 中 (21x21)")
                print("3. 大 (31x31)")
                print("4. 自定义大小")

                choice = input("请选择 (1-4): ").strip()

                if choice == "1":
                    return 11, 11
                elif choice == "2":
                    return 21, 21
                elif choice == "3":
                    return 31, 31
                elif choice == "4":
                    width = int(input("输入宽度 (最小5): "))
                    height = int(input("输入高度 (最小5): "))
                    if width < 5 or height < 5:
                        print("大小太小！请重新输入。")
                        continue
                    return width, height
                else:
                    print("无效选择，请重新输入。")
            except ValueError:
                print("请输入有效数字。")

    def play(self):
        """主游戏循环"""
        self.clear_screen()
        print("欢迎来到迷宫游戏！")
        print()

        # 获取迷宫大小
        width, height = self.get_maze_size()

        # 生成迷宫
        print("正在生成迷宫...")
        self.generate_maze(width, height)

        # 游戏主循环
        while True:
            self.display_maze()

            # 检查是否获胜
            if self.is_game_won():
                print("\n🎉 恭喜！您成功走出了迷宫！")
                break

            print("\n控制: W(上) A(左) S(下) D(右) Q(退出)")

            try:
                key = self.get_char()

                if key == "q":
                    print("\n感谢游玩！")
                    break
                elif key in ["w", "a", "s", "d"]:
                    if not self.move_player(key):
                        # 可以添加撞墙音效或提示
                        pass
                elif key == "\x03":  # Ctrl+C
                    break
            except KeyboardInterrupt:
                print("\n\n游戏被中断。")
                break
            except:
                pass  # 忽略其他按键


def main():
    """主函数"""
    game = MazeGame()
    try:
        game.play()
    except KeyboardInterrupt:
        print("\n\n游戏结束。")
    except Exception as e:
        print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()
