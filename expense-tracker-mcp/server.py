from datetime import datetime
from fastmcp import FastMCP
from db.database import init_db,get_session
from db.model import Expense, Budget
from sqlalchemy import extract


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

# delete expense
@mcp.tool()
def delete_expense(expense_id: int)->str:
    """Delete an expense from the database."""
    session=get_session()
    try:
        expense=session.query(Expense).filter(Expense.id==expense_id).first()
        if not expense:
            return f"Expense with id {expense_id} not found"
        session.delete(expense)
        session.commit()
        return f"Expense with id {expense_id} deleted successfully"
    except Exception as e:
        session.rollback()
        return f"Failed to delete expense: {str(e)}"
    finally:
        session.close()

# get monthly summary
@mcp.tool()
def get_monthly_summary(month: int, year: int)->dict:
    """Get the monthly summary of expenses."""
    session=get_session()
    try:
        expenses=(session.query(Expense).filter(
            extract('month', Expense.date)==month,
            extract('year', Expense.date)==year
        ).all())

        summary={}
        for e in expenses:
            summary[e.category]=summary.get(e.category, 0) + e.amount
        return summary
    except Exception as e:
        return f"Failed to get monthly summary: {str(e)}"
    finally:
        session.close()

# set budgets
@mcp.tool()
def set_budget(category: str, amount: float, month: int, year: int) -> str:
    """Set a spending budget for a category in a given month."""
    session = get_session()
    try:
        existing = (
            session.query(Budget)
            .filter_by(category=category, month=month, year=year)
            .first()
        )
        if existing:
            existing.amount = amount
            msg = f" Updated budget for '{category}': ₹{amount}"
        else:
            session.add(Budget(category=category, amount=amount, month=month, year=year))
            msg = f" Budget set for '{category}': ₹{amount} for {month}/{year}"
        session.commit()
        return msg
    finally:
        session.close()

# check budget
@mcp.tool()
def check_budget(category: str, month: int, year: int) -> dict:
    """Check spending vs budget for a category. Returns warning if over budget."""
    session = get_session()
    try:
        budget = (
            session.query(Budget)
            .filter_by(category=category, month=month, year=year)
            .first()
        )
        expenses = (
            session.query(Expense)
            .filter(
                Expense.category.ilike(f"%{category}%"),
                extract("month", Expense.date) == month,
                extract("year", Expense.date) == year
            )
            .all()
        )
        spent = sum(e.amount for e in expenses)
        budget_amount = budget.amount if budget else 0
        remaining = budget_amount - spent
        status = "Over budget!" if spent > budget_amount else " Within budget"

        return {
            "category": category,
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "status": status
        }
    except Exception as e:
        return f"Failed to check budget: {str(e)}"
    finally:
        session.close()
# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8001)