"""
Level Management for Snake Game
Defines level progression, speeds, and obstacles
"""

from typing import List, Tuple


class LevelManager:
    """Manages game levels, speeds, and obstacles"""

    def __init__(self):
        """Initialize level configurations"""
        # Speed decreases (faster) as level increases
        self.level_speeds = {
            1: 0.4,  # Slow start
            2: 0.35,  # Slightly faster
            3: 0.3,  # Medium speed
            4: 0.25,  # Getting faster
            5: 0.2,  # Fast
            6: 0.18,  # Very fast
            7: 0.15,  # Challenging
            8: 0.12,  # Expert
            9: 0.1,  # Master
            10: 0.08,  # Lightning fast
        }

    def get_level_speed(self, level: int) -> float:
        """Get movement delay for given level"""
        if level in self.level_speeds:
            return self.level_speeds[level]
        # For levels beyond 10, keep getting faster
        return max(0.05, 0.08 - (level - 10) * 0.005)

    def get_level_obstacles(
        self, level: int, width: int, height: int
    ) -> List[Tuple[int, int]]:
        """Generate obstacles for given level"""
        obstacles = []

        if level == 1:
            # Level 1: No obstacles, just walls
            pass

        elif level == 2:
            # Level 2: Simple central cross
            mid_x, mid_y = width // 2, height // 2
            # Vertical line
            for y in range(mid_y - 2, mid_y + 3):
                if 0 < y < height - 1:
                    obstacles.append((mid_x, y))
            # Horizontal line
            for x in range(mid_x - 3, mid_x + 4):
                if 0 < x < width - 1 and (x, mid_y) not in obstacles:
                    obstacles.append((x, mid_y))

        elif level == 3:
            # Level 3: Corner blocks
            # Top-left corner
            for x in range(3, 8):
                for y in range(3, 6):
                    obstacles.append((x, y))
            # Bottom-right corner
            for x in range(width - 8, width - 3):
                for y in range(height - 6, height - 3):
                    obstacles.append((x, y))

        elif level == 4:
            # Level 4: Maze-like corridors
            # Create some walls to form corridors
            for y in range(4, height - 4):
                if y % 4 == 0:
                    for x in range(4, width - 10):
                        obstacles.append((x, y))
                    for x in range(width - 6, width - 4):
                        obstacles.append((x, y))

        elif level == 5:
            # Level 5: Spiral pattern
            center_x, center_y = width // 2, height // 2
            # Create a spiral of obstacles
            for r in range(1, 4):
                for angle in range(0, 360, 30):
                    import math

                    x = center_x + int(r * math.cos(math.radians(angle)))
                    y = center_y + int(r * math.sin(math.radians(angle)))
                    if 1 < x < width - 2 and 1 < y < height - 2:
                        obstacles.append((x, y))

        elif level == 6:
            # Level 6: Border obstacles
            # Add obstacles near borders
            for x in range(3, width - 3):
                obstacles.append((x, 3))
                obstacles.append((x, height - 4))
            for y in range(3, height - 3):
                obstacles.append((3, y))
                obstacles.append((width - 4, y))

        elif level == 7:
            # Level 7: Random scattered obstacles
            import random

            random.seed(42)  # Consistent obstacles
            for _ in range(min(20, (width * height) // 20)):
                x = random.randint(4, width - 5)
                y = random.randint(4, height - 5)
                obstacles.append((x, y))

        elif level == 8:
            # Level 8: Diamond pattern
            center_x, center_y = width // 2, height // 2
            size = min(width, height) // 4
            for x in range(center_x - size, center_x + size + 1):
                for y in range(center_y - size, center_y + size + 1):
                    if abs(x - center_x) + abs(y - center_y) == size:
                        if 1 < x < width - 2 and 1 < y < height - 2:
                            obstacles.append((x, y))

        elif level == 9:
            # Level 9: Complex maze
            # Create a more complex maze pattern
            for x in range(5, width - 5, 3):
                for y in range(2, height - 2):
                    if y % 4 != 0:
                        obstacles.append((x, y))
            for y in range(5, height - 5, 3):
                for x in range(2, width - 2):
                    if x % 4 != 0:
                        obstacles.append((x, y))

        elif level >= 10:
            # Level 10+: Increasingly complex patterns
            import random

            random.seed(level)  # Different seed for each level

            # Combination of previous patterns
            center_x, center_y = width // 2, height // 2

            # Central cross
            for i in range(-2, 3):
                if 1 < center_x + i < width - 2:
                    obstacles.append((center_x + i, center_y))
                if 1 < center_y + i < height - 2:
                    obstacles.append((center_x, center_y + i))

            # Random scattered obstacles
            num_obstacles = min(30 + level, (width * height) // 15)
            for _ in range(num_obstacles):
                x = random.randint(3, width - 4)
                y = random.randint(3, height - 4)
                if (x, y) not in obstacles:
                    obstacles.append((x, y))

        return obstacles

    def get_level_description(self, level: int) -> str:
        """Get description for given level"""
        descriptions = {
            1: "Open Field - Learn the basics",
            2: "Cross Roads - Navigate around obstacles",
            3: "Corner Blocks - Use the corners wisely",
            4: "Corridors - Find your path through",
            5: "Spiral Challenge - Navigate the spiral",
            6: "Border Patrol - Avoid the border obstacles",
            7: "Scattered Chaos - Random obstacles everywhere",
            8: "Diamond Mine - Navigate the diamond pattern",
            9: "Complex Maze - Advanced navigation required",
            10: "Master Challenge - Ultimate test of skill",
        }

        if level in descriptions:
            return descriptions[level]
        return f"Expert Level {level} - Maximum difficulty!"

    def get_max_level(self) -> int:
        """Get maximum supported level"""
        return 10

    def is_final_level(self, level: int) -> bool:
        """Check if this is the final level"""
        return level >= self.get_max_level()
