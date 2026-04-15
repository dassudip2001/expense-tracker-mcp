# MCP Backend Server

A FastMCP-based server that provides tools and services through the Model Context Protocol using SSE (Server-Sent Events) transport.

## Overview

This server exposes utility tools that can be discovered and used by MCP clients. It's built with FastMCP and provides a simple yet powerful interface for tool integration.

## Features

### Available Tools

#### 1. **get_current_time()**
Returns the current date and time in ISO format.

**Usage**: Get the current timestamp without parameters.

#### 2. **search_duckduckgo(query: str)**
Performs a web search using the DuckDuckGo search engine.

**Parameters:**
- `query` (string): The search query

**Returns:** Search results from DuckDuckGo

## Installation

1. Navigate to the backend directory:
```bash
cd mcp-backend
```

2. Install dependencies using pip:
```bash
pip install -e .
```

Or using uv:
```bash
uv sync
```

## Running the Server

Start the server with:

```bash
python main.py
```

## Add the MCP server
```bash
uv run fastmcp install claude-desktop <filename.py>
```

The server will start on:
- **Host**: localhost
- **Port**: 8000
- **Transport**: SSE (Server-Sent Events)

You should see output indicating the server is running and ready for client connections.

## Project Structure

```
mcp-backend/
├── main.py            # Server implementation
├── pyproject.toml     # Project configuration and dependencies
└── README.md         # This documentation
```

## Dependencies

- **fastmcp** (>=3.2.0) - FastMCP framework for building MCP servers
- **langchain-community** (>=0.4.1) - Community tools including DuckDuckGoSearchRun
- **langchain-core** (>=1.2.23) - Core LangChain utilities
- **ddgs** (>=9.12.0) - Python wrapper for DuckDuckGo search API

## Architecture

The server uses the FastMCP framework to:
1. Define tool functions using the `@mcp.tool()` decorator
2. Provide automatic tool discovery and schema generation
3. Handle client connections via SSE transport
4. Manage tool invocation and response handling

## Extending the Server

To add new tools, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
def my_new_tool(param1: str, param2: int):
    """Description of what the tool does."""
    # Implementation
    return result
```

The FastMCP framework automatically:
- Discovers the tool function
- Generates the correct schema
- Makes it available to clients

## Development

To modify the server:

1. Edit `main.py` to add or modify tools
2. Restart the server process
3. Clients will automatically discover the updated tools

## Configuration

### Port and Host

Edit `main.py` to change the server configuration:

```python
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

- Change `host` to bind to different interfaces (default: localhost)
- Change `port` to use a different port (default: 8000)

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, either:
- Stop the process using that port
- Change the port in `main.py`

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -e .
```

## License

MIT
