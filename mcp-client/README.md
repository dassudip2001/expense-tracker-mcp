# MCP Client

An intelligent LLM-powered client that discovers and uses tools from Model Context Protocol (MCP) servers. Built with LangChain and OpenAI integration.

## Overview

This client demonstrates an agent-based architecture that:
1. Connects to multiple MCP servers
2. Discovers available tools
3. Uses an LLM (OpenAI GPT-4o) to intelligently invoke tools
4. Processes tool results and continues reasoning

## Features

### Intelligent Agent Architecture
- **Tool Discovery**: Automatically discovers all available tools from MCP servers
- **LLM Integration**: Uses OpenAI's GPT-4o model for intelligent tool selection
- **Multi-Server Support**: Can connect to multiple MCP servers simultaneously
- **File System Access**: Demonstrates filesystem interaction capabilities

### Current Implementation

The client connects to the `@modelcontextprotocol/server-filesystem` MCP server to:
- Create, read, and manage files
- Execute commands in a controlled filesystem environment
- Leverage AI for intelligent file operations

## Installation

1. Navigate to the client directory:
```bash
cd mcp-client
```

2. Install dependencies using pip:
```bash
pip install -e .
```

Or using uv:
```bash
uv sync
```

## Configuration

### Environment Variables

Create a `.env` file in the client directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4o access

### Filesystem Configuration

The client is configured to work with a specific filesystem folder. Update this in `main.py`:

```python
MCP_FOLDER = "C:\Users\sudip\Downloads\mcp\test"
```

Change this path to the directory where you want the client to operate.

## Running the Client

1. Ensure the `.env` file is configured with your OpenAI API key
2. Ensure the `MCP_FOLDER` path exists
3. Run the client:

```bash
python main.py
```

## Project Structure

```
mcp-client/
├── main.py            # Client implementation
├── pyproject.toml     # Project configuration and dependencies
├── .env              # Environment variables (create this)
└── README.md         # This documentation
```

## Dependencies

- **langchain-openai** (>=1.1.12) - OpenAI model integration
- **langchain-mcp-adapters** (>=0.2.2) - MCP client adapters for LangChain
- **langchain-core** (>=1.2.23) - Core LangChain utilities
- **python-dotenv** (>=1.2.2) - Environment variable management

## Architecture

### Message Flow

```
User Query
    ↓
LLM with Tools
    ↓
Tool Selection
    ↓
Tool Execution (via MCP)
    ↓
Result Processing
    ↓
LLM Reasoning
    ↓
Final Response
```

### Components

1. **MultiServerMCPClient**: Manages connections to multiple MCP servers
2. **Tool Discovery**: Retrieves all tools from connected servers
3. **LLM Agent**: Uses OpenAI's ChatOpenAI model to select and invoke tools
4. **Message Loop**: Handles back-and-forth communication until task completion

## Usage Example

The current implementation demonstrates creating a file:

```python
prompt = "create a file named test.txt and write 'Hello World' in it"
```

The agent will:
1. Parse the prompt
2. Discover available file system tools
3. Select appropriate tools (file creation)
4. Invoke them intelligently
5. Return the result

## Extending the Client

### Adding New MCP Servers

Modify the `chat()` function to add more servers:

```python
client = MultiServerMCPClient({
    "file_system": { ... },
    "your_service": {
        "transport": "stdio",
        "command": "your-mcp-command",
        "args": ["arg1", "arg2"]
    }
})
```

### Changing the LLM Model

Update the model in the client:

```python
llm = ChatOpenAI(model="gpt-4-turbo")  # Change model here
```

## Platform Compatibility

The client handles different operating systems:

```python
def npx_command():
    if platform.system() == "Windows":
        return "npx.cmd"
    else:
        return "npx"
```

This automatically uses the correct command for your OS.

## Troubleshooting

### OpenAI API Key Error
Ensure your `.env` file:
```bash
# Check that the file exists
ls -la .env

# Verify the key format
cat .env
```

### MCP Server Connection Error
- Ensure the filesystem folder exists: `mkdir -p "C:\Users\sudip\Downloads\mcp\test"`
- Verify npm/npx is installed: `npx -v`
- Check the MCP folder path is correct

### Tool Not Found
- Verify the MCP server is running (if using local backend)
- Check tool names match the server's exports
- Review MCP server logs for errors

## Development

To test the client:

1. Create the test directory: `mkdir test`
2. Configure `.env` with your OpenAI API key
3. Run: `python main.py`
4. Check the `test` directory for created files

## License

MIT
