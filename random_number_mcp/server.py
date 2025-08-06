#!/usr/bin/env python3
"""
Random Number MCP Server

A simple MCP server that provides tools for generating random numbers.
Uses the elegant FastMCP approach for clean, declarative tool definitions.
"""

import random
from typing import Literal
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("random-number-server")


@mcp.tool()
async def get_random_number(
    min_val: float = 0,
    max_val: float = 100,
    number_type: Literal["integer", "float"] = "integer",
    count: int = 1,
) -> str:
    """Generate random numbers with customizable parameters.

    Args:
        min_val: Minimum value (default: 0)
        max_val: Maximum value (default: 100)
        number_type: Type of number to generate - 'integer' or 'float'
                    (default: integer)
        count: Number of random numbers to generate, between 1 and 100
               (default: 1)
    """
    # Validate parameters
    if min_val >= max_val:
        raise ValueError("min_val must be less than max_val")

    if count < 1 or count > 100:
        raise ValueError("count must be between 1 and 100")

    # Generate random numbers
    if number_type == "integer":
        numbers = [random.randint(int(min_val), int(max_val)) for _ in range(count)]
    else:  # float
        numbers = [random.uniform(min_val, max_val) for _ in range(count)]

    # Format result
    if count == 1:
        return f"Random {number_type}: {numbers[0]}"
    else:
        return f"Random {number_type}s: {numbers}"


def main():
    """Main entry point."""
    mcp.run()


if __name__ == "__main__":
    main()
