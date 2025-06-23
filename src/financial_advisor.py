"""
Run the financial analysis with the given user data.
"""
from typing import Dict, Any
import streamlit as st
from crewai import Agent, Task, Crew
from src.utils import get_azure_llm
import json

@st.cache_resource(show_spinner=False)
def create_financial_crew():
    """Create and return the financial advisor crew."""
    azure_llm = get_azure_llm()
    
    # Create agents
    budgeting_agent = Agent(
        role="Budgeting Advisor & Financial Calculator",
        goal="Create detailed budgets with mathematical analysis and tabular financial breakdowns.",
        backstory=(
            """You are an expert financial advisor with strong analytical and mathematical skills.
            You excel at creating detailed financial tables, calculating ratios, percentages, and 
            presenting complex financial data in clear, organized formats. You use precise calculations
            to support all your recommendations and present data in tables for easy understanding."""
        ),
        allow_delegation=False,
        verbose=True,
        llm=azure_llm
    )
    
    investment_agent = Agent(
        role="Investment Advisor & Portfolio Analyst",
        goal="Recommend investments with detailed mathematical projections and risk calculations.",
        backstory=(
            """You are an investment expert who specializes in quantitative analysis and portfolio optimization.
            You provide detailed mathematical projections, compound interest calculations, and risk assessments.
            You present investment recommendations with supporting tables showing projected returns, scenarios,
            and time-based growth calculations."""
        ),
        allow_delegation=False,
        verbose=True,
        llm=azure_llm
    )
    
    debt_management_agent = Agent(
        role="Debt Management Specialist & Payment Calculator",
        goal="Create mathematical debt repayment strategies with detailed payment schedules and savings calculations.",
        backstory=(
            """You specialize in debt optimization using mathematical models and payment calculations.
            You create detailed amortization schedules, calculate interest savings, and provide
            precise payoff timelines. You present all debt strategies in clear tabular formats
            showing payment amounts, interest costs, and total savings."""
        ),
        allow_delegation=False,
        verbose=True,
        llm=azure_llm
    )
    
    # Create tasks with mathematical focus
    budgeting_task = Task(
        description="""
        Analyze the client's financial situation with MATHEMATICAL PRECISION using these specific details:

        INCOME & EXPENSES DATA:
        - Monthly Income: {monthly_income}
        - Net Monthly Income: {net_monthly_income}
        - Savings Goal: {savings_goal}
        - Total Monthly Expenses: {total_monthly_expenses}
        - Rent/Mortgage: {expense_breakdown[rent]}
        - Utilities: {expense_breakdown[utilities]}
        - Groceries: {expense_breakdown[groceries]}
        - Transportation: {expense_breakdown[transportation]}
        - Entertainment: {expense_breakdown[entertainment]}
        - Other: {expense_breakdown[other]}

        DEBT DATA:
        - Credit Card: {debt_details[credit_card_balance]} at {debt_details[credit_card_rate]}
        - Loan: {debt_details[loan_balance]} at {debt_details[loan_rate]}

        Create a comprehensive analysis with:

        1. **EXPENSE ANALYSIS TABLE** showing:
           - Category | Amount | % of Income | Recommended % | Variance
        
        2. **FINANCIAL RATIOS CALCULATION**:
           - Savings Rate = (Savings Goal / Monthly Income) × 100
           - Expense Ratio = (Total Expenses / Monthly Income) × 100
           - Debt-to-Income Ratio calculation
        
        3. **MONTHLY CASH FLOW TABLE**:
           - Income vs Expenses breakdown
           - Available funds for savings/debt payment
        
        4. **50/30/20 BUDGET COMPARISON TABLE**:
           - Current allocation vs recommended 50/30/20 rule
        
        5. **SAVINGS PROJECTION TABLE** (1, 3, 5, 10 years):
           - Monthly savings compound growth calculations

        Use MARKDOWN TABLES and show all mathematical calculations.
        """,
        expected_output="""A detailed financial budget analysis with:
        - Mathematical calculations and percentages
        - Multiple comparison tables in markdown format
        - Financial ratios and metrics
        - Cash flow analysis with precise numbers
        - Savings growth projections with compound interest calculations""",
        agent=budgeting_agent
    )
    
    investment_task = Task(
        description="""
        Based on the financial data provided, create investment recommendations with MATHEMATICAL PROJECTIONS:

        Available for Investment: {net_monthly_income} (after covering savings goal of {savings_goal})
        Risk Profile: Moderate (based on current financial stability)

        Create:

        1. **INVESTMENT ALLOCATION TABLE**:
           - Asset Class | Allocation % | Monthly Amount | Annual Amount
        
        2. **COMPOUND GROWTH PROJECTIONS TABLE**:
           - Year | Principal | Interest Earned | Total Value
           - Show 1, 5, 10, 15, 20 year projections
        
        3. **RISK-RETURN SCENARIOS TABLE**:
           - Scenario | Annual Return % | 10-Year Value | 20-Year Value
           - Conservative (4-6%), Moderate (6-8%), Aggressive (8-10%)
        
        4. **MONTHLY INVESTMENT BREAKDOWN**:
           - Emergency Fund: 3-6 months expenses calculation
           - Retirement: 10-15% of income calculation
           - Growth Investments: Remaining available funds
        
        5. **RETIREMENT CALCULATION TABLE**:
           - Current age assumptions (30, 35, 40)
           - Retirement needs calculation
           - Required monthly savings for different retirement goals

        Show all compound interest formulas: A = P(1 + r/n)^(nt)
        """,
        expected_output="""Investment strategy with:
        - Detailed allocation tables with percentages and dollar amounts
        - Compound growth projections with mathematical formulas
        - Multiple scenario analysis tables
        - Retirement planning calculations
        - Risk assessment with quantified projections""",
        agent=investment_agent
    )
    
    debt_management_task = Task(
        description="""
        Create a MATHEMATICAL DEBT ELIMINATION STRATEGY using:

        DEBT DETAILS:
        - Credit Card: {debt_details[credit_card_balance]} at {debt_details[credit_card_rate]}
        - Loan: {debt_details[loan_balance]} at {debt_details[loan_rate]}
        
        Available for debt payment: Calculate from {net_monthly_income} after {savings_goal}

        Create:

        1. **CURRENT DEBT SUMMARY TABLE**:
           - Debt Type | Balance | Interest Rate | Minimum Payment | Total Interest if Min Payments
        
        2. **DEBT AVALANCHE vs SNOWBALL COMPARISON**:
           - Method | Total Interest Paid | Payoff Time | Monthly Payment
        
        3. **PAYMENT STRATEGY TABLE** (Recommended approach):
           - Month | Payment Amount | Principal | Interest | Remaining Balance
           - Show first 12 months and key milestones
        
        4. **INTEREST SAVINGS CALCULATION**:
           - Extra Payment Amount | Time Saved | Interest Saved | Total Savings
           - Show scenarios for +$50, +$100, +$200 extra payments
        
        5. **DEBT-FREE TIMELINE TABLE**:
           - Current payments vs optimized payments
           - Mathematical proof of interest savings
        
        6. **DEBT CONSOLIDATION ANALYSIS** (if applicable):
           - Current total monthly payments
           - Potential consolidated payment at lower rate
           - Savings calculation and break-even analysis

        Use precise mathematical formulas for all calculations.
        Show amortization formulas: M = P[r(1+r)^n]/[(1+r)^n-1]
        """,
        expected_output="""Comprehensive debt management plan with:
        - Detailed payment schedules with mathematical calculations
        - Comparison tables for different strategies
        - Interest savings calculations with precise dollar amounts
        - Timeline tables showing month-by-month progress
        - Mathematical formulas and compound interest calculations
        - ROI analysis for different payment strategies""",
        agent=debt_management_agent
    )
    
    # Create crew
    crew = Crew(
        agents=[budgeting_agent, investment_agent, debt_management_agent],
        tasks=[budgeting_task, investment_task, debt_management_task],
        verbose=True
    )
    
    return crew

def calculate_financial_metrics(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-calculate key financial metrics for the analysis."""
    
    income = financial_data.get('income', 0)
    expenses = financial_data.get('expenses', {})
    debts = financial_data.get('debts', {})
    savings_goal = financial_data.get('savings_goal', 0)
    
    # Basic calculations
    total_expenses = sum(expenses.values())
    net_income = income - total_expenses
    available_for_debt = max(0, net_income - savings_goal)
    
    # Financial ratios
    savings_rate = (savings_goal / income * 100) if income > 0 else 0
    expense_ratio = (total_expenses / income * 100) if income > 0 else 0
    
    # Debt calculations
    cc_debt = debts.get('credit_card', {})
    loan_debt = debts.get('student_loan', {})
    
    total_debt = cc_debt.get('balance', 0) + loan_debt.get('balance', 0)
    debt_to_income = (total_debt / (income * 12) * 100) if income > 0 else 0
    
    # Minimum payments calculation (rough estimate)
    cc_min_payment = cc_debt.get('balance', 0) * 0.02  # 2% minimum
    loan_min_payment = loan_debt.get('balance', 0) * 0.01  # 1% minimum
    total_min_payments = cc_min_payment + loan_min_payment
    
    return {
        'total_expenses': total_expenses,
        'net_income': net_income,
        'available_for_debt': available_for_debt,
        'savings_rate': savings_rate,
        'expense_ratio': expense_ratio,
        'total_debt': total_debt,
        'debt_to_income': debt_to_income,
        'cc_min_payment': cc_min_payment,
        'loan_min_payment': loan_min_payment,
        'total_min_payments': total_min_payments
    }

def run_financial_analysis(financial_data: Dict[str, Any]) -> str:
    """Run comprehensive financial analysis with mathematical calculations."""
    
    # Extract and validate data
    income = financial_data.get('income', 0)
    expenses = financial_data.get('expenses', {})
    debts = financial_data.get('debts', {})
    savings_goal = financial_data.get('savings_goal', 0)
    
    # Calculate metrics
    metrics = calculate_financial_metrics(financial_data)
    
    # Format data for CrewAI with additional calculations
    analysis_inputs = {
        "monthly_income": f"${income:,.2f}",
        "savings_goal": f"${savings_goal:,.2f}",
        "total_monthly_expenses": f"${metrics['total_expenses']:,.2f}",
        "net_monthly_income": f"${metrics['net_income']:,.2f}",
        "available_for_debt_payment": f"${metrics['available_for_debt']:,.2f}",
        "savings_rate_percentage": f"{metrics['savings_rate']:.1f}%",
        "expense_ratio_percentage": f"{metrics['expense_ratio']:.1f}%",
        "debt_to_income_ratio": f"{metrics['debt_to_income']:.1f}%",
        "expense_breakdown": {
            "rent": f"${expenses.get('rent', 0):,.2f}",
            "utilities": f"${expenses.get('utilities', 0):,.2f}",
            "groceries": f"${expenses.get('groceries', 0):,.2f}",
            "transportation": f"${expenses.get('transportation', 0):,.2f}",
            "entertainment": f"${expenses.get('entertainment', 0):,.2f}",
            "other": f"${expenses.get('other', 0):,.2f}"
        },
        "debt_details": {
            "credit_card_balance": f"${debts.get('credit_card', {}).get('balance', 0):,.2f}",
            "credit_card_rate": f"{debts.get('credit_card', {}).get('interest_rate', 0)*100:.1f}%",
            "loan_balance": f"${debts.get('student_loan', {}).get('balance', 0):,.2f}",
            "loan_rate": f"{debts.get('student_loan', {}).get('interest_rate', 0)*100:.1f}%",
            "cc_min_payment": f"${metrics['cc_min_payment']:,.2f}",
            "loan_min_payment": f"${metrics['loan_min_payment']:,.2f}",
            "total_min_payments": f"${metrics['total_min_payments']:,.2f}"
        }
    }
    
    # Add mathematical context
    analysis_inputs["mathematical_context"] = f"""
    FINANCIAL CALCULATION FORMULAS TO USE:
    
    1. Compound Interest: A = P(1 + r/n)^(nt)
    2. Debt Payment: M = P[r(1+r)^n]/[(1+r)^n-1]
    3. Savings Rate: (Monthly Savings / Monthly Income) × 100
    4. Debt-to-Income: (Total Debt / Annual Income) × 100
    5. Emergency Fund: Monthly Expenses × 3 to 6 months
    
    CURRENT FINANCIAL SNAPSHOT:
    - Income: {income:,.0f}/month = {income*12:,.0f}/year
    - Expenses: {metrics['total_expenses']:,.0f}/month = {metrics['total_expenses']*12:,.0f}/year
    - Net Cash Flow: {metrics['net_income']:,.0f}/month
    - Current Savings Rate: {metrics['savings_rate']:.1f}%
    - Current Expense Ratio: {metrics['expense_ratio']:.1f}%
    """
    
    # Create the crew and run analysis
    crew = create_financial_crew()
    result = crew.kickoff(inputs=analysis_inputs)
    
    # Add a mathematical summary at the end
    mathematical_summary = f"""

---

## 📊 QUICK FINANCIAL METRICS SUMMARY

| **Metric** | **Current Value** | **Recommended Range** | **Status** |
|------------|-------------------|----------------------|------------|
| Savings Rate | {metrics['savings_rate']:.1f}% | 20-30% | {'✅ Good' if metrics['savings_rate'] >= 20 else '⚠️ Improve'} |
| Expense Ratio | {metrics['expense_ratio']:.1f}% | 70-80% | {'✅ Good' if metrics['expense_ratio'] <= 80 else '⚠️ High'} |
| Debt-to-Income | {metrics['debt_to_income']:.1f}% | <36% | {'✅ Good' if metrics['debt_to_income'] < 36 else '❌ High'} |

### 🧮 Key Calculations:
- **Monthly Cash Flow**: ${income:,.0f} - ${metrics['total_expenses']:,.0f} = ${metrics['net_income']:,.0f}
- **Annual Savings Potential**: ${metrics['net_income']*12:,.0f}
- **Emergency Fund Target**: ${metrics['total_expenses']*6:,.0f} (6 months expenses)
- **Total Debt Burden**: ${metrics['total_debt']:,.0f}

*All calculations are based on your specific financial data provided.*
"""
    
    return result.raw + mathematical_summary