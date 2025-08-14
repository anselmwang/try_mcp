"""
Snake Game Engine - Core game logic and classes
"""

import random
from typing import List, Tuple
from enum import Enum


class Direction(Enum):
    """Direction enumeration for snake movement"""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """Snake class managing position, movement, and growth"""

    def __init__(self, start_x: int, start_y: int):
        """Initialize snake at starting position"""
        self.body = [(start_x, start_y)]
        self.direction = Direction.RIGHT
        self.grow_pending = False

    def move(self) -> Tuple[int, int]:
        """Move snake in current direction and return new head position"""
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow_pending:
            self.body.pop()  # Remove tail if not growing
        else:
            self.grow_pending = False

        return new_head

    def change_direction(self, new_direction: Direction):
        """Change snake direction if not opposite to current direction"""
        # Prevent reversing into itself
        if self.direction == Direction.UP and new_direction == Direction.DOWN:
            return
        if self.direction == Direction.DOWN and new_direction == Direction.UP:
            return
        if self.direction == Direction.LEFT and new_direction == Direction.RIGHT:
            return
        if self.direction == Direction.RIGHT and new_direction == Direction.LEFT:
            return

        self.direction = new_direction

    def grow(self):
        """Mark snake to grow on next move"""
        self.grow_pending = True

    def check_self_collision(self) -> bool:
        """Check if snake head collides with its body"""
        head = self.body[0]
        return head in self.body[1:]

    def get_head(self) -> Tuple[int, int]:
        """Get snake head position"""
        return self.body[0]

    def get_body(self) -> List[Tuple[int, int]]:
        """Get full snake body positions"""
        return self.body.copy()


class Food:
    """Food class for snake to eat"""

    def __init__(
        self, width: int, height: int, obstacles: List[Tuple[int, int]] = None
    ):
        """Initialize food with game boundaries"""
        self.width = width
        self.height = height
        self.obstacles = obstacles or []
        self.position = self._generate_position()

    def _generate_position(self) -> Tuple[int, int]:
        """Generate random food position avoiding obstacles"""
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in self.obstacles:
                return (x, y)

    def regenerate(self, snake_body: List[Tuple[int, int]]):
        """Generate new food position avoiding snake and obstacles"""
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            pos = (x, y)
            if pos not in snake_body and pos not in self.obstacles:
                self.position = pos
                break

    def get_position(self) -> Tuple[int, int]:
        """Get current food position"""
        return self.position


class GameState:
    """Manages overall game state, scoring, and level progression"""

    def __init__(self, width: int = 30, height: int = 20):
        """Initialize game state"""
        self.width = width
        self.height = height
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.foods_per_level = 5
        self.game_over = False
        self.game_won = False
        self.max_level = 10

        # Initialize snake and food
        start_x = width // 2
        start_y = height // 2
        self.snake = Snake(start_x, start_y)

        # Get obstacles for current level
        from .levels import LevelManager

        self.level_manager = LevelManager()
        obstacles = self.level_manager.get_level_obstacles(self.level, width, height)
        self.food = Food(width, height, obstacles)

        # Ensure food doesn't spawn on snake
        self.food.regenerate(self.snake.get_body())

    def update(self) -> bool:
        """Update game state, return False if game over"""
        if self.game_over or self.game_won:
            return False

        # Move snake
        new_head = self.snake.move()

        # Check wall collision
        if (
            new_head[0] <= 0
            or new_head[0] >= self.width - 1
            or new_head[1] <= 0
            or new_head[1] >= self.height - 1
        ):
            self.game_over = True
            return False

        # Check obstacle collision
        obstacles = self.level_manager.get_level_obstacles(
            self.level, self.width, self.height
        )
        if new_head in obstacles:
            self.game_over = True
            return False

        # Check self collision
        if self.snake.check_self_collision():
            self.game_over = True
            return False

        # Check food collision
        if new_head == self.food.get_position():
            self.snake.grow()
            self.score += 10
            self.foods_eaten += 1
            self.food.regenerate(self.snake.get_body())

            # Check level completion
            if self.foods_eaten >= self.foods_per_level:
                self._advance_level()

        return True

    def _advance_level(self):
        """Advance to next level"""
        if self.level >= self.max_level:
            self.game_won = True
            return

        self.level += 1
        self.foods_eaten = 0
        self.score += 50  # Level completion bonus

        # Update food with new level obstacles
        obstacles = self.level_manager.get_level_obstacles(
            self.level, self.width, self.height
        )
        self.food.obstacles = obstacles
        self.food.regenerate(self.snake.get_body())

    def change_snake_direction(self, direction: Direction):
        """Change snake direction"""
        self.snake.change_direction(direction)

    def get_speed(self) -> float:
        """Get current game speed (delay between moves)"""
        return self.level_manager.get_level_speed(self.level)

    def get_obstacles(self) -> List[Tuple[int, int]]:
        """Get current level obstacles"""
        return self.level_manager.get_level_obstacles(
            self.level, self.width, self.height
        )

    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.game_over

    def is_game_won(self) -> bool:
        """Check if game is won"""
        return self.game_won

    def get_progress(self) -> str:
        """Get level progress string"""
        return f"Level {self.level} - Food: {self.foods_eaten}/{self.foods_per_level}"
