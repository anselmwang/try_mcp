# Random Number MCP Server

A simple Model Context Protocol (MCP) server that provides tools for generating random numbers.

## Features

- Generate random integers or floating-point numbers
- Customizable min/max range
- Generate multiple random numbers at once
- Proper error handling and validation

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python -m random_number_mcp.server
```

### Available Tools

#### `get_random_number`

Generate random numbers with customizable parameters.

**Parameters:**
- `min` (number, optional): Minimum value (default: 0)
- `max` (number, optional): Maximum value (default: 100)
- `type` (string, optional): "integer" or "float" (default: "integer")
- `count` (integer, optional): Number of random numbers to generate (default: 1, max: 100)

**Examples:**
- Generate a single random integer between 0-100: `{}`
- Generate a random float between 0-1: `{"min": 0, "max": 1, "type": "float"}`
- Generate 5 random integers between 1-10: `{"min": 1, "max": 10, "count": 5}`

## MCP Configuration

To use this server with an MCP client, add the following configuration:

```json
{
  "mcpServers": {
    "random-number": {
      "command": "python",
      "args": ["/path/to/your/project/.venv/Scripts/python", "-m", "random_number_mcp.server"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

## Development

The server is built using the Python MCP SDK and follows the MCP protocol specification.

### Project Structure

```
random-number-mcp/
├── .venv/                  # Virtual environment
├── random_number_mcp/      # Main package
│   ├── __init__.py
│   └── server.py          # MCP server implementation
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## License

MIT License
