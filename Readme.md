# MCP (Model Context Protocol) Project

A complete implementation of the Model Context Protocol featuring a FastMCP-based backend server and a LangChain-powered client for intelligent tool integration.

## Project Structure

```
mcp/
├── mcp-backend/         # FastMCP server providing tools and services
├── mcp-client/          # LLM-powered client for tool interaction
└── README.md           # This file
```

## Overview

This project demonstrates the Model Context Protocol (MCP) pattern with:

- **Backend Server**: A FastMCP server that exposes tools like web search and time information
- **Client Application**: An intelligent client powered by LangChain and OpenAI that can discover and use available tools

## Components

### MCP Backend
A FastMCP server providing:
- **Search Tool**: DuckDuckGo web search capability
- **Time Tool**: Current datetime information
- **Protocol**: SSE (Server-Sent Events) transport on localhost:8000

[More details →](./mcp-backend/README.md)

### MCP Client
An agent-based client featuring:
- Multi-server MCP client support
- LangChain integration with OpenAI models
- File system interaction capabilities
- Tool-calling agent architecture

[More details →](./mcp-client/README.md)

## Quick Start

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Setup

1. **Backend Server**
```bash
cd mcp-backend
pip install -r requirements.txt  # or: uv sync
python main.py
```
The server will start on `http://localhost:8000`

2. **Client**
```bash
cd mcp-client
pip install -r requirements.txt  # or: uv sync
# Configure your OpenAI API key in .env
python main.py
```

## Environment Configuration

Create a `.env` file in the mcp-client directory:

```env
OPENAI_API_KEY=your_api_key_here
```

## Dependencies

### Backend
- `fastmcp>=3.2.0` - FastMCP framework
- `langchain-community>=0.4.1` - LangChain community tools
- `langchain-core>=1.2.23` - Core LangChain utilities
- `ddgs>=9.12.0` - DuckDuckGo search API

### Client
- `langchain-openai>=1.1.12` - OpenAI integration
- `langchain-mcp-adapters>=0.2.2` - MCP client adapters
- `langchain-core>=1.2.23` - Core LangChain utilities
- `python-dotenv>=1.2.2` - Environment variable management

## License

MIT
