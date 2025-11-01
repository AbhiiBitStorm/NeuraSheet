import streamlit as st
import pandas as pd
from pathlib import Path
import time
from tools import ExcelTools
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AI Excel Agent 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ADVANCED CSS WITH ANIMATIONS
# ============================================
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background with Gradient Animation */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Main Header with Typing Animation */
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #667eea); }
        to { filter: drop-shadow(0 0 20px #764ba2); }
    }
    
    /* Animated Agent Avatar */
    .agent-avatar {
        width: 120px;
        height: 120px;
        margin: 0 auto;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Animated Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover:before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Chat Message Bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.5s ease;
    }
    
    .agent-message {
        background: rgba(255, 255, 255, 0.95);
        color: #333;
        padding: 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Upload Zone */
    .upload-zone {
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
        animation: borderPulse 2s ease-in-out infinite;
    }
    
    @keyframes borderPulse {
        0%, 100% { border-color: #667eea; }
        50% { border-color: #764ba2; }
    }
    
    .upload-zone:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: scale(1.02);
    }
    
    .upload-icon {
        font-size: 5rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    /* Success/Error Alerts */
    .success-alert {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
        animation: slideInDown 0.5s ease;
    }
    
    .error-alert {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(235, 51, 73, 0.4);
        animation: shake 0.5s ease;
    }
    
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Loading Spinner */
    .loader {
        border: 5px solid rgba(255, 255, 255, 0.3);
        border-top: 5px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 1rem 2rem;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 2px solid #667eea;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Radio Buttons */
    .stRadio>div {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 15px;
    }
    
    /* Navigation Items */
    .nav-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateX(10px);
    }
    
    /* Floating Action Button */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        cursor: pointer;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Particle Background Effect */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    </style>
""", unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================
def process_chat_command(command, df):
    """Process user chat commands"""
    command_lower = command.lower()
    
    try:
        if 'sum' in command_lower or 'total' in command_lower:
            for col in df.columns:
                if col.lower() in command_lower:
                    result = df[col].sum()
                    return f"✅ Sum of **{col}**: **{result:,}**"
            return "❌ Column not found. Please specify column name."
        
        elif 'average' in command_lower or 'mean' in command_lower:
            for col in df.columns:
                if col.lower() in command_lower:
                    result = df[col].mean()
                    return f"✅ Average of **{col}**: **{result:.2f}**"
            return "❌ Column not found."
        
        elif 'count' in command_lower or 'rows' in command_lower:
            return f"✅ Total rows: **{len(df)}**"
        
        elif 'columns' in command_lower or 'column' in command_lower:
            return f"✅ Columns: **{', '.join(df.columns)}**"
        
        elif 'max' in command_lower or 'maximum' in command_lower:
            for col in df.columns:
                if col.lower() in command_lower:
                    result = df[col].max()
                    return f"✅ Maximum of **{col}**: **{result}**"
            return "❌ Column not found."
        
        elif 'min' in command_lower or 'minimum' in command_lower:
            for col in df.columns:
                if col.lower() in command_lower:
                    result = df[col].min()
                    return f"✅ Minimum of **{col}**: **{result}**"
            return "❌ Column not found."
        
        else:
            return """🤔 I can help you with:
            
**📊 Data Analysis:**
- "sum of [column]" - Calculate total
- "average of [column]" - Find mean
- "max of [column]" - Find maximum
- "min of [column]" - Find minimum

**ℹ️ Information:**
- "count rows" - Total number of rows
- "show columns" - List all columns

**💡 Example:** "What is the sum of Salary column?"
"""
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

def typing_effect(text):
    """Simulate typing effect"""
    placeholder = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(0.01)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'excel_tools' not in st.session_state:
    st.session_state.excel_tools = ExcelTools()
if 'file_loaded' not in st.session_state:
    st.session_state.file_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# ============================================
# SIDEBAR - AGENT CONTROL PANEL
# ============================================
with st.sidebar:
    # Agent Avatar
    st.markdown("""
        <div class="agent-avatar">
            🤖
        </div>
        <h2 style='text-align: center; margin-top: 1rem;'>AI Excel Agent</h2>
        <p style='text-align: center; color: #666;'>Powered by Mistral 7B</p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🎯 Navigation Panel")
    
    page = st.radio(
        "",
        ["🏠 Dashboard", "📤 Upload Data", "💬 AI Assistant", "📊 Analytics", "⚙️ Operations", "🎨 Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Status Indicator
    if st.session_state.file_loaded:
        st.markdown("""
            <div class="success-alert">
                ✅ <strong>Status:</strong> Active<br>
                📁 <strong>File:</strong> Loaded<br>
                🔋 <strong>Agent:</strong> Ready
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Data", key="clear_sidebar"):
            st.session_state.file_loaded = False
            st.session_state.df = None
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown("""
            <div style="background: rgba(255,193,7,0.2); padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107;">
                ⚠️ <strong>No Data Loaded</strong><br>
                Please upload an Excel file
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    if st.session_state.file_loaded:
        st.markdown("### 📈 Quick Stats")
        df = st.session_state.df
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", len(df), delta=None)
        with col2:
            st.metric("Columns", len(df.columns), delta=None)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.8rem;'>
            <p>Made with ❤️</p>
            <p>Version 2.0</p>
            <p>© 2024 AI Excel Agent</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# PAGE 1: DASHBOARD
# ============================================
if page == "🏠 Dashboard":
    # Header with Animation
    st.markdown('<h1 class="main-header">🤖 AI Excel Agent Dashboard</h1>', unsafe_allow_html=True)
    
    # Welcome Message
    st.markdown("""
        <div class="glass-card">
            <h2 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                👋 Welcome to Your AI-Powered Excel Assistant
            </h2>
            <p style='font-size: 1.2rem; color: #555;'>
                Transform your Excel data into insights with the power of AI. Upload, analyze, and interact with your data like never before!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("### ✨ Powerful Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="glass-card">
                <div style='text-align: center; font-size: 3rem; margin-bottom: 1rem;'>📤</div>
                <h3 style='text-align: center; color: #667eea;'>Smart Upload</h3>
                <p style='text-align: center; color: #666;'>
                    Drag & drop Excel files with instant preview and validation
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="glass-card">
                <div style='text-align: center; font-size: 3rem; margin-bottom: 1rem;'>💬</div>
                <h3 style='text-align: center; color: #667eea;'>AI Chat</h3>
                <p style='text-align: center; color: #666;'>
                    Ask questions in natural language and get instant answers
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="glass-card">
                <div style='text-align: center; font-size: 3rem; margin-bottom: 1rem;'>📊</div>
                <h3 style='text-align: center; color: #667eea;'>Visual Analytics</h3>
                <p style='text-align: center; color: #666;'>
                    Beautiful charts and graphs generated automatically
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Capabilities Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="glass-card">
                <h3>🎯 Data Operations</h3>
                <ul style='font-size: 1.1rem; line-height: 2;'>
                    <li>✅ Read & Write Excel Files</li>
                    <li>✅ Advanced Filtering & Sorting</li>
                    <li>✅ Column Management</li>
                    <li>✅ Data Cleaning & Validation</li>
                    <li>✅ Export to Multiple Formats</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="glass-card">
                <h3>🧮 Advanced Analytics</h3>
                <ul style='font-size: 1.1rem; line-height: 2;'>
                    <li>✅ Statistical Analysis</li>
                    <li>✅ Sum, Average, Min, Max</li>
                    <li>✅ Correlation Matrix</li>
                    <li>✅ Interactive Visualizations</li>
                    <li>✅ Trend Analysis</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Getting Started
    st.markdown("""
        <div class="glass-card" style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);'>
            <h2 style='text-align: center; color: #667eea;'>🚀 Get Started in 3 Easy Steps</h2>
            <div style='display: flex; justify-content: space-around; margin-top: 2rem;'>
                <div style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>1️⃣</div>
                    <h4>Upload File</h4>
                    <p style='color: #666;'>Go to Upload Data</p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>2️⃣</div>
                    <h4>Chat with AI</h4>
                    <p style='color: #666;'>Ask questions</p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>3️⃣</div>
                    <h4>Visualize Data</h4>
                    <p style='color: #666;'>View analytics</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Now - Upload Your First File", key="cta_upload"):
            st.session_state.nav = "📤 Upload Data"
            st.rerun()

# ============================================
# PAGE 2: UPLOAD DATA
# ============================================
elif page == "📤 Upload Data":
    st.markdown('<h1 class="main-header">📤 Upload Your Excel File</h1>', unsafe_allow_html=True)
    
    # Upload Zone
    uploaded_file = st.file_uploader(
        "",
        type=['xlsx', 'xls'],
        help="Upload your Excel file here",
        label_visibility="collapsed"
    )
    
    if uploaded_file is None:
        st.markdown("""
            <div class="upload-zone">
                <div class="upload-icon">📁</div>
                <h2 style='color: #667eea; margin-top: 1rem;'>Drag & Drop Your Excel File</h2>
                <p style='color: #666; font-size: 1.2rem;'>or click to browse</p>
                <p style='color: #999;'>Supported formats: .xlsx, .xls</p>
            </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Show loading animation
            with st.spinner(''):
                st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
                time.sleep(1)
            
            # Save and read file
            temp_path = Path("temp_upload.xlsx")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            df = pd.read_excel(temp_path)
            st.session_state.df = df
            st.session_state.file_loaded = True
            st.session_state.excel_tools.df = df
            
            # Success message
            st.markdown(f"""
                <div class="success-alert">
                    <h3>✅ File Uploaded Successfully!</h3>
                    <p><strong>Filename:</strong> {uploaded_file.name}</p>
                    <p><strong>Upload Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics Cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Rows</div>
                        <div class="metric-value">{len(df)}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <div class="metric-label">Columns</div>
                        <div class="metric-value">{len(df.columns)}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        <div class="metric-label">File Size</div>
                        <div class="metric-value">{uploaded_file.size / 1024:.1f}</div>
                        <div class="metric-label">KB</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                memory_usage = df.memory_usage(deep=True).sum() / 1024
                st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                        <div class="metric-label">Memory</div>
                        <div class="metric-value">{memory_usage:.1f}</div>
                        <div class="metric-label">KB</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Data Preview
            st.markdown("""
                <div class="glass-card">
                    <h2 style='color: #667eea;'>👀 Data Preview</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Column Information
            st.markdown("""
                <div class="glass-card">
                    <h2 style='color: #667eea;'>📋 Column Information</h2>
                </div>
            """, unsafe_allow_html=True)
            
            col_info = pd.DataFrame({
                'Column Name': df.columns,
                'Data Type': df.dtypes.values,
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values,
                'Unique Values': [df[col].nunique() for col in df.columns]
            })
            
            st.dataframe(col_info, use_container_width=True)
            
            # Download Section
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name='data.csv',
                    mime='text/csv',
                )
            
            with col2:
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_data,
                    file_name='data.json',
                    mime='application/json',
                )
            
            with col3:
                if st.button("🔄 Upload New File"):
                    st.session_state.file_loaded = False
                    st.session_state.df = None
                    st.rerun()
            
        except Exception as e:
            st.markdown(f"""
                <div class="error-alert">
                    <h3>❌ Error Loading File</h3>
                    <p>{str(e)}</p>
                </div>
            """, unsafe_allow_html=True)

# ============================================
# PAGE 3: AI ASSISTANT (CHAT)
# ============================================
elif page == "💬 AI Assistant":
    st.markdown('<h1 class="main-header">💬 AI Chat Assistant</h1>', unsafe_allow_html=True)
    
    if not st.session_state.file_loaded:
        st.markdown("""
            <div class="error-alert">
                <h3>⚠️ No Data Loaded</h3>
                <p>Please upload an Excel file first from the <strong>Upload Data</strong> page.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📤 Go to Upload Page"):
            st.rerun()
    
    else:
        # Chat Interface
        st.markdown("""
            <div class="glass-card">
                <h3 style='color: #667eea;'>💡 Ask me anything about your data!</h3>
                <p style='color: #666;'>Examples: "What is the sum of Sales?", "Show average of Age", "Count total rows"</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Chat History
        chat_container = st.container()
        
        with chat_container:
            for chat in st.session_state.chat_history:
                if chat['role'] == 'user':
                    st.markdown(f"""
                        <div class="user-message">
                            <strong>🧑 You:</strong><br>
                            {chat['message']}
                        </div>
                        <div style='clear: both;'></div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="agent-message">
                            <strong>🤖 Agent:</strong><br>
                            {chat['message']}
                        </div>
                        <div style='clear: both;'></div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Input Area
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "",
                placeholder="Type your question here... (e.g., 'sum of Salary column')",
                key="chat_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send 📤", use_container_width=True)
        
        if send_button and user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'message': user_input
            })
            
            # Process command
            response = process_chat_command(user_input, st.session_state.df)
            
            # Add agent response
            st.session_state.chat_history.append({
                'role': 'agent',
                'message': response
            })
            
            st.rerun()
        
        # Quick Actions
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Show Summary", use_container_width=True):
                summary = st.session_state.df.describe()
                st.dataframe(summary, use_container_width=True)
        
        with col2:
            if st.button("🔢 Count Rows", use_container_width=True):
                st.success(f"Total Rows: {len(st.session_state.df)}")
        
        with col3:
            if st.button("📋 List Columns", use_container_width=True):
                st.info(f"Columns: {', '.join(st.session_state.df.columns)}")
        
        with col4:
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

# ============================================
# PAGE 4: ANALYTICS
# ============================================
elif page == "📊 Analytics":
    st.markdown('<h1 class="main-header">📊 Data Analytics & Visualization</h1>', unsafe_allow_html=True)
    
    if not st.session_state.file_loaded:
        st.warning("⚠️ Please upload an Excel file first!")
    else:
        df = st.session_state.df
        
        # Summary Statistics
        st.markdown("""
            <div class="glass-card">
                <h2 style='color: #667eea;'>📈 Statistical Summary</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df.describe(), use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("""
            <div class="glass-card">
                <h2 style='color: #667eea;'>📊 Interactive Visualizations</h2>
            </div>
        """, unsafe_allow_html=True)
        
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        if numeric_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_col = st.selectbox("📌 Select Column:", numeric_cols)
            
            with col2:
                chart_type = st.selectbox("📊 Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart", "Histogram", "Box Plot"])
            
            # Create chart based on selection
            if chart_type == "Bar Chart":
                fig = px.bar(
                    df,
                    y=selected_col,
                    title=f"{selected_col} - Bar Chart",
                    color_discrete_sequence=['#667eea']
                )
            elif chart_type == "Line Chart":
                fig = px.line(
                    df,
                    y=selected_col,
                    title=f"{selected_col} - Line Chart",
                    color_discrete_sequence=['#764ba2']
                )
            elif chart_type == "Pie Chart":
                fig = px.pie(
                    df,
                    names=df.columns[0],
                    values=selected_col,
                    title=f"{selected_col} - Distribution"
                )
            elif chart_type == "Box Plot":
                fig = px.box(
                    df,
                    y=selected_col,
                    title=f"{selected_col} - Box Plot",
                    color_discrete_sequence=['#f093fb']
                )
            else:
                fig = px.histogram(
                    df,
                    x=selected_col,
                    title=f"{selected_col} - Distribution",
                    color_discrete_sequence=['#4facfe']
                )
            
            fig.update_layout(
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Correlation Matrix
            if len(numeric_cols) > 1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                    <div class="glass-card">
                        <h2 style='color: #667eea;'>🔗 Correlation Heatmap</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                corr = df[numeric_cols].corr()
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    title="Correlation Matrix",
                    color_continuous_scale='RdBu'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ No numeric columns found for visualization")

# ============================================
# PAGE 5: OPERATIONS
# ============================================
elif page == "⚙️ Operations":
    st.markdown('<h1 class="main-header">⚙️ Data Operations</h1>', unsafe_allow_html=True)
    
    if not st.session_state.file_loaded:
        st.warning("⚠️ Please upload an Excel file first!")
    else:
        df = st.session_state.df
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Filter", "↕️ Sort", "➕ Add Column", "🧮 Calculate"])
        
        # TAB 1: Filter
        with tab1:
            st.markdown("""
                <div class="glass-card">
                    <h2 style='color: #667eea;'>🔍 Filter Your Data</h2>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                filter_col = st.selectbox("Select Column:", df.columns, key="filter_col")
            with col2:
                filter_val = st.text_input("Enter Value:", key="filter_val")
            
            if st.button("Apply Filter", key="apply_filter"):
                filtered_df = df[df[filter_col].astype(str).str.contains(filter_val, case=False, na=False)]
                st.dataframe(filtered_df, use_container_width=True, height=400)
                st.success(f"✅ Found {len(filtered_df)} matching rows")
        
        # TAB 2: Sort
        with tab2:
            st.markdown("""
                <div class="glass-card">
                    <h2 style='color: #667eea;'>↕️ Sort Your Data</h2>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                sort_col = st.selectbox("Select Column:", df.columns, key="sort_col")
            with col2:
                sort_order = st.radio("Order:", ["Ascending ⬆️", "Descending ⬇️"], key="sort_order")
            
            if st.button("Apply Sort", key="apply_sort"):
                sorted_df = df.sort_values(by=sort_col, ascending=("Ascending" in sort_order))
                st.session_state.df = sorted_df
                st.dataframe(sorted_df, use_container_width=True, height=400)
                st.success("✅ Data sorted successfully!")
        
        # TAB 3: Add Column
        with tab3:
            st.markdown("""
                <div class="glass-card">
                    <h2 style='color: #667eea;'>➕ Add New Column</h2>
                </div>
            """, unsafe_allow_html=True)
            
            new_col_name = st.text_input("Column Name:", key="new_col_name")
            new_col_value = st.text_input("Default Value:", key="new_col_value")
            
            if st.button("Add Column", key="add_column"):
                if new_col_name:
                    st.session_state.df[new_col_name] = new_col_value
                    st.success(f"✅ Column '{new_col_name}' added!")
                    st.dataframe(st.session_state.df, use_container_width=True, height=400)
        
        # TAB 4: Calculate
        with tab4:
            st.markdown("""
                <div class="glass-card">
                    <h2 style='color: #667eea;'>🧮 Quick Calculations</h2>
                </div>
            """, unsafe_allow_html=True)
            
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if numeric_cols:
                calc_col = st.selectbox("Select Column:", numeric_cols, key="calc_col")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("Sum", key="calc_sum", use_container_width=True):
                        result = df[calc_col].sum()
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">Sum</div>
                                <div class="metric-value">{result:,.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("Average", key="calc_avg", use_container_width=True):
                        result = df[calc_col].mean()
                        st.markdown(f"""
                            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                                <div class="metric-label">Average</div>
                                <div class="metric-value">{result:,.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("Maximum", key="calc_max", use_container_width=True):
                        result = df[calc_col].max()
                        st.markdown(f"""
                            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                                <div class="metric-label">Maximum</div>
                                <div class="metric-value">{result:,.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col4:
                    if st.button("Minimum", key="calc_min", use_container_width=True):
                        result = df[calc_col].min()
                        st.markdown(f"""
                            <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                                <div class="metric-label">Minimum</div>
                                <div class="metric-value">{result:,.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ No numeric columns available for calculations")

# ============================================
# PAGE 6: SETTINGS
# ============================================
elif page == "🎨 Settings":
    st.markdown('<h1 class="main-header">🎨 Settings & Preferences</h1>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card">
            <h2 style='color: #667eea;'>⚙️ Application Settings</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("""
        <div class="glass-card">
            <h3>ℹ️ About</h3>
            <p><strong>Version:</strong> 2.0.0</p>
            <p><strong>AI Model:</strong> Mistral 7B</p>
            <p><strong>Framework:</strong> Streamlit</p>
            <p><strong>Status:</strong> <span style='color: #11998e;'>✅ Active</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Clear All Data
    st.markdown("""
        <div class="glass-card">
            <h3>🗑️ Data Management</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear All Data & Reset", key="clear_all"):
        st.session_state.file_loaded = False
        st.session_state.df = None
        st.session_state.chat_history = []
        st.success("✅ All data cleared successfully!")
        time.sleep(1)
        st.rerun()
    
    # Help Section
    st.markdown("""
        <div class="glass-card">
            <h3>❓ Help & Documentation</h3>
            <p>Need help? Here are some resources:</p>
            <ul>
                <li>📖 User Guide</li>
                <li>🎥 Video Tutorials</li>
                <li>💬 Community Support</li>
                <li>🐛 Report a Bug</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Floating Action Button (Optional)
st.markdown("""
    <div class="fab">
        💬
    </div>
""", unsafe_allow_html=True)