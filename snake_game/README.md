# Snake Game - CLI Version

A classic Snake game implemented in Python for the command line interface, featuring multiple levels with increasing difficulty and speed.

## Features

🐍 **Classic Snake Gameplay**
- Control a growing snake that eats food
- Avoid walls, obstacles, and your own tail
- Progressive difficulty with each level

🎮 **Multiple Levels**
- 10 unique levels with different obstacle patterns
- Each level introduces new challenges
- Increasing speed as you progress

⚡ **Progressive Difficulty**
- Speed increases with each level
- Unique obstacle layouts for each level
- Level completion bonuses

🎯 **Scoring System**
- 10 points per food eaten
- 50 bonus points for completing each level
- Track your high scores across sessions

## Installation

No additional dependencies required! The game uses only Python standard library modules.

```bash
# Clone or download the snake_game directory
cd snake_game

# Run the game
python run_game.py

# Or run directly
python -m snake_game.main
```

## How to Play

### Controls
- **W** or **↑** - Move Up
- **A** or **←** - Move Left  
- **S** or **↓** - Move Down
- **D** or **→** - Move Right
- **P** - Pause/Resume Game
- **Q** - Quit Game

### Objective
1. Control your snake to eat food (@) and grow
2. Avoid hitting walls, obstacles, or your own tail
3. Eat enough food to complete each level
4. Progress through all 10 levels to win!

### Game Elements
- `●` - Snake Head (Green)
- `○` - Snake Body (Green)
- `@` - Food (Red)
- `■` - Obstacles (Blue)
- `█` - Walls

## Level Progression

**Level 1: Open Field**
- Learn the basics with no obstacles
- Speed: 0.4 seconds per move

**Level 2: Cross Roads**
- Navigate around a central cross pattern
- Speed: 0.35 seconds per move

**Level 3: Corner Blocks**
- Use corners wisely to avoid blocks
- Speed: 0.3 seconds per move

**Level 4: Corridors**
- Find your path through corridor patterns
- Speed: 0.25 seconds per move

**Level 5: Spiral Challenge**
- Navigate around a spiral obstacle pattern
- Speed: 0.2 seconds per move

**Level 6: Border Patrol**
- Avoid obstacles near the borders
- Speed: 0.18 seconds per move

**Level 7: Scattered Chaos**
- Random obstacles scattered throughout
- Speed: 0.15 seconds per move

**Level 8: Diamond Mine**
- Navigate through a diamond-shaped pattern
- Speed: 0.12 seconds per move

**Level 9: Complex Maze**
- Advanced maze navigation required
- Speed: 0.1 seconds per move

**Level 10: Master Challenge**
- Ultimate test of skill and reflexes
- Speed: 0.08 seconds per move

## Project Structure

```
snake_game/
├── __init__.py          # Package initialization
├── main.py              # Main game controller and entry point
├── run_game.py          # Simple launcher script
├── README.md            # This file
└── game/
    ├── __init__.py      # Game package exports
    ├── snake_engine.py  # Core game logic (Snake, Food, GameState)
    ├── display.py       # Screen rendering and UI
    ├── input_handler.py # Cross-platform input handling
    └── levels.py        # Level configuration and progression
```

## Technical Features

### Cross-Platform Compatibility
- Works on Windows, macOS, and Linux
- Handles different terminal input methods
- Graceful fallback for missing libraries

### Robust Input Handling
- Non-blocking keyboard input
- Support for both WASD and arrow keys
- Proper cleanup of terminal settings

### Clean Architecture
- Modular design with separated concerns
- Easy to extend with new levels or features
- Well-documented code with type hints

## Customization

### Adding New Levels
Edit `game/levels.py` to add new obstacle patterns:

```python
def get_level_obstacles(self, level: int, width: int, height: int):
    # Add your custom level logic here
    if level == 11:
        # Your custom obstacle pattern
        pass
```

### Adjusting Difficulty
Modify speed settings in `game/levels.py`:

```python
self.level_speeds = {
    1: 0.5,  # Slower
    2: 0.4,  # Adjust as needed
    # ...
}
```

### Changing Game Size
Modify the game dimensions in `main.py`:

```python
game_width = 40   # Wider game field
game_height = 20  # Taller game field
```

## Troubleshooting

### Game doesn't respond to keys
- Make sure your terminal supports the required input methods
- Try running with Python 3.7 or higher
- On some systems, you may need to press Enter after each key

### Display issues
- Ensure your terminal supports Unicode characters
- Try adjusting your terminal's font size
- Some terminals may not display colors correctly

### Import errors
- Make sure you're running from the correct directory
- Verify Python path includes the snake_game module
- Try using `python -m snake_game.main` instead

## System Requirements

- Python 3.7 or higher
- Terminal/Command Prompt with keyboard input support
- No external dependencies required

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute improvements, new levels, or bug fixes:

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Have Fun!

Enjoy playing this classic Snake game! Try to beat all 10 levels and achieve the highest score possible. Good luck! 🐍
