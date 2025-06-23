# 💼 Business Advisor Suite

A comprehensive AI-powered business strategy and financial planning platform built with CrewAI and Streamlit.

## 🌟 Features

### 💰 Financial Advisor

- **Comprehensive Budget Analysis**: Detailed expense breakdown and optimization recommendations
- **Investment Strategy Planning**: Portfolio allocation with compound growth projections
- **Debt Management**: Mathematical debt elimination strategies with payment schedules
- **Financial Ratios & Metrics**: Automated calculation of key financial health indicators
- **Interactive Reports**: Downloadable financial plans with tables and calculations

### 🚀 Product Launch Planner

- **Market Research**: AI-powered competitor analysis and target demographic identification
- **Content Strategy**: Blog posts, social media content, and promotional material creation
- **PR & Outreach**: Influencer and media contact strategies
- **Launch Timeline**: Comprehensive project planning with budget allocation
- **Complete Launch Package**: Downloadable ZIP with all planning materials

### 🔍 Website Researcher

- **Intelligent Content Analysis**: Deep website content extraction and analysis
- **Topic-Focused Research**: Specific information gathering on user-defined topics
- **Structured Reports**: Well-organized findings with source citations
- **Quality Metrics**: Research completeness and depth assessment
- **Export Options**: Multiple download formats (Markdown, Text, PDF-ready)

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Framework**: CrewAI with multi-agent orchestration
- **LLM**: Azure OpenAI (GPT-4)
- **Tools**: DuckDuckGo Search, Website Scraping, Content Analysis
- **Data Validation**: Pydantic models
- **Configuration**: JSON-based user settings with persistence

## 📋 Prerequisites

- Python 3.11
- Azure OpenAI API access
- Internet connection for web research capabilities

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/palaemezie/Agentic-Business-Advisor.git
cd Business_Advisor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env

AZURE_API_KEY=your_azure_api_key
AZURE_API_BASE=your_azure_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_API_VERSION=your_azure_api_version

```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📂 Project Structure

```
Business_Advisor/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── config.py              # Default configuration values
│   ├── config_manager.py      # User configuration management
│   ├── utils.py               # Azure LLM setup and utilities
│   ├── financial_advisor.py   # Financial analysis crew
│   ├── product_launcher.py    # Product launch planning crew
│   └── web_researcher.py      # Web research crew
└── outputs/                   # Generated reports (auto-created)
    ├── user_config.json       # User preferences
    └── *.md, *.txt, *.json    # Generated analysis files
```

## 💡 Usage Guide

### Financial Analysis

1. Navigate to **Financial Advisor** in the sidebar
2. Input your income, expenses, debts, and savings goals
3. Click **Analyze My Finances** to generate a comprehensive financial plan
4. Download your personalized report in multiple formats

### Product Launch Planning

1. Go to **Product Launch Planner**
2. Enter product details, target market, and budget
3. Click **Create Launch Plan** for market research, content strategy, and PR planning
4. Download individual components or complete launch package

### Website Research

1. Select **Website Researcher**
2. Enter the website URL and specific research topic
3. Click **Start Research** for AI-powered content analysis
4. Review structured findings and download detailed reports

### Settings Management

- Access **Settings** to customize default values
- Save frequently used configurations
- Reset to factory defaults when needed

## 🔧 Configuration

### Default Settings

The application comes with pre-configured defaults that can be customized:

- **Financial**: Sample income, expenses, and debt scenarios
- **Product Launch**: Template product information and budgets
- **Research**: Default websites and topics for quick testing

### User Preferences

- Settings are automatically saved to `outputs/user_config.json`
- Configurations persist between sessions
- Individual module settings can be customized independently

## 📊 Output Files

### Financial Advisor

- `financial_analysis_*.md`: Comprehensive financial plans
- Includes budget tables, investment projections, and debt strategies

### Product Launch Planner

- `launch_summary_*.md`: Complete launch strategy overview
- `market_research.json`: Competitor and market analysis data
- `content_plan.txt`: Content marketing strategy
- `outreach_report.md`: PR and influencer outreach plans
- `launch_package_*.zip`: Complete launch materials package

### Website Researcher

- `research_*.md`: Structured research findings
- Topic-focused analysis with source citations
- Quality metrics and research completeness indicators

## 🤖 AI Agents & Crews

### Financial Advisor Crew

- **Budgeting Agent**: Mathematical analysis and budget optimization
- **Investment Agent**: Portfolio recommendations with projections
- **Debt Management Agent**: Debt elimination strategies and calculations

### Product Launch Crew

- **Market Researcher**: Target demographics and competitor analysis
- **Content Creator**: Blog posts, social media, and promotional content
- **PR Specialist**: Influencer outreach and media relations

### Web Research Crew

- **Research Analyst**: Systematic content extraction and analysis
- **Content Analyzer**: Structure and quality assessment

## 🔒 Security & Privacy

- Environment variables for secure API key storage
- No data persistence of sensitive financial information
- Local file storage for generated reports
- User configurations stored locally only

## 🛠️ Troubleshooting

### Common Issues

**Environment Variables Not Set**

- Ensure `.env` file exists with correct Azure credentials
- Verify Azure OpenAI deployment names match configuration

**Import Errors**

- Run `pip install -r requirements.txt` to install dependencies
- Check Python version compatibility (3.11)

**API Rate Limits**

- Azure OpenAI, and DuckDuckGo may have rate limits based on your subscription
- Wait and retry if you encounter temporary limits

**Web Research Failures**

- Verify website URLs are accessible
- Some websites may block automated access
- Try alternative URLs or topics

### Performance Optimization

- The app uses Streamlit caching for better performance
- Large analysis tasks may take 30-60 seconds
- Progress bars show real-time status updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the GitHub repository

- Check the troubleshooting section above

- Review the Azure OpenAI documentation for API-related issues

## 🔮 Future Enhancements

- [ ] Additional LLM provider support (OpenAI, Anthropic)
- [ ] Advanced financial planning features (retirement, insurance)
- [ ] Multi-language support
- [ ] API integration for real-time market data
- [ ] Enhanced export formats (PDF, Excel)
- [ ] Team collaboration features
- [ ] Historical analysis tracking

---

**Built with ❤️ using CrewAI, Streamlit, and Azure OpenAI**
