import streamlit as st

def load_custom_css():
    """Load custom CSS for the cosmic theme"""
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a23 0%, #1a1a3a 50%, #2a2a4a 100%);
        color: white;
    }
    
    /* Animated stars background */
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .stars::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ddd, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 3s linear infinite;
    }
    
    @keyframes sparkle {
        0% { transform: translateY(0px) }
        100% { transform: translateY(-100px) }
    }
    
    /* Glowing elements */
    .auth-card, .upload-card, .info-card {
        background: rgba(26, 26, 58, 0.8);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: rgba(10, 10, 35, 0.9);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ffff 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00ff88 0%, #00ffff 100%);
        color: #0a0a23;
        font-weight: bold;
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(26, 26, 58, 0.6);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        background: rgba(26, 26, 58, 0.8);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(26, 26, 58, 0.8);
        border: 2px dashed rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #00ffff;
        background: rgba(26, 26, 58, 0.9);
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(26, 26, 58, 0.6);
        border-radius: 10px 10px 0 0;
        border: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: #00ffff;
    }
    
    /* Scanning animation */
    .scanning-animation {
        position: relative;
    }
    
    .scanning-animation::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ffff, transparent);
        animation: scan 2s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #00ff88;
        border-radius: 10px;
    }
    
    .stError {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        border-radius: 10px;
    }
    
    .stInfo {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 10px;
    }
    
    .stWarning {
        background: rgba(255, 235, 59, 0.1);
        border: 1px solid #ffeb3b;
        border-radius: 10px;
    }
    
    /* DataFrame styling */
    .dataframe {
        background: rgba(26, 26, 58, 0.8);
        border-radius: 10px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 58, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00ffff 0%, #667eea 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)
