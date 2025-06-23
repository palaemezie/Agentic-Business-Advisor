"""
Business Advisor Suite - Streamlit Application
A comprehensive financial planning and business strategy platform
"""

import streamlit as st

st.set_page_config(
    page_title="Business Advisor Suite",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

loading_placeholder = st.empty()
sidebar_placeholder = st.sidebar.empty()

with loading_placeholder.container():
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>💼 Business Advisor Suite</h1>
        <div style="margin: 2rem 0;">
            <div style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; 
                        width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
        </div>
        <h3>🚀 Initializing Your Business Advisor...</h3>
        <p>Loading modules and setting up environment...</p>
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
            <p><strong>Loading Components:</strong></p>
            <p>• Financial Analysis Engine</p>
            <p>• Product Launch Planner</p>
            <p>• Web Research Tools</p>
            <p>• AI Models & Configurations</p>
        </div>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

with sidebar_placeholder.container():
    st.markdown("### 🔄 Loading Navigation...")
    st.progress(0.3)
    st.text("Preparing modules...")

# Now import heavy dependencies after showing the loading screen
import asyncio
import json
import os
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional

# === CONFIGURATION ===
SRC_DIR = Path(__file__).parent
sys.path.insert(0, str(SRC_DIR))

with loading_placeholder.container():
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>💼 Business Advisor Suite</h1>
        <div style="margin: 2rem 0;">
            <div style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; 
                        width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
        </div>
        <h3>📦 Loading Core Modules...</h3>
        <p>Importing financial advisor, product launcher, and research tools...</p>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

with sidebar_placeholder.container():
    st.markdown("### 📦 Loading Modules...")
    st.progress(0.6)
    st.text("Importing core components...")

try:
    from src.config_manager import load_user_config, save_user_config, reset_to_defaults
    from src.config import OUTPUT_DIR
    from src import financial_advisor, product_launcher, web_researcher, utils
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

with loading_placeholder.container():
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>💼 Business Advisor Suite</h1>
        <div style="margin: 2rem 0;">
            <div style="border: 4px solid #27ae60; border-top: 4px solid #2ecc71; border-radius: 50%; 
                        width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
        </div>
        <h3>✅ Almost Ready!</h3>
        <p>Finalizing setup and preparing interface...</p>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

with sidebar_placeholder.container():
    st.markdown("### ✅ Finalizing...")
    st.progress(0.9)
    st.text("Ready to launch!")

PAGES = {
    "Financial Advisor": "💰",
    "Product Launch Planner": "🚀", 
    "Website Researcher": "🔍",
    "Settings": "⚙️"
}

EMPTY_FINANCIAL_DATA = {
    "income": 0,
    "savings_goal": 0,
    "expenses": {
        "rent": 0,
        "utilities": 0,
        "groceries": 0,
        "transportation": 0,
        "entertainment": 0,
        "other": 0
    },
    "debts": {
        "credit_card": {"balance": 0, "interest_rate": 0.0},
        "student_loan": {"balance": 0, "interest_rate": 0.0}
    }
}

EMPTY_PRODUCT_DATA = {
    "product_name": "",
    "product_description": "",
    "target_market": "",
    "launch_date": date.today().isoformat(),
    "budget": 1000
}

@st.cache_resource(show_spinner=False)
def initialize_app() -> None:
    """Initialize application resources and ensure directories exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return True

def setup_session_state() -> None:
    """Initialize session state with default values."""
    if 'user_config' not in st.session_state:
        st.session_state.user_config = load_user_config()
    
    if 'financial_result' not in st.session_state:
        st.session_state.financial_result = None
        
    if 'product_result' not in st.session_state:
        st.session_state.product_result = None
        
    if 'research_result' not in st.session_state:
        st.session_state.research_result = None

def check_environment() -> bool:
    """Verify environment setup."""
    success, message = utils.setup_environment_variables()
    if not success:
        st.error(f"Environment setup error: {message}")
        st.error("Please configure your environment variables.")
        return False
    return True

def create_progress_handler(status_messages: list) -> callable:
    """Create a progress handler with custom status messages."""
    def update_progress(progress: int, elapsed: float) -> None:
        progress_bar = st.session_state.get('progress_bar')
        status_text = st.session_state.get('status_text')
        
        if progress_bar:
            progress_bar.progress(progress)
        
        if status_text and status_messages:
            message_index = min(int(progress / (100 / len(status_messages))), len(status_messages) - 1)
            remaining_time = max(60 - int(elapsed), 0)
            status_text.text(f"{status_messages[message_index]} (Est. {remaining_time}s remaining)")
    
    return update_progress

def safe_file_write(file_path: str, content: str) -> bool:
    """Safely write content to file with error handling."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        return os.path.exists(file_path) and os.path.getsize(file_path) > 0
    except Exception:
        return False

def sanitize_filename(name: str) -> str:
    """Create safe filename from string."""
    return "".join(c for c in name if c.isalnum() or c in ('_', '-')).rstrip()[:50]

loading_placeholder.empty()
sidebar_placeholder.empty()

def render_sidebar() -> str:
    """Render sidebar navigation and return selected page."""
    st.sidebar.title("🏢 Business Advisor Suite")
    st.sidebar.markdown("---")
    
    page_options = [f"{icon} {name}" for name, icon in PAGES.items()]
    selected = st.sidebar.radio("Navigate to:", page_options)
    
    page_name = selected.split(" ", 1)[1]
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip**: Save your settings in the Settings page for faster workflow!")
    
    return page_name

def main_interface() -> None:
    """Main application router."""
    page = render_sidebar()
    
    st.title(f"{PAGES[page]} {page}")
    
    if page == "Financial Advisor":
        render_financial_advisor()
    elif page == "Product Launch Planner":
        render_product_launcher()
    elif page == "Website Researcher":
        render_web_researcher()
    elif page == "Settings":
        render_settings()

def render_financial_advisor() -> None:
    """Render Financial Advisor interface."""
    st.markdown("""
    ### 📊 Comprehensive Financial Analysis
    Get personalized recommendations for budgeting, investments, and debt management.
    """)
    
    with st.form("financial_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Income & Savings")
            income = st.number_input("Monthly Income ($)", min_value=0, step=100, help="Your total monthly income")
            savings_goal = st.number_input("Monthly Savings Goal ($)", min_value=0, step=50, help="How much you want to save monthly")
            
            st.subheader("💳 Debt Information")
            cc_balance = st.number_input("Credit Card Balance ($)", min_value=0, step=100)
            cc_interest = st.number_input("Credit Card Interest Rate (%)", min_value=0.0, step=0.1, format="%.1f") / 100
        
        with col2:
            st.subheader("🏠 Monthly Expenses")
            rent = st.number_input("Rent/Mortgage ($)", min_value=0, step=50)
            utilities = st.number_input("Utilities ($)", min_value=0, step=10)
            groceries = st.number_input("Groceries ($)", min_value=0, step=10)
            transportation = st.number_input("Transportation ($)", min_value=0, step=10)
            entertainment = st.number_input("Entertainment ($)", min_value=0, step=10)
            other = st.number_input("Other Expenses ($)", min_value=0, step=10)
            
            st.subheader("🎓 Additional Loans")
            loan_balance = st.number_input("Student/Personal Loan Balance ($)", min_value=0, step=100)
            loan_interest = st.number_input("Loan Interest Rate (%)", min_value=0.0, step=0.1, format="%.1f") / 100
        
        submitted = st.form_submit_button("🔍 Analyze My Finances", use_container_width=True)
    
    if submitted:
        if not check_environment():
            return
            
        financial_data = {
            "income": income,
            "expenses": {
                "rent": rent, "utilities": utilities, "groceries": groceries,
                "transportation": transportation, "entertainment": entertainment, "other": other
            },
            "debts": {
                "credit_card": {"balance": cc_balance, "interest_rate": cc_interest},
                "student_loan": {"balance": loan_balance, "interest_rate": loan_interest}
            },
            "savings_goal": savings_goal
        }
        
        st.session_state.current_financial_data = financial_data
        
        execute_financial_analysis(financial_data)    

    if st.session_state.financial_result and 'current_financial_data' in st.session_state:
        display_financial_results(st.session_state.financial_result, st.session_state.current_financial_data)

def execute_financial_analysis(financial_data: Dict[str, Any]) -> None:
    """Execute financial analysis with progress tracking."""
    
    status_messages = [
        "🔍 Analyzing income and expenses...",
        "📊 Evaluating debt-to-income ratios...", 
        "💡 Generating budget recommendations...",
        "📈 Creating investment strategies...",
        "✅ Finalizing your financial plan..."
    ]
    
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("🚀 Starting financial analysis...")
    
    st.session_state.progress_bar = progress_bar
    st.session_state.status_text = status_text
    
    progress_handler = create_progress_handler(status_messages)
    
    try:
        time.sleep(0.1)
        
        start_time = time.time()
        
        with st.spinner(""):
            result = financial_advisor.run_financial_analysis(financial_data)
        
        for i in range(101):
            elapsed = time.time() - start_time
            progress_handler(i, elapsed)
            time.sleep(0.01)
        
        st.session_state.financial_result = result
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        st.success("✅ Financial analysis completed!")
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
    finally:
        if 'progress_bar' in st.session_state:
            del st.session_state.progress_bar
        if 'status_text' in st.session_state:
            del st.session_state.status_text

def render_product_launcher() -> None:
    """Render Product Launch Planner interface."""
    st.markdown("""
    ### 🚀 Strategic Product Launch Planning
    Comprehensive market research, content strategy, and PR outreach planning.
    """)
    
    with st.form("product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("Product Name", help="What's your product called?")
            product_description = st.text_area("Product Description", height=100, 
                                             help="Describe your product's key features and benefits")
            target_market = st.text_input("Target Market", help="Who is your ideal customer?")
        
        with col2:
            launch_date = st.date_input("Planned Launch Date", value=date.today(), 
                                      help="When do you plan to launch?")
            budget = st.number_input("Marketing Budget ($)", min_value=100, step=1000,
                                   help="How much can you invest in marketing?")
        
        submitted = st.form_submit_button("🚀 Create Launch Plan", use_container_width=True)
    
    if submitted:
        if not all([product_name, product_description, target_market]):
            st.error("Please fill in all required fields.")
            return
            
        if not check_environment():
            return
        
        product_data = {
            "product_name": product_name,
            "product_description": product_description,
            "target_market": target_market,
            "launch_date": launch_date.isoformat(),
            "budget": budget
        }
        
        st.session_state.current_product = product_data
        
        execute_product_launch(product_data)
    
    if st.session_state.product_result:
        display_product_results(st.session_state.product_result)

def execute_product_launch(product_data: Dict[str, Any]) -> None:
    """Execute product launch planning with progress tracking."""
    status_messages = [
        "🔍 Conducting market research...",
        "📝 Analyzing competitors...",
        "📋 Creating content strategy...",
        "📞 Developing PR outreach plan...",
        "✅ Finalizing launch strategy..."
    ]
    
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("🔍 Conducting market research...")
    
    st.session_state.progress_bar = progress_bar
    st.session_state.status_text = status_text
    
    progress_handler = create_progress_handler(status_messages)
    
    try:
        time.sleep(0.1)
        
        start_time = time.time()
        
        with st.spinner(""):
            result = product_launcher.run_product_launch(product_data)
        
        for i in range(101):
            elapsed = time.time() - start_time
            progress_handler(i, elapsed)
            time.sleep(0.01)
        
        st.session_state.product_result = result
        progress_bar.progress(100)
        status_text.text("✅ Finalizing launch strategy...")
        time.sleep(0.5)
        st.success("✅ Launch plan created successfully!")
        
    except Exception as e:
        st.error(f"❌ Launch planning failed: {str(e)}")
    finally:
        if 'progress_bar' in st.session_state:
            del st.session_state.progress_bar
        if 'status_text' in st.session_state:
            del st.session_state.status_text

def render_web_researcher() -> None:
    """Render Web Researcher interface."""
    st.markdown("""
    ### 🔍 Intelligent Web Research
    Extract and analyze information from websites on specific topics.
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        website_url = st.text_input("Website URL", placeholder="https://example.com",
                                  help="Enter the website you want to research")
    
    with col2:
        st.write("")
        if st.button("🔗 Validate URL"):
            if website_url and website_url.startswith(('http://', 'https://')):
                st.success("✅ Valid URL")
            else:
                st.error("❌ Invalid URL")
    
    topic = st.text_input("Research Topic", placeholder="e.g., pricing strategy, company history",
                        help="What specific topic should I research on this website?")
    
    if st.button("🔍 Start Research", use_container_width=True):
        if not website_url or not topic:
            st.error("Please provide both website URL and research topic.")
            return
            
        if not check_environment():
            return
        
        research_data = {"website_url": website_url, "research_topic": topic}
        execute_web_research(research_data)
    
    if st.session_state.research_result:
        display_research_results(st.session_state.research_result, 
                               st.session_state.get('research_data', {}))

def execute_web_research(research_data: Dict[str, str]) -> None:
    """Execute web research with progress tracking."""
    status_messages = [
        "🌐 Connecting to website...",
        "📖 Scanning content...",
        "🔍 Analyzing relevant information...",
        "📝 Generating summary...",
        "✅ Research complete!"
    ]
    
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("🌐 Connecting to website...")
    
    st.session_state.progress_bar = progress_bar
    st.session_state.status_text = status_text
    
    progress_handler = create_progress_handler(status_messages)
    
    try:
        time.sleep(0.1)
        
        start_time = time.time()
        
        with st.spinner(""):
            result = web_researcher.run_web_research(
                research_data['website_url'],
                research_data['research_topic'])
        
        for i in range(101):
            elapsed = time.time() - start_time
            progress_handler(i, elapsed)
            time.sleep(0.01)
        
        st.session_state.research_result = result
        st.session_state.research_data = research_data
        progress_bar.progress(100)
        status_text.text("📝 Generating summary...")
        time.sleep(0.5)
        st.success("✅ Research completed!")
        
    except Exception as e:
        st.error(f"❌ Research failed: {str(e)}")
        st.error(f"Available keys in research_data: {list(research_data.keys())}")
    finally:
        if 'progress_bar' in st.session_state:
            del st.session_state.progress_bar
        if 'status_text' in st.session_state:
            del st.session_state.status_text

def render_settings() -> None:
    """Render Settings interface."""
    st.markdown("""
    ### ⚙️ Application Configuration
    Customize default settings and manage your preferences.
    """)
    
    tabs = st.tabs(["💰 Financial", "🚀 Product Launch", "🔍 Research", "🔄 Reset"])
    
    with tabs[0]:
        render_financial_settings()
    
    with tabs[1]:
        render_product_settings()
    
    with tabs[2]:
        render_research_settings()
    
    with tabs[3]:
        render_reset_settings()

def render_financial_settings() -> None:
    """Render financial settings tab."""
    st.subheader("Default Financial Settings")
    financial_data = st.session_state.user_config["financial_data"]
    
    updated_data = financial_data.copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        updated_data["income"] = st.number_input("Default Monthly Income ($)", 
                                               min_value=0, value=financial_data["income"], step=100)
        updated_data["savings_goal"] = st.number_input("Default Savings Goal ($)", 
                                                     min_value=0, value=financial_data["savings_goal"], step=50)
    
    with col2:
        updated_data['rent'] = st.number_input("Default Rent/Mortgage ($)", min_value=0, step=50)
        updated_data['utilities'] = st.number_input("Default Utilities ($)", min_value=0, step=10)
        updated_data['groceries'] = st.number_input("Default Groceries ($)", min_value=0, step=10)
        updated_data['transportation'] = st.number_input("Default Transportation ($)", min_value=0, step=10)
        updated_data['entertainment'] = st.number_input("Default Entertainment ($)", min_value=0, step=10)
        updated_data['other'] = st.number_input("Default Other Expenses ($)", min_value=0, step=10)
        
        updated_data['loan_balance'] = st.number_input("Default Student/Personal Loan Balance ($)", min_value=0, step=100)
        updated_data['loan_interest'] = st.number_input("Default Loan Interest Rate (%)", min_value=0.0, step=0.1, format="%.1f") / 100
    
    
    if st.button("💾 Save Financial Settings", use_container_width=True):
        st.session_state.user_config["financial_data"] = updated_data
        success, message = save_user_config(st.session_state.user_config)
        if success:
            st.success("✅ Financial settings saved!")
        else:
            st.error(f"❌ {message}")

def render_product_settings() -> None:
    """Render product settings tab."""
    st.subheader("Default Product Launch Settings")
    product_data = st.session_state.user_config["product_data"]
    
    updated_data = product_data.copy()
    
    updated_data["product_name"] = st.text_input("Default Product Name", value=product_data["product_name"])
    updated_data["target_market"] = st.text_input("Default Target Market", value=product_data["target_market"])
    updated_data["budget"] = st.number_input("Default Budget ($)", min_value=1000, value=product_data["budget"], step=1000)
    
    if st.button("💾 Save Product Settings", use_container_width=True):
        st.session_state.user_config["product_data"] = updated_data
        success, message = save_user_config(st.session_state.user_config)
        if success:
            st.success("✅ Product settings saved!")
        else:
            st.error(f"❌ {message}")

def render_research_settings() -> None:
    """Render research settings tab."""
    st.subheader("Default Research Settings")
    
    website_url = st.text_input("Default Website URL", value=st.session_state.user_config["website_url"])
    research_topic = st.text_input("Default Research Topic", value=st.session_state.user_config["research_topic"])
    
    if st.button("💾 Save Research Settings", use_container_width=True):
        st.session_state.user_config["website_url"] = website_url
        st.session_state.user_config["research_topic"] = research_topic
        success, message = save_user_config(st.session_state.user_config)
        if success:
            st.success("✅ Research settings saved!")
        else:
            st.error(f"❌ {message}")

def render_reset_settings() -> None:
    """Render reset settings tab."""
    st.subheader("🔄 Reset Configuration")
    st.warning("This will reset ALL settings to default values. This action cannot be undone.")
    
    if st.button("🔄 Reset All Settings", type="primary", use_container_width=True):
        success, message = reset_to_defaults()
        if success:
            st.session_state.user_config = load_user_config()
            st.success("✅ All settings reset to defaults!")
        else:
            st.error(f"❌ {message}")

def display_financial_results(result: str, financial_data: Dict[str, Any]) -> None:
    """Display financial analysis results with download options."""
    st.markdown("---")
    st.subheader("📊 Your Personalized Financial Plan")
    
    with st.container():
        st.markdown(result)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    income_info = f"income_{financial_data['income']}"
    filename = f"financial_analysis_{income_info}_{timestamp}.md"
    
    enhanced_report = f"""# Personal Financial Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Monthly Income:** ${financial_data['income']:,}
**Savings Goal:** ${financial_data['savings_goal']:,}

---

## Analysis Results

{result}

---

**Note:** This analysis is generated by AI, based on the information provided and should be used as a guide. 
Consider consulting with a financial advisor for personalized advice.
"""
    
    # Save to file
    output_path = os.path.join(OUTPUT_DIR, filename)
    if safe_file_write(output_path, enhanced_report):
        st.success(f"✅ Report saved to: `{filename}`")
    
    st.markdown("### 📥 Download Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 Download Full Report",
            data=enhanced_report,
            file_name=filename,
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        plain_text = enhanced_report.replace('#', '').replace('*', '')
        st.download_button(
            label="📝 Download as Text",
            data=plain_text,
            file_name=filename.replace('.md', '.txt'),
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.financial_result = None
            st.rerun()

def display_product_results(results: Dict[str, Any]) -> None:
    """Display product launch results with comprehensive download options."""
    st.markdown("---")
    st.subheader("🚀 Your Product Launch Strategy")
    
    with st.container():
        st.markdown(results['result'])
    
    st.markdown("### 📋 Detailed Launch Components")
    
    tab1, tab2, tab3 = st.tabs(["📊 Market Research", "📝 Content Strategy", "📞 PR & Outreach"])
    
    with tab1:
        if 'market_research.json' in results.get('files', {}):
            try:
                research_data = json.loads(results['files']['market_research.json'])
                st.json(research_data)
            except json.JSONDecodeError:
                st.code(results['files']['market_research.json'], language='json')
        else:
            st.info("📋 Market research data will be available after analysis")
    
    with tab2:
        if 'content_plan.txt' in results.get('files', {}):
            st.text_area("Content Strategy Plan", 
                        value=results['files']['content_plan.txt'], 
                        height=300, disabled=True)
        else:
            st.info("📝 Content plan will be available after analysis")
    
    with tab3:
        if 'outreach_report.md' in results.get('files', {}):
            st.markdown(results['files']['outreach_report.md'])
        else:
            st.info("📞 PR outreach plan will be available after analysis")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    product_name = "product"
    if 'current_product' in st.session_state:
        product_name = st.session_state.current_product.get('product_name', 'product')
    
    safe_name = sanitize_filename(product_name)
    
    st.markdown("### 📦 Download Launch Package")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        summary_filename = f"launch_summary_{safe_name}_{timestamp}.md"
        st.download_button(
            label="📋 Download Summary",
            data=results['result'],
            file_name=summary_filename,
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        if 'market_research.json' in results.get('files', {}):
            research_filename = f"market_research_{safe_name}_{timestamp}.json"
            st.download_button(
                label="📊 Download Research",
                data=results['files']['market_research.json'],
                file_name=research_filename,
                mime="application/json",
                use_container_width=True
            )
    
    with col3:
        if 'content_plan.txt' in results.get('files', {}):
            content_filename = f"content_plan_{safe_name}_{timestamp}.txt"
            st.download_button(
                label="📝 Download Content Plan",
                data=results['files']['content_plan.txt'],
                file_name=content_filename,
                mime="text/plain",
                use_container_width=True
            )
    
    with col4:
        if 'outreach_report.md' in results.get('files', {}):
            outreach_filename = f"pr_outreach_{safe_name}_{timestamp}.md"
            st.download_button(
                label="📞 Download PR Plan",
                data=results['files']['outreach_report.md'],
                file_name=outreach_filename,
                mime="text/markdown",
                use_container_width=True
            )
    
    if st.button("📦 Create Complete Package (ZIP)", use_container_width=True):
        zip_filename = f"launch_package_{safe_name}_{timestamp}.zip"
        create_launch_package_zip(results, zip_filename, safe_name, timestamp)
    
    if st.button("🗑️ Clear Results", use_container_width=True):
        st.session_state.product_result = None
        if 'current_product' in st.session_state:
            del st.session_state.current_product
        st.rerun()

def create_launch_package_zip(results: Dict[str, Any], zip_filename: str, safe_name: str, timestamp: str) -> None:
    """Create a complete ZIP package of all launch materials."""
    import tempfile
    import io
    
    try:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr(f"launch_summary_{safe_name}.md", results['result'])
            
            for filename, content in results.get('files', {}).items():
                if content and content.strip():  # Only add non-empty files
                    zipf.writestr(filename, content)
            
            readme_content = f"""# Product Launch Package: {safe_name}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contents:
- launch_summary_{safe_name}.md: Complete launch strategy overview
- market_research.json: Market analysis and competitor research
- content_plan.txt: Content marketing strategy
- outreach_report.md: PR and influencer outreach plan

This package was created by the Business Advisor Suite.
"""
            zipf.writestr("README.md", readme_content)
        
        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        
        st.download_button(
            label="📦 Download Complete Package",
            data=zip_data,
            file_name=zip_filename,
            mime="application/zip",
            use_container_width=True,
            help="Download all launch materials as a ZIP file"
        )
        
        st.success(f"✅ ZIP package created successfully! ({len(zip_data):,} bytes)")
        
    except Exception as e:
        st.error(f"❌ Failed to create ZIP package: {str(e)}")
        
        st.warning("Offering individual file downloads instead:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📋 Download Summary",
                data=results['result'],
                file_name=f"launch_summary_{safe_name}_{timestamp}.md",
                mime="text/markdown"
            )
        
        with col2:
            combined_content = f"""# Product Launch Package: {safe_name}

## Launch Summary
{results['result']}

## Additional Files
"""
            for filename, content in results.get('files', {}).items():
                if content:
                    combined_content += f"\n\n### {filename}\n{content}"
            
            st.download_button(
                label="📄 Download All as Text",
                data=combined_content,
                file_name=f"complete_launch_plan_{safe_name}_{timestamp}.txt",
                mime="text/plain"
            )

def display_research_results(result: str, research_data: Dict[str, str]) -> None:
    """Display research results with download options."""
    st.markdown("---")
    st.subheader("🔍 Research Findings")
    
    with st.container():
        st.markdown(result)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic = research_data.get('research_topic', 'research')
    safe_topic = sanitize_filename(topic)
    filename = f"research_{safe_topic}_{timestamp}.md"
    
    comprehensive_report = f"""# Website Research Report

**Research Topic:** {research_data.get('research_topic', 'N/A')}
**Website Analyzed:** {research_data.get('website_url', 'N/A')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Key Findings

{result}

---

*This research was conducted using the Business Advisor Suite Web Research Module*
"""
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    if safe_file_write(output_path, comprehensive_report):
        st.success(f"✅ Research saved as: `{filename}`")
    
    st.markdown("### 📥 Download Research")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 Download Full Report",
            data=comprehensive_report,
            file_name=filename,
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        plain_text = comprehensive_report.replace('#', '').replace('*', '')
        st.download_button(
            label="📝 Download as Text",
            data=plain_text,
            file_name=filename.replace('.md', '.txt'),
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.research_result = None
            st.session_state.research_data = None
            st.rerun()

def main() -> None:
    """Application entry point."""
    initialize_app()
    setup_session_state()
    
    if 'first_visit' not in st.session_state:
        st.info("👋 Welcome to Business Advisor Suite! Navigate using the sidebar to get started.")
        st.session_state.first_visit = False
    
    main_interface()

if __name__ == "__main__":
    main()