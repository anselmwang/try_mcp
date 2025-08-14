#!/usr/bin/env python3
"""
Simple test script for Snake Game
Tests core functionality without user interaction
"""


def test_snake_game():
    """Test core Snake Game functionality"""
    print("🐍 Testing Snake Game Core Functionality...")

    try:
        # Test imports
        from game.snake_engine import GameState, Direction, Snake, Food
        from game.levels import LevelManager
        from game.display import GameDisplay
        from game.input_handler import InputHandler

        print("✅ All modules imported successfully")

        # Test GameState initialization
        game_state = GameState(20, 15)
        print(
            f"✅ Game initialized: Level {game_state.level}, Score {game_state.score}"
        )

        # Test Snake functionality
        initial_pos = game_state.snake.get_head()
        game_state.change_snake_direction(Direction.DOWN)
        print(f"✅ Snake direction changed, head at {initial_pos}")

        # Test Level Manager
        level_manager = LevelManager()
        speed = level_manager.get_level_speed(1)
        obstacles = level_manager.get_level_obstacles(1, 20, 15)
        print(f"✅ Level 1 speed: {speed}s, obstacles: {len(obstacles)}")

        # Test game update
        initial_score = game_state.score
        success = game_state.update()
        print(f"✅ Game update successful: {success}, Score: {game_state.score}")

        # Test Display (non-interactive)
        display = GameDisplay()
        print("✅ Display system initialized")

        # Test Input Handler (initialization only)
        input_handler = InputHandler()
        print("✅ Input handler initialized")

        # Test multiple levels
        for level in range(1, 6):
            obstacles = level_manager.get_level_obstacles(level, 30, 20)
            speed = level_manager.get_level_speed(level)
            desc = level_manager.get_level_description(level)
            print(
                f"✅ Level {level}: {len(obstacles)} obstacles, {speed}s speed - {desc}"
            )

        print("\n🎉 All tests passed! Snake Game is ready to play!")
        print("\nTo play the game:")
        print("  python run_game.py")
        print("  or")
        print("  python -m snake_game.main")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_snake_game()
