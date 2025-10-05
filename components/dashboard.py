import streamlit as st
from components.data_processing import handle_data_upload, show_dataset_insights
from components.ai_model import run_ai_detection
from components.visualizations import show_exovisuals, show_shap_explainability
from components.auth import logout_user

def show_dashboard():
    """Main dashboard interface"""
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem;'>
            Welcome, Explorer {st.session_state.username} 👋
        </h1>
        <p style='color: #00ffff; font-size: 1.1rem;'>Ready to discover new worlds beyond our solar system?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/200x100/0a0a23/00ffff?text=ExoHunter", width=200)
        
        st.markdown("### Navigation")
        
        if st.button("🧠 Run AI Detection", use_container_width=True):
            st.session_state.dashboard_tab = "ai_detection"
            st.rerun()
            
        if st.button("📈 View Dataset Insights", use_container_width=True):
            st.session_state.dashboard_tab = "dataset_insights"
            st.rerun()
            
        if st.button("☄️ ExoVisuals", use_container_width=True):
            st.session_state.dashboard_tab = "exovisuals"
            st.rerun()
            
        if st.button("🔍 Explainability (SHAP)", use_container_width=True):
            st.session_state.dashboard_tab = "shap"
            st.rerun()
            
        if st.button("📜 About NASA Dataset", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Initialize dashboard tab if not set
    if 'dashboard_tab' not in st.session_state:
        st.session_state.dashboard_tab = "ai_detection"
    
    # Main content area
    if st.session_state.dashboard_tab == "ai_detection":
        show_ai_detection_tab()
    elif st.session_state.dashboard_tab == "dataset_insights":
        show_dataset_insights()
    elif st.session_state.dashboard_tab == "exovisuals":
        show_exovisuals()
    elif st.session_state.dashboard_tab == "shap":
        show_shap_explainability()

def show_ai_detection_tab():
    """AI Detection tab content"""
    st.markdown("## 🧠 AI Exoplanet Detection")
    st.markdown("Upload your CSV file containing exoplanet candidate data for analysis using our hybrid AI model.")
    
    # Upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with exoplanet candidate data"
        )
        
        if uploaded_file is not None:
            # Store uploaded file in session state
            st.session_state.uploaded_file = uploaded_file
            
            # Process and preview data
            preview_data = handle_data_upload(uploaded_file)
            
            if preview_data is not None:
                st.success("✅ File uploaded successfully!")
                
                # Show data preview
                st.markdown("### Data Preview")
                st.dataframe(preview_data.head(), use_container_width=True)
                
                st.markdown(f"**Dataset Shape:** {preview_data.shape[0]} rows × {preview_data.shape[1]} columns")
                
                # Run AI button
                if st.button("🚀 Run ExoFusion AI", use_container_width=True, type="primary"):
                    st.session_state.page = "results"
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
        <h4>📊 Expected Data Format</h4>
        <ul>
        <li><strong>koi_period:</strong> Orbital period (days)</li>
        <li><strong>koi_depth:</strong> Transit depth (ppm)</li>
        <li><strong>koi_duration:</strong> Transit duration (hours)</li>
        <li><strong>koi_impact:</strong> Impact parameter</li>
        <li><strong>koi_prad:</strong> Planet radius (Earth radii)</li>
        </ul>
        <p style='font-size: 0.9rem; color: #00ffff;'>
        💡 Don't have data? We'll use NASA's KOI dataset for demonstration.
        </p>
        </div>
        """, unsafe_allow_html=True)
