"""
Display and UI management for Snake Game
"""

import os
from typing import List, Tuple
from .snake_engine import GameState, Direction


class GameDisplay:
    """Handles game rendering and display"""

    def __init__(self):
        """Initialize display settings"""
        # Display characters
        self.WALL = "█"
        self.SNAKE_HEAD = "●"
        self.SNAKE_BODY = "○"
        self.FOOD = "@"
        self.OBSTACLE = "■"
        self.EMPTY = " "

        # Colors (if terminal supports them)
        self.RESET = "\033[0m"
        self.GREEN = "\033[92m"
        self.RED = "\033[91m"
        self.YELLOW = "\033[93m"
        self.BLUE = "\033[94m"
        self.CYAN = "\033[96m"

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def render_game(self, game_state: GameState):
        """Render the complete game screen"""
        self.clear_screen()

        # Game title and info
        print("🐍 SNAKE GAME 🐍")
        print("=" * 50)

        # Game stats
        score_text = f"Score: {game_state.score}"
        progress_text = game_state.get_progress()
        speed_text = f"Speed: {game_state.get_speed():.2f}s"

        print(f"{score_text:<20} {progress_text:<20} {speed_text}")
        print("-" * 50)

        # Level description
        level_desc = game_state.level_manager.get_level_description(game_state.level)
        print(f"Level {game_state.level}: {level_desc}")
        print()

        # Game field
        self._render_field(game_state)

        # Controls
        print()
        print("Controls: W/↑(Up) A/←(Left) S/↓(Down) D/→(Right) P(Pause) Q(Quit)")

    def _render_field(self, game_state: GameState):
        """Render the game field"""
        width = game_state.width
        height = game_state.height
        snake_body = game_state.snake.get_body()
        snake_head = game_state.snake.get_head()
        food_pos = game_state.food.get_position()
        obstacles = game_state.get_obstacles()

        # Top border
        print("+" + self.WALL * width + "+")

        # Game field rows
        for y in range(height):
            row = "|"
            for x in range(width):
                pos = (x, y)

                # Determine what to display at this position
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    # Border walls
                    char = self.WALL
                elif pos == snake_head:
                    # Snake head
                    char = self._colored_char(self.SNAKE_HEAD, self.GREEN)
                elif pos in snake_body[1:]:
                    # Snake body
                    char = self._colored_char(self.SNAKE_BODY, self.GREEN)
                elif pos == food_pos:
                    # Food
                    char = self._colored_char(self.FOOD, self.RED)
                elif pos in obstacles:
                    # Obstacles
                    char = self._colored_char(self.OBSTACLE, self.BLUE)
                else:
                    # Empty space
                    char = self.EMPTY

                row += char

            row += "|"
            print(row)

        # Bottom border
        print("+" + self.WALL * width + "+")

    def _colored_char(self, char: str, color: str) -> str:
        """Return colored character if terminal supports it"""
        try:
            return f"{color}{char}{self.RESET}"
        except:
            return char

    def show_game_over(self, game_state: GameState):
        """Display game over screen"""
        self.clear_screen()

        print("🐍 SNAKE GAME 🐍")
        print("=" * 50)
        print()

        if game_state.is_game_won():
            print("🎉 CONGRATULATIONS! 🎉")
            print("You completed all levels!")
        else:
            print("💀 GAME OVER 💀")
            if game_state.snake.check_self_collision():
                print("You bit yourself!")
            else:
                print("You hit a wall or obstacle!")

        print()
        print(f"Final Score: {game_state.score}")
        print(f"Level Reached: {game_state.level}")
        print(
            f"Total Food Eaten: {game_state.foods_eaten + (game_state.level - 1) * game_state.foods_per_level}"
        )

        if game_state.level > 1:
            print(f"Levels Completed: {game_state.level - 1}")

        print()
        print("=" * 50)

    def show_pause_screen(self, game_state: GameState):
        """Display pause screen"""
        self.clear_screen()

        print("🐍 SNAKE GAME - PAUSED 🐍")
        print("=" * 50)
        print()

        print(f"Score: {game_state.score}")
        print(f"Level: {game_state.level}")
        print(f"Progress: {game_state.foods_eaten}/{game_state.foods_per_level}")

        print()
        print("Game is paused.")
        print("Press P to resume, Q to quit")
        print()
        print("=" * 50)

    def show_level_complete(self, game_state: GameState):
        """Display level completion screen"""
        self.clear_screen()

        print("🐍 SNAKE GAME 🐍")
        print("=" * 50)
        print()

        print("🎉 LEVEL COMPLETE! 🎉")
        print()
        print(f"Level {game_state.level - 1} completed!")
        print(f"Score: {game_state.score}")
        print(f"Bonus: +50 points")

        print()

        if game_state.level <= game_state.level_manager.get_max_level():
            next_desc = game_state.level_manager.get_level_description(game_state.level)
            print(f"Next: Level {game_state.level}")
            print(f"{next_desc}")
            print()
            print("Press any key to continue...")
        else:
            print("🏆 ALL LEVELS COMPLETED! 🏆")
            print("You are a Snake Master!")

        print()
        print("=" * 50)

    def show_start_screen(self):
        """Display game start screen"""
        self.clear_screen()

        print("🐍 SNAKE GAME 🐍")
        print("=" * 50)
        print()
        print("Welcome to Snake Game!")
        print()
        print("How to Play:")
        print("• Control the snake with W/A/S/D or arrow keys")
        print("• Eat food (@) to grow and score points")
        print("• Avoid walls, obstacles, and your own tail")
        print("• Complete levels by eating enough food")
        print("• Each level gets faster with new obstacles")
        print()
        print("Features:")
        print("• 10 levels with increasing difficulty")
        print("• Progressive speed increases")
        print("• Unique obstacles for each level")
        print("• Score system with level completion bonuses")
        print()
        print("Controls:")
        print("  W or ↑  - Move Up")
        print("  A or ←  - Move Left")
        print("  S or ↓  - Move Down")
        print("  D or →  - Move Right")
        print("  P       - Pause Game")
        print("  Q       - Quit Game")
        print()
        print("=" * 50)
        print("Press any key to start...")

    def show_instructions(self):
        """Show detailed instructions"""
        self.clear_screen()

        print("🐍 SNAKE GAME - INSTRUCTIONS 🐍")
        print("=" * 50)
        print()
        print("OBJECTIVE:")
        print("Guide your snake to eat food and grow while avoiding obstacles.")
        print("Complete all 10 levels to win the game!")
        print()
        print("SCORING:")
        print("• Food eaten: +10 points each")
        print("• Level completion: +50 bonus points")
        print("• Survive as long as possible!")
        print()
        print("LEVEL PROGRESSION:")
        print("Level 1: Open Field - Learn the basics")
        print("Level 2: Cross Roads - Navigate around obstacles")
        print("Level 3: Corner Blocks - Use the corners wisely")
        print("Level 4: Corridors - Find your path through")
        print("Level 5: Spiral Challenge - Navigate the spiral")
        print("Level 6: Border Patrol - Avoid the border obstacles")
        print("Level 7: Scattered Chaos - Random obstacles everywhere")
        print("Level 8: Diamond Mine - Navigate the diamond pattern")
        print("Level 9: Complex Maze - Advanced navigation required")
        print("Level 10: Master Challenge - Ultimate test of skill")
        print()
        print("SYMBOLS:")
        print(f"  {self.SNAKE_HEAD}  - Snake Head")
        print(f"  {self.SNAKE_BODY}  - Snake Body")
        print(f"  {self.FOOD}  - Food")
        print(f"  {self.OBSTACLE}  - Obstacle")
        print(f"  {self.WALL}  - Wall")
        print()
        print("=" * 50)
        print("Press any key to return...")
