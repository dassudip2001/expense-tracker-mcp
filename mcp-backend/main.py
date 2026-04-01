from fastmcp import FastMCP
from datetime import datetime

from langchain_community.tools import DuckDuckGoSearchRun

mcp=FastMCP("MCP Server")


search_tool = DuckDuckGoSearchRun()

@mcp.tool()
def get_current_time():
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def search_duckduckgo(query: str):
    """Search DuckDuckGo for a query."""
    return search_tool.run(query)


mcp.run(transport="sse", host="localhost", port=8000)