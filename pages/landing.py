import streamlit as st

def show_landing_page():
    """Display the landing/welcome page"""
    
    # Hero section with animated background
    st.markdown("""
    <div style='text-align: center; padding: 4rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: -1rem -1rem 2rem -1rem; position: relative; overflow: hidden;'>
        <div class='stars'></div>
        <div style='position: relative; z-index: 2;'>
            <h1 style='font-size: 4rem; margin-bottom: 1rem; color: white; text-shadow: 0 0 20px rgba(0,255,255,0.5);'>
                🪐 ExoHunter
            </h1>
            <h2 style='font-size: 2rem; margin-bottom: 1rem; color: #00ffff; font-weight: 300;'>
                The Exoplanet Discovery AI
            </h2>
            <p style='font-size: 1.5rem; color: rgba(255,255,255,0.9); margin-bottom: 3rem; max-width: 600px; margin-left: auto; margin-right: auto;'>
                Explore the Unknown. Detect the Undiscovered.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin: 3rem 0;'>
            <h3 style='color: #00ffff; margin-bottom: 2rem;'>🚀 Discover New Worlds with AI</h3>
            <p style='font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;'>
                ExoHunter combines the power of <strong>NASA's open datasets</strong> with cutting-edge 
                <strong>hybrid AI technology</strong> (CNN + XGBoost fusion) to detect exoplanets 
                lurking in the vast cosmic darkness.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features grid
        st.markdown("### ✨ Key Features")
        
        feat_col1, feat_col2 = st.columns(2)
        
        with feat_col1:
            st.markdown("""
            **🧠 Hybrid AI Model**  
            Advanced CNN + XGBoost fusion for superior detection accuracy
            
            **📊 Interactive Visualizations**  
            Explore light curves, planetary properties, and 3D data
            
            **🔍 Model Explainability**  
            SHAP analysis to understand AI decision-making
            """)
        
        with feat_col2:
            st.markdown("""
            **🌌 NASA Data Integration**  
            Direct access to Kepler, K2, and TESS mission datasets
            
            **📈 Real-time Analysis**  
            Upload your CSV data for instant exoplanet detection
            
            **📄 Detailed Reports**  
            Generate comprehensive PDF analysis reports
            """)
        
        # Call-to-action buttons
        st.markdown("<div style='margin: 3rem 0; text-align: center;'>", unsafe_allow_html=True)
        
        button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
        
        with button_col1:
            if st.button("🚀 Get Started", use_container_width=True, type="primary"):
                st.session_state.page = "auth"
                st.rerun()
        
        with button_col2:
            if st.button("📜 Learn More", use_container_width=True):
                st.session_state.page = "about"
                st.rerun()
        
        with button_col3:
            if st.button("🌟 Demo Mode", use_container_width=True):
                # Set demo credentials
                st.session_state.authenticated = True
                st.session_state.username = "Demo Explorer"
                st.session_state.page = "dashboard"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Statistics section
    st.markdown("---")
    st.markdown("### 🌌 The Search for New Worlds")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("🪐 Confirmed Exoplanets", "5,000+", "Growing daily")
    
    with stat_col2:
        st.metric("🔭 Kepler Discoveries", "4,000+", "Revolutionary mission")
    
    with stat_col3:
        st.metric("🌟 Stars Monitored", "200,000+", "Continuous observation")
    
    with stat_col4:
        st.metric("🎯 Detection Accuracy", "95%+", "AI-powered precision")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #666;'>
        <p>🚀 Powered by NASA Open Data & AI Fusion</p>
        <p>Built with Streamlit • TensorFlow • XGBoost • SHAP</p>
    </div>
    """, unsafe_allow_html=True)
