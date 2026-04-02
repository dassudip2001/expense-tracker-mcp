from datetime import datetime
from fastmcp import FastMCP
from db.database import init_db,get_session
from db.model import Expense

# Initialize the database
init_db()

# Create the MCP server
mcp=FastMCP("Expense Tracker")



# Add expense
@mcp.tool()
def add_expense(amount: float, category: str, description: str, date: str)->str:
    """Add a new expense to the database."""
    session=get_session()
    try:
        parse_data=(
            datetime.strftime(date,"%Y-%m-%d").date()
            if date else date.today()
        )

        expense=Expense(
            amount=amount,
            category=category,
            description=description,
            date=parse_data
        )
        session.add(expense)
        session.commit()
        return f"Expense of {amount} added successfully for {category} on {date}"
    except Exception as e:
        session.rollback()
        return f"Failed to add expense: {str(e)}"
    finally:
        session.close()


# Get expenses





# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8001)