# Expense Tracker MCP

A [Model Context Protocol](https://modelcontextprotocol.io/) server built with [FastMCP](https://github.com/jlowin/fastmcp) that stores expenses and budgets in SQLite via SQLAlchemy. Clients (for example Cursor, Claude Desktop, or a LangChain app) can add and query spending, set monthly budgets per category, and compare spend against budget.

## Requirements

- Python 3.11+
- Dependencies are listed in [`pyproject.toml`](pyproject.toml) (notably `fastmcp` and `sqlalchemy`).

## Install

From this directory:

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

## Run the server

The server uses **SSE** transport and listens on **port 8001** by default:

```bash
python server.py
```

The MCP SSE endpoint is:

```text
http://localhost:8001/sse
```

On first run, SQLite creates `expense_tracker.db` in the **current working directory** (see [`db/database.py`](db/database.py)).

## MCP tools

| Tool | Purpose |
|------|---------|
| `add_expense` | Add an expense (`amount`, `category`, `description`, `date` as `YYYY-MM-DD`). |
| `get_expenses` | List expenses; optional `start_date`, `end_date`, `category` filters. |
| `delete_expense` | Remove an expense by `expense_id`. |
| `get_monthly_summary` | Totals per category for a given `month` and `year`. |
| `set_budget` | Create or update a monthly budget for a `category`. |
| `check_budget` | Compare spend vs budget for a `category` in a `month`/`year`. |

## Connect a client

Point any MCP client that supports **SSE** at `http://localhost:8001/sse`. For example, in a LangChain [`MultiServerMCPClient`](https://github.com/langchain-ai/langchain-mcp-adapters) setup:

```python
"expense-tracker": {
    "transport": "sse",
    "url": "http://localhost:8001/sse",
}
```

Ensure this server is running before the client connects.

## Project layout

- [`server.py`](server.py) — FastMCP app and tool definitions.
- [`db/model.py`](db/model.py) — `Expense` and `Budget` SQLAlchemy models.
- [`db/database.py`](db/database.py) — SQLite engine, session factory, and `init_db()`.

## License

See the repository root for license information if applicable.
