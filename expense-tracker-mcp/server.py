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
@mcp.tool()
def get_expenses(start_date: str="", end_date:str="", category:str="")->list[dict]:
    """Get expenses from the database."""
    session=get_session()
    try:
        query=session.query(Expense)
        if start_date:
            query=query.filter(Expense.date >=datetime.strftime(start_date,"%Y-%m-%d").date())
        if end_date:
            query=query.filter(Expense.date <=datetime.strftime(end_date,"%Y-%m-%d").date())
        if category:
            query=query.filter(Expense.category.ilike(f"%{category}%"))
        expenses=query.order_by(Expense.date.desc()).all()
        return [
            {
                "id": e.id,
                "amount": e.amount,
                "category": e.category,
                "description": e.description,
                "date": str(e.date)
            } for e in expenses
        ]
    except Exception as e:
        return f"Failed to get expenses: {str(e)}"
    finally:
        session.close()




# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8001)