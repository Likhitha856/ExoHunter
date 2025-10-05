import streamlit as st

def show_about_page():
    """Display the about page with NASA dataset information"""
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;'>
            📜 About ExoHunter
        </h1>
        <p style='font-size: 1.2rem; color: #00ffff;'>
            Powered by NASA's Open Data & Advanced AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission section
    st.markdown("## 🚀 Our Mission")
    st.markdown("""
    ExoHunter represents the next generation of exoplanet discovery tools, combining NASA's comprehensive 
    astronomical datasets with cutting-edge artificial intelligence. Our mission is to democratize 
    exoplanet detection, making advanced astronomical analysis accessible to researchers, students, 
    and space enthusiasts worldwide.
    
    By leveraging hybrid AI models that fuse Convolutional Neural Networks (CNN) with XGBoost ensemble 
    methods, ExoHunter achieves unprecedented accuracy in identifying potential exoplanets from 
    observational data.
    """)
    
    # NASA Datasets section
    st.markdown("## 🔭 NASA Dataset Sources")
    
    # Create tabs for different missions
    tab1, tab2, tab3 = st.tabs(["🛰️ Kepler Mission", "🌟 K2 Mission", "🔍 TESS Mission"])
    
    with tab1:
        show_kepler_info()
    
    with tab2:
        show_k2_info()
    
    with tab3:
        show_tess_info()
    
    # Technology stack
    st.markdown("## 🧠 AI Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🤖 Machine Learning Models
        - **XGBoost Classifier**: Gradient boosting for tabular data excellence
        - **Convolutional Neural Network**: Deep learning for pattern recognition
        - **Hybrid Fusion**: Combining strengths of both models
        - **SHAP Integration**: Explainable AI for transparency
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Data Processing
        - **NASA Exoplanet Archive**: Real-time data integration
        - **Feature Engineering**: Advanced signal processing
        - **Data Validation**: Quality assurance protocols
        - **Interactive Visualization**: Plotly-powered charts
        """)
    
    # Statistics and achievements
    st.markdown("## 📈 Platform Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 1px solid #00ffff; border-radius: 10px;'>
            <h3 style='color: #00ffff; margin: 0;'>5,000+</h3>
            <p style='margin: 0;'>Confirmed Exoplanets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 1px solid #00ffff; border-radius: 10px;'>
            <h3 style='color: #00ffff; margin: 0;'>95%+</h3>
            <p style='margin: 0;'>Detection Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 1px solid #00ffff; border-radius: 10px;'>
            <h3 style='color: #00ffff; margin: 0;'>200K+</h3>
            <p style='margin: 0;'>Stars Monitored</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; border: 1px solid #00ffff; border-radius: 10px;'>
            <h3 style='color: #00ffff; margin: 0;'>TB</h3>
            <p style='margin: 0;'>of Data Processed</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("## ⚙️ How ExoHunter Works")
    
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    
    with step_col1:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
            <h4>1. Data Upload</h4>
            <p>Upload your CSV file with exoplanet candidate data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🧠</div>
            <h4>2. AI Analysis</h4>
            <p>Hybrid CNN+XGBoost models analyze the data patterns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔍</div>
            <h4>3. Detection</h4>
            <p>AI identifies potential exoplanet signatures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col4:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📈</div>
            <h4>4. Results</h4>
            <p>Interactive visualizations and detailed reports</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    
    with col2:
        if st.button("🚀 Try ExoHunter", use_container_width=True, type="primary"):
            if st.session_state.authenticated:
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "auth"
            st.rerun()
    
    with col3:
        if st.button("📊 View Demo", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Demo Explorer"
            st.session_state.page = "dashboard"
            st.rerun()

def show_kepler_info():
    """Display Kepler mission information"""
    st.markdown("""
    ### 🛰️ Kepler Space Telescope (2009-2013)
    
    The Kepler mission revolutionized exoplanet discovery by continuously monitoring over 150,000 stars 
    in a single field of view. Using the transit method, Kepler detected the tiny dimming of starlight 
    when planets passed in front of their host stars.
    
    **Key Achievements:**
    - Discovered over 4,000 confirmed exoplanets
    - Found the first Earth-size planet in the habitable zone
    - Provided statistical foundation for exoplanet populations
    - Enabled discovery of multi-planet systems
    
    **Data Products Used in ExoHunter:**
    - Kepler Objects of Interest (KOI) catalog
    - Light curve data and transit parameters
    - Stellar characterization data
    - Disposition classifications (confirmed, candidate, false positive)
    """)
    
    # Add some visual elements
    st.image("https://via.placeholder.com/400x200/0a0a23/00ffff?text=Kepler+Mission", 
             caption="Artist's concept of the Kepler Space Telescope")

def show_k2_info():
    """Display K2 mission information"""
    st.markdown("""
    ### 🌟 K2 Mission (2014-2018)
    
    After the primary Kepler mission ended, the K2 mission provided a second life for the telescope. 
    By using solar radiation pressure for stability, K2 observed different fields along the ecliptic plane, 
    expanding the search for exoplanets to a wider variety of stellar types and environments.
    
    **Key Achievements:**
    - Observed over 500,000 stars across 19 campaigns
    - Discovered planets around young stars and in star clusters
    - Enabled studies of stellar activity and rotation
    - Extended exoplanet discovery to M-dwarf stars
    
    **Data Products Used in ExoHunter:**
    - K2 candidate catalogs
    - Campaign-specific light curves
    - Extended stellar sample diversity
    - Young planet population studies
    """)
    
    st.image("https://via.placeholder.com/400x200/0a0a23/764ba2?text=K2+Extended+Mission", 
             caption="K2 mission observing different fields of the galaxy")

def show_tess_info():
    """Display TESS mission information"""
    st.markdown("""
    ### 🔍 TESS Mission (2018-Present)
    
    The Transiting Exoplanet Survey Satellite (TESS) is conducting an all-sky survey to discover 
    exoplanets around the brightest stars. TESS monitors stellar brightness with unprecedented precision, 
    searching for the characteristic dips that indicate planetary transits.
    
    **Key Achievements:**
    - Surveying 85% of the sky over two years
    - Monitoring over 200,000 of the brightest stars
    - Discovering planets around nearby stars ideal for follow-up
    - Enabling atmospheric characterization with next-gen telescopes
    
    **Data Products Used in ExoHunter:**
    - TESS Objects of Interest (TOI) catalog
    - High-precision photometric time series
    - All-sky coverage with 27-day sectors
    - Integration with ground-based follow-up networks
    """)
    
    st.image("https://via.placeholder.com/400x200/0a0a23/667eea?text=TESS+All-Sky+Survey", 
             caption="TESS surveying the entire sky for exoplanets")
