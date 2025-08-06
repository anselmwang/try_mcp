# 1A2B Game MCP Server

A Model Context Protocol (MCP) server that wraps the existing 1A2B CLI game, providing remote access via MCP tools while keeping the original CLI functionality intact.

## 🎯 Overview

This MCP server provides a stateless interface to the 1A2B guessing game. It maintains a single game session and offers tools for game management and interaction.

## 🛠️ Available Tools

### 1. `start_game`
- **Description**: Start a new 1A2B guessing game session
- **Parameters**: None
- **Returns**: Game rules and welcome message
- **Note**: Starting a new game automatically ends any current game

### 2. `make_guess`
- **Description**: Submit a 4-digit guess
- **Parameters**: 
  - `guess` (string): 4-digit number with unique digits (e.g., "1234")
- **Returns**: Feedback in XA YB format, win status, and attempt count

### 3. `get_game_status`
- **Description**: Get current game status information
- **Parameters**: None
- **Returns**: Game state, attempt count, and history summary

### 4. `show_history`
- **Description**: Display all guesses and feedback for current game
- **Parameters**: None
- **Returns**: Formatted table of guess history

### 5. `reveal_answer`
- **Description**: Reveal the answer and end the current game
- **Parameters**: None
- **Returns**: Answer, statistics, and game summary

## 🎮 Game Rules

- Guess a 4-digit number with unique digits (0-9)
- **A (Bulls)**: Correct digit in correct position
- **B (Cows)**: Correct digit in wrong position
- Goal: Achieve 4A0B (all correct)

## 📁 Architecture

### Design Principles
- **Zero Intrusion**: Original CLI game code remains completely unchanged
- **Code Reuse**: MCP server directly imports and uses original game logic
- **Independent Deployment**: Both CLI and MCP server can be used independently

### File Structure
```
1a2b_mcp_server/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server implementation
└── README.md           # This documentation

1a2b_mcp/               # Original CLI game (unchanged)
├── main.py             # CLI entry point
├── game/               # Game logic modules
│   ├── __init__.py
│   ├── game_engine.py  # Core game logic
│   ├── validator.py    # Input validation
│   └── display.py      # CLI display
└── README.md
```

### Implementation Details
- **Path Management**: Dynamically adds original game directory to Python path
- **Session Management**: Single global game session with automatic reset
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Import Strategy**: Selective imports to minimize dependencies

## 🚀 Usage Examples

### Starting a Game
```python
# Use MCP tool: start_game()
# Returns: Game rules and welcome message
```

### Making Guesses
```python
# Use MCP tool: make_guess("1234")
# Returns: "🎯 猜测: 1234 → 1A2B\n📊 当前尝试次数: 1"
```

### Checking Status
```python
# Use MCP tool: get_game_status()
# Returns: Current game state and statistics
```

## ⚙️ Configuration

The MCP server is configured in the Cline MCP settings:

```json
{
  "mcpServers": {
    "1a2b-game-mcp": {
      "autoApprove": [],
      "disabled": false,
      "timeout": 60,
      "type": "stdio",
      "command": "c:/GitRoot/try_mcp/.venv/Scripts/python.exe",
      "args": ["1a2b_mcp_server/server.py"],
      "cwd": "c:/GitRoot/try_mcp"
    }
  }
}
```

## 🔧 Technical Features

### Compatibility
- **Original CLI**: `cd 1a2b_mcp && python main.py` continues to work unchanged
- **MCP Interface**: Remote access via standardized MCP protocol
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Performance
- **Lightweight**: Minimal overhead on original game logic
- **Fast Startup**: Quick initialization and response times
- **Memory Efficient**: Single game session with automatic cleanup

### Reliability
- **Error Recovery**: Graceful handling of invalid inputs and edge cases
- **State Management**: Consistent game state across tool calls
- **Input Validation**: Reuses original robust validation logic

## 🧪 Testing

A test script is available to verify functionality:

```bash
python test_mcp_server.py
```

Expected output:
```
✅ Successfully imported game components
✅ Game state created with secret: XXXX
✅ Validator test: (True, '1234', '')
✅ Game logic test - feedback: XA YB
🎉 All tests passed! The MCP server should work correctly.
```

## 📝 License

This MCP server wrapper inherits the same MIT license as the original 1A2B game.
