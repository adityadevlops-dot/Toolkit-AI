"""
Multi-Tool LLM Agent - Streamlit Application with 25 Tools
Clean Professional Version - Complete
"""

import streamlit as st
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Callable

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Tool Kit AI",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules with error handling
try:
    from config import Config
except ImportError:
    class Config:
        AIPIPE_API_KEY: str = os.getenv("AIPIPE_API_KEY", "")
        UPLOAD_FOLDER: str = "./uploads"
        MAX_FILE_SIZE: int = 10 * 1024 * 1024
        
        @classmethod
        def validate(cls) -> bool:
            if not cls.AIPIPE_API_KEY:
                raise ValueError("AIPIPE_API_KEY environment variable is not set")
            return True

try:
    from agent import MultiToolAgent
except ImportError:
    class MultiToolAgent:
        def __init__(self):
            self.initialized = True
        
        def process(self, query: str) -> str:
            return f"Processed: {query}"

try:
    from tools import AVAILABLE_TOOLS, get_tool_by_name
except ImportError:
    AVAILABLE_TOOLS: Dict[str, Any] = {}
    
    class BaseTool:
        """Base tool class for fallback implementation."""
        
        def __init__(self, name: str, description: str):
            self.name = name
            self.description = description
        
        def execute(self, **kwargs) -> str:
            return f"Tool '{self.name}' executed with args: {kwargs}"
    
    # Create fallback tools
    _FALLBACK_TOOLS = {
        "calculator": BaseTool("calculator", "Perform mathematical calculations"),
        "web_search": BaseTool("web_search", "Search the web"),
        "wikipedia": BaseTool("wikipedia", "Search Wikipedia"),
        "weather": BaseTool("weather", "Get weather information"),
        "file_reader": BaseTool("file_reader", "Read and analyze files"),
        "url_reader": BaseTool("url_reader", "Read content from URLs"),
        "code_executor": BaseTool("code_executor", "Execute Python code"),
        "text_summarizer": BaseTool("text_summarizer", "Summarize text"),
        "semantic_qa": BaseTool("semantic_qa", "Semantic question answering"),
        "intent_classifier": BaseTool("intent_classifier", "Classify user intent"),
        "prompt_optimizer": BaseTool("prompt_optimizer", "Optimize prompts"),
        "code_generator": BaseTool("code_generator", "Generate code"),
        "code_debugger": BaseTool("code_debugger", "Debug code"),
        "regex_tool": BaseTool("regex_tool", "Work with regular expressions"),
        "api_tester": BaseTool("api_tester", "Test APIs"),
        "dependency_analyzer": BaseTool("dependency_analyzer", "Analyze dependencies"),
        "csv_analyzer": BaseTool("csv_analyzer", "Analyze CSV data"),
        "data_visualization": BaseTool("data_visualization", "Create visualizations"),
        "json_schema_generator": BaseTool("json_schema_generator", "Generate JSON schemas"),
        "log_analyzer": BaseTool("log_analyzer", "Analyze log files"),
        "translator": BaseTool("translator", "Translate text"),
        "unit_currency_converter": BaseTool("unit_currency_converter", "Convert units and currencies"),
        "datetime_reasoner": BaseTool("datetime_reasoner", "Date and time calculations"),
        "email_writer": BaseTool("email_writer", "Write professional emails"),
        "task_planner": BaseTool("task_planner", "Plan and organize tasks"),
    }
    
    AVAILABLE_TOOLS = _FALLBACK_TOOLS
    
    def get_tool_by_name(name: str) -> Optional[BaseTool]:
        """Get a tool by its name."""
        return _FALLBACK_TOOLS.get(name)


# ============================================================================
# Constants
# ============================================================================

class SessionKeys:
    """Session state key constants."""
    ACTIVE_TOOL = "active_tool"
    AGENT = "agent"
    TOOL_RESULTS = "tool_results"
    CHAT_HISTORY = "chat_history"
    DARK_MODE = "dark_mode"


TOOL_CATEGORIES: Dict[str, list] = {
    "Core Tools": [
        {
            "name": "calculator",
            "icon": "🧮",
            "label": "Calculator",
            "desc": "Perform advanced mathematical calculations including arithmetic, algebra, calculus derivatives and integrals."
        },
        {
            "name": "web_search",
            "icon": "🔍",
            "label": "Web Search",
            "desc": "Search the web for real-time information, news, and data from multiple sources."
        },
        {
            "name": "wikipedia",
            "icon": "📚",
            "label": "Wikipedia",
            "desc": "Access the world's largest encyclopedia instantly with customizable summary lengths."
        },
        {
            "name": "weather",
            "icon": "🌤️",
            "label": "Weather",
            "desc": "Get current weather conditions and forecasts for any global location."
        },
        {
            "name": "file_reader",
            "icon": "📁",
            "label": "File Reader",
            "desc": "Upload and analyze documents in multiple formats including PDF, DOCX, TXT, CSV."
        },
        {
            "name": "url_reader",
            "icon": "🌐",
            "label": "URL Reader",
            "desc": "Extract and parse content from any web page with clean HTML extraction."
        },
    ],
    "AI & NLP": [
        {
            "name": "text_summarizer",
            "icon": "📝",
            "label": "Summarizer",
            "desc": "Transform lengthy documents into concise summaries in paragraph or bullet format."
        },
        {
            "name": "semantic_qa",
            "icon": "🧠",
            "label": "Semantic QA",
            "desc": "Build a knowledge base and ask natural language questions with RAG retrieval."
        },
        {
            "name": "intent_classifier",
            "icon": "🎯",
            "label": "Intent Classifier",
            "desc": "Automatically classify user intents from text for chatbots and automation."
        },
        {
            "name": "prompt_optimizer",
            "icon": "✨",
            "label": "Prompt Optimizer",
            "desc": "Enhance your LLM prompts for better responses with optimization strategies."
        },
        {
            "name": "translator",
            "icon": "🌍",
            "label": "Translator",
            "desc": "Translate text between 12+ languages with high accuracy and auto-detection."
        },
    ],
    "Developer": [
        {
            "name": "code_generator",
            "icon": "💻",
            "label": "Code Generator",
            "desc": "Generate production-ready code from natural language in Python, JS, SQL, and more."
        },
        {
            "name": "code_debugger",
            "icon": "🐛",
            "label": "Code Debugger",
            "desc": "Analyze code for bugs, syntax errors, and get suggested fixes."
        },
        {
            "name": "code_executor",
            "icon": "▶️",
            "label": "Code Executor",
            "desc": "Execute Python code in a secure sandbox environment instantly."
        },
        {
            "name": "regex_tool",
            "icon": "🔤",
            "label": "Regex Tool",
            "desc": "Build, test, and debug regular expressions with pattern explanations."
        },
        {
            "name": "api_tester",
            "icon": "🔌",
            "label": "API Tester",
            "desc": "Test REST APIs with full HTTP method support and response inspection."
        },
        {
            "name": "dependency_analyzer",
            "icon": "📦",
            "label": "Dependencies",
            "desc": "Analyze code dependencies and generate requirements files automatically."
        },
    ],
    "Data Tools": [
        {
            "name": "csv_analyzer",
            "icon": "📊",
            "label": "CSV Analyzer",
            "desc": "Analyze CSV datasets with statistics, distributions, and missing value reports."
        },
        {
            "name": "data_visualization",
            "icon": "📈",
            "label": "Visualization",
            "desc": "Create bar charts, line graphs, histograms, and pie charts from your data."
        },
        {
            "name": "json_schema_generator",
            "icon": "📋",
            "label": "JSON Schema",
            "desc": "Generate JSON schemas from sample data and validate JSON payloads."
        },
        {
            "name": "log_analyzer",
            "icon": "📜",
            "label": "Log Analyzer",
            "desc": "Parse and analyze log files for patterns, errors, and timelines."
        },
    ],
    "Utilities": [
        {
            "name": "unit_currency_converter",
            "icon": "💱",
            "label": "Converter",
            "desc": "Convert between units and currencies for length, weight, temperature, and more."
        },
        {
            "name": "datetime_reasoner",
            "icon": "📅",
            "label": "DateTime",
            "desc": "Perform date and time calculations, add durations, find differences."
        },
        {
            "name": "email_writer",
            "icon": "✉️",
            "label": "Email Writer",
            "desc": "Generate professional emails from 13+ templates for any business scenario."
        },
        {
            "name": "task_planner",
            "icon": "📋",
            "label": "Task Planner",
            "desc": "Plan projects with intelligent task breakdown, scheduling, and priorities."
        },
    ],
}


# ============================================================================
# CSS Styles
# ============================================================================

def apply_base_styles() -> None:
    """Apply base CSS styles to the application."""
    st.markdown("""
    <style>
        /* Light Mode (Default) - Full Reset */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e8ecf1 100%) !important;
        }
        
        body, [data-testid="stMarkdownContainer"], .stMarkdown, p, span, label, div {
            color: #262730 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #0a1428 !important;
        }
        
        /* Professional Color Scheme */
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --accent-color: #4CAF50;
        }
        
        /* Universal Button Styling */
        .stButton > button {
            width: 100%;
            height: 45px;
            font-size: 13px;
            font-weight: 600;
            margin: 2px 0;
            border-radius: 12px;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* Professional Header */
        .header-container {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            text-align: center;
            color: white;
        }
        
        .logo-text {
            font-size: 3.5em;
            font-weight: 900;
            margin: 0;
            letter-spacing: -2px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .tagline {
            font-size: 1.2em;
            margin-top: 10px;
            opacity: 0.95;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        .tool-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            border-left: 5px solid #4CAF50;
        }
        
        .tool-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin: 10px 0;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .tool-card:hover {
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
            transform: translateX(4px);
        }
        
        .result-box {
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #4CAF50;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            line-height: 1.6;
            background-color: #f8f9fa;
            color: #262730;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .category-header {
            font-weight: 700;
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Input Styling */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stSelectbox"] {
            border-radius: 10px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 10px 15px !important;
            font-size: 14px !important;
        }
        
        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 8px rgba(102, 126, 234, 0.2) !important;
        }
        
        /* Info/Success/Error Boxes */
        [data-testid="stAlert"] {
            border-radius: 12px;
            padding: 15px 20px;
            font-weight: 500;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Smooth Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
        }
        
        /* Hide card click buttons */
        .card-button-container {
            height: 0;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }
        
        .card-button-container button {
            opacity: 0;
            height: 0;
            padding: 0;
            margin: 0;
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)


def apply_dark_mode_css() -> None:
    """Apply dark mode CSS styling when dark mode is enabled."""
    if st.session_state.get(SessionKeys.DARK_MODE, False):
        st.markdown("""
        <style>
            /* Dark Mode - Full Coverage */
            
            /* Main container and backgrounds */
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0e1117 0%, #1a1f26 100%) !important;
            }
            
            [data-testid="stSidebar"] {
                background: #010409 !important;
            }
            
            /* Text colors */
            body, [data-testid="stMarkdownContainer"], .stMarkdown {
                color: #e0e0e0 !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }
            
            p, span, label, div {
                color: #e0e0e0 !important;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
            }
            
            .stButton > button:hover {
                background: linear-gradient(90deg, #7a8eea 0%, #8a5cb2 100%);
            }
            
            /* Input fields */
            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stTextArea"] textarea {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
                border-color: #404854 !important;
            }
            
            /* Selectbox and other inputs */
            [data-testid="stSelectbox"] div,
            [data-testid="stMultiSelect"] div {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
            }
            
            /* Code blocks */
            .stCode {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
            }
            
            /* Result boxes */
            .result-box {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
                border-left-color: #66BB6A !important;
            }
            
            /* Tool headers */
            .tool-header {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
            }
            
            /* Tool cards */
            .tool-card {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
                border-left-color: #667eea !important;
            }
            
            .tool-card:hover {
                background-color: #252b35 !important;
            }
            
            /* Alerts and messages */
            [data-testid="stAlert"] {
                background-color: #1e1e1e !important;
                color: #e0e0e0 !important;
            }
            
            /* Category headers */
            .category-header {
                color: #667eea !important;
            }
            
            /* Expandable sections */
            [data-testid="stExpander"] {
                background-color: #1e1e1e !important;
            }
        </style>
        """, unsafe_allow_html=True)


# ============================================================================
# Utility Functions
# ============================================================================

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: The original filename
        
    Returns:
        Sanitized filename safe for file operations
    """
    # Remove any path components
    filename = os.path.basename(filename)
    # Replace potentially dangerous characters
    return re.sub(r'[^\w\-_\.]', '_', filename)


def init_session_state() -> None:
    """Initialize all session state variables with default values."""
    defaults = {
        SessionKeys.ACTIVE_TOOL: None,
        SessionKeys.AGENT: None,
        SessionKeys.TOOL_RESULTS: {},
        SessionKeys.CHAT_HISTORY: [],
        SessionKeys.DARK_MODE: False,
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def initialize_agent() -> bool:
    """
    Initialize the MultiToolAgent.
    
    Returns:
        True if initialization successful, False otherwise
    """
    try:
        api_key = getattr(Config, 'AIPIPE_API_KEY', None) or os.getenv("AIPIPE_API_KEY", "")
        if api_key:
            st.session_state[SessionKeys.AGENT] = MultiToolAgent()
            return True
        return False
    except Exception as e:
        st.error(f"Agent initialization failed: {str(e)}")
        return False


def execute_tool_safely(tool_name: str, **kwargs) -> Optional[str]:
    """
    Execute a tool with proper error handling.
    
    Args:
        tool_name: Name of the tool to execute
        **kwargs: Arguments to pass to the tool
        
    Returns:
        Tool execution result or None if failed
    """
    try:
        tool = get_tool_by_name(tool_name)
        if tool is None:
            st.error(f"Tool '{tool_name}' not found")
            return None
        
        result = tool.execute(**kwargs)
        return result
    except Exception as e:
        st.error(f"Tool execution error: {str(e)}")
        return None


def store_result(tool_name: str, result: Optional[str]) -> None:
    """
    Store a tool result in session state.
    
    Args:
        tool_name: Name of the tool
        result: Result to store
    """
    if result is not None:
        st.session_state[SessionKeys.TOOL_RESULTS][tool_name] = result


def get_result(tool_name: str) -> Optional[str]:
    """
    Get a stored tool result from session state.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Stored result or None
    """
    return st.session_state[SessionKeys.TOOL_RESULTS].get(tool_name)


def display_result(tool_name: str, display_type: str = "code") -> None:
    """
    Display a stored tool result.
    
    Args:
        tool_name: Name of the tool
        display_type: How to display ('code', 'info', 'text', 'success')
    """
    result = get_result(tool_name)
    if result:
        st.markdown("### Result")
        if display_type == "code":
            st.code(result)
        elif display_type == "info":
            st.info(result)
        elif display_type == "success":
            st.success(result)
        elif display_type == "text":
            st.text_area("Content:", result, height=300)
        else:
            st.write(result)


# ============================================================================
# Sidebar Rendering
# ============================================================================

def render_sidebar() -> None:
    """Render the application sidebar with tool navigation."""
    with st.sidebar:
        # Professional Header with Logo
        st.markdown("""
        <div style="text-align: center; padding: 20px 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; margin-bottom: 20px;">
            <div style="font-size: 3em; margin-bottom: 10px;">🧰</div>
            <h1 style="color: white; margin: 0 0 5px 0; font-size: 1.8em;">Tool Kit AI</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.85em;">Professional LLM Agent</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme Toggle Section
        st.markdown(
            "<p style='text-align: center; font-weight: 600; color: #667eea; margin: 0 0 10px 0;'>Theme Settings</p>",
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark", use_container_width=True, key="dark_btn"):
                st.session_state[SessionKeys.DARK_MODE] = True
                st.rerun()
        
        with col2:
            if st.button("☀️ Light", use_container_width=True, key="light_btn"):
                st.session_state[SessionKeys.DARK_MODE] = False
                st.rerun()
        
        # Show current theme status
        is_dark = st.session_state.get(SessionKeys.DARK_MODE, False)
        theme_status = "🌙 Dark Mode Active" if is_dark else "☀️ Light Mode Active"
        st.markdown(
            f"<p style='text-align: center; color: #667eea; font-size: 11px; font-weight: 500; margin-top: 8px;'>{theme_status}</p>",
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Tools Section with Professional Styling
        st.markdown("<h3 style='color: #667eea; margin-bottom: 15px;'>🔧 Tools</h3>", unsafe_allow_html=True)
        
        for category, tools in TOOL_CATEGORIES.items():
            st.markdown(f"**{category}**")
            
            cols = st.columns(2)
            for i, tool in enumerate(tools):
                with cols[i % 2]:
                    is_active = st.session_state.get(SessionKeys.ACTIVE_TOOL) == tool["name"]
                    btn_type = "primary" if is_active else "secondary"
                    
                    if st.button(
                        f"{tool['icon']} {tool['label']}",
                        key=f"btn_{tool['name']}",
                        type=btn_type,
                        use_container_width=True
                    ):
                        st.session_state[SessionKeys.ACTIVE_TOOL] = tool["name"]
                        st.rerun()
            
            st.markdown("")
        
        st.markdown("---")
        
        # API Status
        api_key = getattr(Config, 'AIPIPE_API_KEY', None) or os.getenv("AIPIPE_API_KEY", "")
        if api_key:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Key Missing")
        
        st.markdown(f"**Tools Available:** {len(AVAILABLE_TOOLS)}")
        
        # Home/Reset button
        if st.button("🏠 Home", use_container_width=True):
            st.session_state[SessionKeys.ACTIVE_TOOL] = None
            st.session_state[SessionKeys.TOOL_RESULTS] = {}
            st.rerun()


# ============================================================================
# Home Page with Clean Tool Cards
# ============================================================================

def render_home() -> None:
    """Render the home page with clean, professional tool cards."""
    
    is_dark = st.session_state.get(SessionKeys.DARK_MODE, False)
    
    # Colors based on theme
    if is_dark:
        card_bg = "#1a1f2e"
        card_border = "#2d3748"
        title_color = "#f7fafc"
        desc_color = "#a0aec0"
        hover_border = "#667eea"
    else:
        card_bg = "#ffffff"
        card_border = "#e2e8f0"
        title_color = "#1a202c"
        desc_color = "#64748b"
        hover_border = "#667eea"
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 35px 20px; border-radius: 16px; margin-bottom: 25px;
                box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3); text-align: center;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 10px;">
            <span style="font-size: 2.8em;">🧰</span>
            <h1 style="margin: 0; color: white; font-size: 2.4em; font-weight: 800;">Tool Kit AI</h1>
        </div>
        <p style="color: rgba(255,255,255,0.9); font-size: 1em; margin: 0;">
            25+ Professional Tools • Powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category Icons
    category_icons = {
        "Core Tools": "🔧",
        "AI & NLP": "🤖",
        "Developer": "👨‍💻",
        "Data Tools": "📊",
        "Utilities": "🛠️",
    }
    
    # Render each category
    for category, tools in TOOL_CATEGORIES.items():
        cat_icon = category_icons.get(category, "📦")
        
        # Category Header
        st.markdown(f"""
        <div style="margin: 25px 0 12px 0;">
            <span style="color: #667eea; font-size: 1.15em; font-weight: 700;
                         border-bottom: 2px solid #667eea; padding-bottom: 5px;">
                {cat_icon} {category}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Tool Cards Grid
        cols = st.columns(3)
        
        for i, tool in enumerate(tools):
            with cols[i % 3]:
                tool_icon = tool.get("icon", "🔧")
                tool_label = tool.get("label", "Tool")
                tool_desc = tool.get("desc", "A useful tool.")
                tool_name = tool.get("name", "")
                
                # Truncate description
                max_len = 90
                if len(tool_desc) > max_len:
                    tool_desc = tool_desc[:max_len-3] + "..."
                
                # Card
                st.markdown(f"""
                <div style="
                    background: {card_bg};
                    border: 1px solid {card_border};
                    border-radius: 10px;
                    padding: 14px;
                    margin-bottom: 10px;
                    min-height: 100px;
                    transition: all 0.2s ease;
                    cursor: pointer;
                " onmouseover="
                    this.style.borderColor='{hover_border}';
                    this.style.transform='translateY(-2px)';
                    this.style.boxShadow='0 4px 15px rgba(102,126,234,0.2)';
                " onmouseout="
                    this.style.borderColor='{card_border}';
                    this.style.transform='translateY(0)';
                    this.style.boxShadow='none';
                ">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 1.5em;">{tool_icon}</span>
                        <span style="font-size: 0.95em; font-weight: 600; color: {title_color};">{tool_label}</span>
                    </div>
                    <p style="font-size: 0.75em; color: {desc_color}; margin: 0; line-height: 1.4;">
                        {tool_desc}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden button for click
                st.markdown('<div class="card-button-container">', unsafe_allow_html=True)
                if st.button("Open", key=f"card_{tool_name}"):
                    st.session_state[SessionKeys.ACTIVE_TOOL] = tool_name
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; color: #64748b; font-size: 0.8em; margin-top: 20px;">
        💡 Click any card above or use the sidebar to open a tool
    </p>
    """, unsafe_allow_html=True)


# ============================================================================
# Tool Rendering Functions
# ============================================================================

def render_calculator() -> None:
    """Render the calculator tool interface."""
    st.markdown("## 🧮 Calculator")
    st.markdown("Perform mathematical calculations, solve equations, derivatives, and integrals.")
    
    expression = st.text_input("Enter expression:", placeholder="e.g., 2+2, sqrt(16), solve x^2-4=0")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Calculate", type="primary", use_container_width=True):
            if expression:
                result = execute_tool_safely("calculator", expression=expression)
                store_result("calculator", result)
            else:
                st.warning("Please enter an expression")
    
    with col2:
        if st.button("Example: Derivative", use_container_width=True):
            result = execute_tool_safely("calculator", expression="derivative of x^3 + 2x")
            store_result("calculator", result)
    
    with col3:
        if st.button("Example: Solve", use_container_width=True):
            result = execute_tool_safely("calculator", expression="solve x^2 - 5x + 6 = 0")
            store_result("calculator", result)
    
    display_result("calculator", "code")


def render_web_search() -> None:
    """Render the web search tool interface."""
    st.markdown("## 🔍 Web Search")
    st.markdown("Search the web for information.")
    
    query = st.text_input("Search query:", placeholder="Enter your search query")
    num_results = st.slider("Number of results:", 1, 10, 5)
    
    if st.button("Search", type="primary", use_container_width=True):
        if query:
            with st.spinner("Searching..."):
                result = execute_tool_safely("web_search", query=query, num_results=num_results)
                store_result("web_search", result)
        else:
            st.warning("Please enter a search query")
    
    if get_result("web_search"):
        st.markdown("### Results")
        st.markdown(get_result("web_search"))


def render_wikipedia() -> None:
    """Render the Wikipedia search tool interface."""
    st.markdown("## 📚 Wikipedia")
    st.markdown("Search Wikipedia for information.")
    
    query = st.text_input("Search topic:", placeholder="e.g., Python programming")
    sentences = st.slider("Sentences:", 1, 10, 5)
    
    if st.button("Search", type="primary", use_container_width=True):
        if query:
            with st.spinner("Searching..."):
                result = execute_tool_safely("wikipedia", query=query, sentences=sentences)
                store_result("wikipedia", result)
        else:
            st.warning("Please enter a search topic")
    
    display_result("wikipedia", "info")


def render_weather() -> None:
    """Render the weather tool interface."""
    st.markdown("## 🌤️ Weather")
    st.markdown("Get current weather for any location.")
    
    location = st.text_input("City:", placeholder="e.g., London, New York, Tokyo")
    units = st.radio("Units:", ["celsius", "fahrenheit"], horizontal=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Get Weather", type="primary", use_container_width=True):
            if location:
                with st.spinner("Getting weather..."):
                    result = execute_tool_safely("weather", location=location, units=units)
                    store_result("weather", result)
            else:
                st.warning("Please enter a city name")
    
    with col2:
        if st.button("London", use_container_width=True):
            with st.spinner("Getting weather..."):
                result = execute_tool_safely("weather", location="London", units=units)
                store_result("weather", result)
    
    with col3:
        if st.button("New York", use_container_width=True):
            with st.spinner("Getting weather..."):
                result = execute_tool_safely("weather", location="New York", units=units)
                store_result("weather", result)
    
    if get_result("weather"):
        st.markdown("### Weather Report")
        st.info(get_result("weather"))


def render_file_reader() -> None:
    """Render the file reader tool interface with security improvements."""
    st.markdown("## 📁 File Reader")
    st.markdown("Upload and analyze files.")
    
    uploaded_file = st.file_uploader(
        "Choose a file:",
        type=["txt", "pdf", "docx", "csv", "json", "py", "md"]
    )
    
    if uploaded_file:
        try:
            upload_folder = getattr(Config, 'UPLOAD_FOLDER', './uploads')
            upload_dir = Path(upload_folder)
            upload_dir.mkdir(exist_ok=True)
            
            # Sanitize the filename
            safe_filename = sanitize_filename(uploaded_file.name)
            file_path = upload_dir / safe_filename
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"Uploaded: {safe_filename}")
            
            operation = st.selectbox("Operation:", ["read", "summary", "word_count"])
            
            if st.button("Process File", type="primary", use_container_width=True):
                with st.spinner("Processing..."):
                    result = execute_tool_safely("file_reader", file_path=str(file_path), operation=operation)
                    store_result("file_reader", result)
                    
        except PermissionError:
            st.error("Permission denied: Cannot write to upload directory")
        except Exception as e:
            st.error(f"File processing error: {str(e)}")
    
    display_result("file_reader", "text")


def render_url_reader() -> None:
    """Render the URL reader tool interface."""
    st.markdown("## 🌐 URL Reader")
    st.markdown("Extract content from web pages.")
    
    url = st.text_input("URL:", placeholder="https://example.com")
    max_length = st.slider("Max content length:", 1000, 10000, 5000)
    
    if st.button("Read URL", type="primary", use_container_width=True):
        if url:
            with st.spinner("Fetching..."):
                result = execute_tool_safely("url_reader", url=url, max_length=max_length)
                store_result("url_reader", result)
        else:
            st.warning("Please enter a URL")
    
    if get_result("url_reader"):
        st.markdown("### Content")
        st.text_area("Page content:", get_result("url_reader"), height=400)


def render_code_executor() -> None:
    """Render the code executor tool interface."""
    st.markdown("## ▶️ Code Executor")
    st.markdown("Execute Python code safely.")
    
    code = st.text_area("Python code:", height=200, placeholder="print('Hello, World!')")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Code", type="primary", use_container_width=True):
            if code:
                with st.spinner("Executing..."):
                    result = execute_tool_safely("code_executor", code=code)
                    store_result("code_executor", result)
            else:
                st.warning("Please enter some code")
    
    with col2:
        if st.button("Example: Fibonacci", use_container_width=True):
            example = """def fib(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=' ')
        a, b = b, a+b

fib(10)"""
            result = execute_tool_safely("code_executor", code=example)
            store_result("code_executor", result)
    
    if get_result("code_executor"):
        st.markdown("### Output")
        st.code(get_result("code_executor"))


def render_text_summarizer() -> None:
    """Render the text summarizer tool interface."""
    st.markdown("## 📝 Text Summarizer")
    st.markdown("Summarize long text into concise points.")
    
    text = st.text_area("Text to summarize:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        max_sentences = st.slider("Max sentences:", 1, 10, 3)
    with col2:
        style = st.selectbox("Style:", ["paragraph", "bullets", "keywords"])
    
    if st.button("Summarize", type="primary", use_container_width=True):
        if text:
            with st.spinner("Summarizing..."):
                result = execute_tool_safely(
                    "text_summarizer",
                    text=text,
                    max_sentences=max_sentences,
                    style=style
                )
                store_result("text_summarizer", result)
        else:
            st.warning("Please enter text to summarize")
    
    display_result("text_summarizer", "info")


def render_semantic_qa() -> None:
    """Render the semantic Q&A tool interface."""
    st.markdown("## 🧠 Semantic Q&A")
    st.markdown("RAG-based question answering over documents.")
    
    operation = st.selectbox("Operation:", ["ingest", "query", "clear"])
    
    if operation == "ingest":
        text = st.text_area("Document to ingest:", height=200)
        if st.button("Ingest Document", type="primary", use_container_width=True):
            if text:
                result = execute_tool_safely("semantic_qa", text=text, operation="ingest")
                store_result("semantic_qa", result)
            else:
                st.warning("Please enter document text")
    
    elif operation == "query":
        question = st.text_input("Your question:")
        top_k = st.slider("Results:", 1, 5, 3)
        if st.button("Ask", type="primary", use_container_width=True):
            if question:
                result = execute_tool_safely("semantic_qa", text=question, operation="query", top_k=top_k)
                store_result("semantic_qa", result)
            else:
                st.warning("Please enter a question")
    
    else:  # clear
        if st.button("Clear Knowledge Base", type="primary", use_container_width=True):
            result = execute_tool_safely("semantic_qa", text="clear", operation="clear")
            store_result("semantic_qa", result)
    
    display_result("semantic_qa", "info")


def render_intent_classifier() -> None:
    """Render the intent classifier tool interface."""
    st.markdown("## 🎯 Intent Classifier")
    st.markdown("Classify user intent from text.")
    
    text = st.text_input("Text to classify:", placeholder="I want to book a flight to Paris")
    custom_intents = st.text_input("Custom intents (optional):", placeholder="booking, inquiry, complaint")
    
    if st.button("Classify", type="primary", use_container_width=True):
        if text:
            result = execute_tool_safely(
                "intent_classifier",
                text=text,
                custom_intents=custom_intents if custom_intents else None
            )
            store_result("intent_classifier", result)
        else:
            st.warning("Please enter text to classify")
    
    display_result("intent_classifier", "code")


def render_prompt_optimizer() -> None:
    """Render the prompt optimizer tool interface."""
    st.markdown("## ✨ Prompt Optimizer")
    st.markdown("Optimize prompts for better LLM responses.")
    
    prompt = st.text_area("Prompt to optimize:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        task_type = st.selectbox("Task type:", ["general", "coding", "creative", "analysis", "instruction"])
    with col2:
        operation = st.selectbox("Operation:", ["optimize", "analyze", "rewrite", "score"])
    
    if st.button("Optimize", type="primary", use_container_width=True):
        if prompt:
            result = execute_tool_safely(
                "prompt_optimizer",
                prompt=prompt,
                task_type=task_type,
                operation=operation
            )
            store_result("prompt_optimizer", result)
        else:
            st.warning("Please enter a prompt to optimize")
    
    display_result("prompt_optimizer", "code")


def render_code_generator() -> None:
    """Render the code generator tool interface."""
    st.markdown("## 💻 Code Generator")
    st.markdown("Generate code from natural language.")
    
    description = st.text_area(
        "Describe what you want:",
        height=100,
        placeholder="A function to sort a list"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language:", ["python", "javascript", "html", "css", "sql", "bash"])
    with col2:
        style = st.selectbox("Style:", ["documented", "simple", "production"])
    
    if st.button("Generate", type="primary", use_container_width=True):
        if description:
            with st.spinner("Generating code..."):
                result = execute_tool_safely(
                    "code_generator",
                    description=description,
                    language=language,
                    style=style
                )
                store_result("code_generator", result)
        else:
            st.warning("Please describe what you want")
    
    if get_result("code_generator"):
        st.markdown("### Generated Code")
        st.code(get_result("code_generator"), language=language)


def render_code_debugger() -> None:
    """Render the code debugger tool interface."""
    st.markdown("## 🐛 Code Debugger")
    st.markdown("Analyze and debug code for errors.")
    
    code = st.text_area("Code to debug:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language:", ["auto", "python", "javascript"])
    with col2:
        error_message = st.text_input("Error message (optional):")
    
    if st.button("Debug", type="primary", use_container_width=True):
        if code:
            with st.spinner("Analyzing code..."):
                result = execute_tool_safely(
                    "code_debugger",
                    code=code,
                    language=language,
                    error_message=error_message if error_message else None
                )
                store_result("code_debugger", result)
        else:
            st.warning("Please enter code to debug")
    
    if get_result("code_debugger"):
        st.markdown("### Debug Report")
        st.code(get_result("code_debugger"))


def render_regex_tool() -> None:
    """Render the regex tool interface."""
    st.markdown("## 🔤 Regex Tool")
    st.markdown("Test and build regular expressions.")
    
    pattern = st.text_input("Pattern:", placeholder=r"\d+")
    text = st.text_area("Text to search:", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        operation = st.selectbox("Operation:", ["findall", "match", "replace", "split", "explain", "build"])
    with col2:
        flags = st.text_input("Flags (i, m, s):", placeholder="i")
    
    replacement: Optional[str] = None
    if operation == "replace":
        replacement = st.text_input("Replacement:")
    
    if st.button("Execute", type="primary", use_container_width=True):
        if pattern:
            result = execute_tool_safely(
                "regex_tool",
                pattern=pattern,
                text=text,
                operation=operation,
                replacement=replacement,
                flags=flags
            )
            store_result("regex_tool", result)
        else:
            st.warning("Please enter a regex pattern")
    
    display_result("regex_tool", "code")


def render_api_tester() -> None:
    """Render the API tester tool interface."""
    st.markdown("## 🔌 API Tester")
    st.markdown("Test HTTP APIs and endpoints.")
    
    url = st.text_input("API URL:", placeholder="https://api.example.com/endpoint")
    method = st.selectbox("Method:", ["GET", "POST", "PUT", "DELETE", "PATCH"])
    
    col1, col2 = st.columns(2)
    with col1:
        headers = st.text_area("Headers (JSON):", height=80, placeholder='{"Authorization": "Bearer token"}')
    with col2:
        body = st.text_area("Body (JSON):", height=80, placeholder='{"key": "value"}')
    
    if st.button("Send Request", type="primary", use_container_width=True):
        if url:
            with st.spinner("Sending request..."):
                result = execute_tool_safely(
                    "api_tester",
                    url=url,
                    method=method,
                    headers=headers if headers else None,
                    body=body if body else None
                )
                store_result("api_tester", result)
        else:
            st.warning("Please enter an API URL")
    
    if get_result("api_tester"):
        st.markdown("### Response")
        st.code(get_result("api_tester"))


def render_dependency_analyzer() -> None:
    """Render the dependency analyzer tool interface."""
    st.markdown("## 📦 Dependency Analyzer")
    st.markdown("Analyze code dependencies and imports.")
    
    code = st.text_area("Code to analyze:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language:", ["auto", "python", "javascript"])
    with col2:
        operation = st.selectbox("Operation:", ["analyze", "requirements", "tree", "security"])
    
    if st.button("Analyze", type="primary", use_container_width=True):
        if code:
            with st.spinner("Analyzing dependencies..."):
                result = execute_tool_safely(
                    "dependency_analyzer",
                    code=code,
                    language=language,
                    operation=operation
                )
                store_result("dependency_analyzer", result)
        else:
            st.warning("Please enter code to analyze")
    
    if get_result("dependency_analyzer"):
        st.markdown("### Analysis")
        st.code(get_result("dependency_analyzer"))


def render_csv_analyzer() -> None:
    """Render the CSV analyzer tool interface."""
    st.markdown("## 📊 CSV Analyzer")
    st.markdown("Analyze CSV data with statistics.")
    
    csv_input = st.text_area(
        "CSV data:",
        height=150,
        placeholder="name,age,city\nJohn,25,NYC\nJane,30,LA"
    )
    operation = st.selectbox("Operation:", ["summary", "statistics", "columns", "preview", "missing"])
    column = st.text_input("Column (for stats):", placeholder="age")
    
    if st.button("Analyze", type="primary", use_container_width=True):
        if csv_input:
            result = execute_tool_safely(
                "csv_analyzer",
                csv_data=csv_input,
                operation=operation,
                column=column if column else None
            )
            store_result("csv_analyzer", result)
        else:
            st.warning("Please enter CSV data")
    
    if get_result("csv_analyzer"):
        st.markdown("### Analysis")
        st.code(get_result("csv_analyzer"))


def render_data_visualization() -> None:
    """Render the data visualization tool interface."""
    st.markdown("## 📈 Data Visualization")
    st.markdown("Generate text-based charts.")
    
    data = st.text_input("Data (comma-separated):", placeholder="10, 25, 15, 30, 20")
    
    col1, col2 = st.columns(2)
    with col1:
        chart_type = st.selectbox(
            "Chart type:",
            ["bar", "horizontal_bar", "line", "histogram", "pie", "table"]
        )
    with col2:
        title = st.text_input("Title:", placeholder="My Chart")
    
    labels = st.text_input("Labels (comma-separated):", placeholder="A, B, C, D, E")
    
    if st.button("Create Chart", type="primary", use_container_width=True):
        if data:
            result = execute_tool_safely(
                "data_visualization",
                data=data,
                chart_type=chart_type,
                title=title if title else None,
                labels=labels if labels else None
            )
            store_result("data_visualization", result)
        else:
            st.warning("Please enter data values")
    
    if get_result("data_visualization"):
        st.markdown("### Chart")
        st.code(get_result("data_visualization"))


def render_json_schema_generator() -> None:
    """Render the JSON schema generator tool interface."""
    st.markdown("## 📋 JSON Schema Generator")
    st.markdown("Generate JSON schemas from JSON data.")
    
    json_data = st.text_area("JSON data:", height=150, placeholder='{"name": "John", "age": 30}')
    
    col1, col2 = st.columns(2)
    with col1:
        operation = st.selectbox("Operation:", ["generate", "validate", "sample", "format"])
    with col2:
        title = st.text_input("Schema title:", placeholder="MySchema")
    
    schema: Optional[str] = None
    if operation == "validate":
        schema = st.text_area("Schema for validation:", height=100)
    
    if st.button("Process", type="primary", use_container_width=True):
        if json_data:
            result = execute_tool_safely(
                "json_schema_generator",
                json_data=json_data,
                operation=operation,
                schema=schema,
                title=title if title else None
            )
            store_result("json_schema_generator", result)
        else:
            st.warning("Please enter JSON data")
    
    if get_result("json_schema_generator"):
        st.markdown("### Result")
        st.code(get_result("json_schema_generator"))


def render_log_analyzer() -> None:
    """Render the log analyzer tool interface."""
    st.markdown("## 📜 Log Analyzer")
    st.markdown("Analyze log files for patterns and errors.")
    
    log_data = st.text_area("Log data:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        operation = st.selectbox("Operation:", ["summary", "errors", "patterns", "timeline", "search", "stats"])
    with col2:
        search_term = st.text_input("Search term:", placeholder="error")
    
    if st.button("Analyze", type="primary", use_container_width=True):
        if log_data:
            result = execute_tool_safely(
                "log_analyzer",
                log_data=log_data,
                operation=operation,
                search_term=search_term if search_term else None
            )
            store_result("log_analyzer", result)
        else:
            st.warning("Please enter log data")
    
    if get_result("log_analyzer"):
        st.markdown("### Analysis")
        st.code(get_result("log_analyzer"))


def render_translator() -> None:
    """Render the translator tool interface."""
    st.markdown("## 🌍 Translator")
    st.markdown("Translate text between languages.")
    
    text = st.text_area("Text to translate:", height=100)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        source_lang = st.selectbox(
            "From:",
            ["auto", "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "hi", "ar"]
        )
    with col2:
        target_lang = st.selectbox(
            "To:",
            ["es", "en", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "hi", "ar"]
        )
    with col3:
        operation = st.selectbox("Operation:", ["translate", "detect", "languages", "phrases"])
    
    if st.button("Translate", type="primary", use_container_width=True):
        if text or operation in ["languages", "phrases"]:
            result = execute_tool_safely(
                "translator",
                text=text if text else "hello",
                source_lang=source_lang,
                target_lang=target_lang,
                operation=operation
            )
            store_result("translator", result)
        else:
            st.warning("Please enter text to translate")
    
    display_result("translator", "info")


def render_unit_currency_converter() -> None:
    """Render the unit and currency converter tool interface."""
    st.markdown("## 💱 Unit & Currency Converter")
    st.markdown("Convert between units and currencies.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        value = st.number_input("Value:", value=1.0)
    with col2:
        from_unit = st.text_input("From:", placeholder="km, usd, celsius")
    with col3:
        to_unit = st.text_input("To:", placeholder="miles, eur, fahrenheit")
    
    category = st.selectbox(
        "Category:",
        ["auto", "length", "weight", "temperature", "volume", "area", "time", "data", "currency"]
    )
    
    if st.button("Convert", type="primary", use_container_width=True):
        if from_unit and to_unit:
            result = execute_tool_safely(
                "unit_currency_converter",
                value=value,
                from_unit=from_unit,
                to_unit=to_unit,
                category=category
            )
            store_result("unit_currency_converter", result)
        else:
            st.warning("Please enter both from and to units")
    
    display_result("unit_currency_converter", "success")


def render_datetime_reasoner() -> None:
    """Render the datetime reasoner tool interface."""
    st.markdown("## 📅 Date-Time Reasoner")
    st.markdown("Perform date and time calculations.")
    
    query = st.text_input("Query:", placeholder="today, 2024-01-15, 5 days from now")
    operation = st.selectbox(
        "Operation:",
        ["now", "parse", "difference", "add", "subtract", "weekday", "info", "format"]
    )
    
    # Initialize variables with defaults to avoid undefined variable errors
    amount: int = 1
    unit: str = "days"
    date2: Optional[str] = None
    
    # Conditional inputs based on operation
    if operation in ["add", "subtract"]:
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount:", value=1, min_value=1)
        with col2:
            unit = st.selectbox("Unit:", ["days", "weeks", "months", "years", "hours", "minutes"])
    elif operation == "difference":
        date2 = st.text_input("Second date:", placeholder="2024-12-31")
    
    if st.button("Calculate", type="primary", use_container_width=True):
        try:
            if operation in ["add", "subtract"]:
                result = execute_tool_safely(
                    "datetime_reasoner",
                    query=query,
                    operation=operation,
                    date1=query,
                    amount=amount,
                    unit=unit
                )
            elif operation == "difference":
                if not date2:
                    st.warning("Please provide a second date for difference calculation")
                    return
                result = execute_tool_safely(
                    "datetime_reasoner",
                    query=query,
                    operation=operation,
                    date1=query,
                    date2=date2
                )
            else:
                result = execute_tool_safely(
                    "datetime_reasoner",
                    query=query if query else "now",
                    operation=operation
                )
            
            store_result("datetime_reasoner", result)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    display_result("datetime_reasoner", "code")


def render_email_writer() -> None:
    """Render the email writer tool interface."""
    st.markdown("## ✉️ Email Writer")
    st.markdown("Generate professional emails.")
    
    col1, col2 = st.columns(2)
    with col1:
        email_type = st.selectbox("Email type:", [
            "business", "follow_up", "thank_you", "apology", "request",
            "introduction", "meeting", "complaint", "resignation",
            "cover_letter", "cold_outreach", "reminder", "congratulations"
        ])
        recipient_name = st.text_input("Recipient:", placeholder="John Doe")
        sender_name = st.text_input("Sender:", placeholder="Your Name")
    
    with col2:
        subject = st.text_input("Subject:", placeholder="Meeting Request")
        company = st.text_input("Company:", placeholder="ABC Corp")
        tone = st.selectbox("Tone:", ["professional", "formal", "friendly", "casual"])
    
    key_points = st.text_input("Key points (comma-separated):", placeholder="point 1, point 2, point 3")
    
    if st.button("Generate Email", type="primary", use_container_width=True):
        result = execute_tool_safely(
            "email_writer",
            email_type=email_type,
            recipient_name=recipient_name if recipient_name else None,
            sender_name=sender_name if sender_name else None,
            subject=subject if subject else None,
            key_points=key_points if key_points else None,
            tone=tone,
            company=company if company else None
        )
        store_result("email_writer", result)
    
    if get_result("email_writer"):
        st.markdown("### Generated Email")
        st.code(get_result("email_writer"))


def render_task_planner() -> None:
    """Render the task planner tool interface."""
    st.markdown("## 📋 Task Planner")
    st.markdown("Plan and organize tasks with priorities.")
    
    task = st.text_input("Main task/project:", placeholder="Build a website")
    
    col1, col2 = st.columns(2)
    with col1:
        operation = st.selectbox("Operation:", [
            "create", "breakdown", "schedule", "prioritize",
            "estimate", "timeline", "dependencies", "daily_plan"
        ])
        priority = st.selectbox("Priority:", ["high", "medium", "low"])
    
    with col2:
        deadline = st.text_input("Deadline (YYYY-MM-DD):", placeholder="2024-12-31")
        hours_available = st.number_input("Hours/day:", value=8, min_value=1, max_value=16)
    
    subtasks = st.text_input("Subtasks (comma-separated):", placeholder="design, develop, test")
    
    if st.button("Plan", type="primary", use_container_width=True):
        if task:
            result = execute_tool_safely(
                "task_planner",
                task=task,
                operation=operation,
                subtasks=subtasks if subtasks else None,
                deadline=deadline if deadline else None,
                priority=priority,
                hours_available=hours_available
            )
            store_result("task_planner", result)
        else:
            st.warning("Please enter a task or project")
    
    if get_result("task_planner"):
        st.markdown("### Plan")
        st.code(get_result("task_planner"))


# ============================================================================
# Tool Renderer Mapping
# ============================================================================

TOOL_RENDERERS: Dict[str, Callable[[], None]] = {
    "calculator": render_calculator,
    "web_search": render_web_search,
    "wikipedia": render_wikipedia,
    "weather": render_weather,
    "file_reader": render_file_reader,
    "url_reader": render_url_reader,
    "code_executor": render_code_executor,
    "text_summarizer": render_text_summarizer,
    "semantic_qa": render_semantic_qa,
    "intent_classifier": render_intent_classifier,
    "prompt_optimizer": render_prompt_optimizer,
    "code_generator": render_code_generator,
    "code_debugger": render_code_debugger,
    "regex_tool": render_regex_tool,
    "api_tester": render_api_tester,
    "dependency_analyzer": render_dependency_analyzer,
    "csv_analyzer": render_csv_analyzer,
    "data_visualization": render_data_visualization,
    "json_schema_generator": render_json_schema_generator,
    "log_analyzer": render_log_analyzer,
    "translator": render_translator,
    "unit_currency_converter": render_unit_currency_converter,
    "datetime_reasoner": render_datetime_reasoner,
    "email_writer": render_email_writer,
    "task_planner": render_task_planner,
}


# ============================================================================
# Main Function
# ============================================================================

def main() -> None:
    """Main Streamlit application entry point."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        st.warning(f"Configuration warning: {str(e)}")
        st.info("Some features may be limited without API configuration.")
    except Exception as e:
        st.error(f"Configuration error: {str(e)}")
    
    # Initialize session state
    init_session_state()
    
    # Initialize agent if not already done
    if st.session_state.get(SessionKeys.AGENT) is None:
        initialize_agent()
    
    # Apply CSS styles
    apply_base_styles()
    apply_dark_mode_css()
    
    # Render sidebar
    render_sidebar()
    
    # Get active tool and render appropriate view
    active_tool = st.session_state.get(SessionKeys.ACTIVE_TOOL)
    
    if active_tool and active_tool in TOOL_RENDERERS:
        TOOL_RENDERERS[active_tool]()
    else:
        render_home()


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()