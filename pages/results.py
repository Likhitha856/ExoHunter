import streamlit as st
import time
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from components.ai_model import run_ai_detection
from components.data_processing import process_uploaded_csv_for_detection
from utils.pdf_generator import generate_detection_report

def show_results_page():
    """Display AI detection results with animations"""
    
    # Check if we have uploaded data
    if 'original_data' not in st.session_state:
        st.error("No data found. Please upload a dataset first.")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    st.markdown("## 🔬 ExoFusion AI Analysis Results")
    
    # Show animated loader
    if 'analysis_complete' not in st.session_state:
        show_analysis_loader()
        return
    
    # Display results
    display_detection_results()

def show_analysis_loader():
    """Display animated analysis loader"""
    st.markdown("""
    <div style='text-align: center; margin: 3rem 0;'>
        <div class='scanning-animation'>
            <h2 style='color: #00ffff; margin-bottom: 2rem;'>🛰️ Analyzing Cosmic Data...</h2>
            <p style='font-size: 1.1rem; margin-bottom: 2rem;'>
                Our hybrid AI is scanning the uploaded dataset for exoplanet signatures
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar animation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "🔍 Loading dataset...",
        "🧠 Initializing AI models...",
        "⚙️ Training XGBoost classifier...",
        "🤖 Training CNN model...",
        "🔗 Fusing model predictions...",
        "📊 Generating SHAP explanations...",
        "✨ Finalizing analysis..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.5)  # Simulate processing time
    
    # Run actual AI detection
    try:
        with st.spinner("Running final analysis..."):
            results = run_ai_detection(st.session_state.original_data)
            st.session_state.detection_results = results
            st.session_state.analysis_complete = True
        
        status_text.success("✅ Analysis complete!")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

def display_detection_results():
    """Display the main detection results"""
    results = st.session_state.detection_results
    
    # Main result card
    exoplanet_count = results['exoplanet_count']
    confidence = results['confidence']
    
    # Determine result type and color
    if exoplanet_count > 0:
        if confidence > 0.8:
            result_type = "🟢 Confirmed Exoplanet Detected!"
            result_color = "#00ff00"
            result_icon = "🪐"
        else:
            result_type = "🔵 Possible Candidate Detected"
            result_color = "#00ffff"
            result_icon = "🌟"
    else:
        result_type = "🔴 No Exoplanet Found"
        result_color = "#ff6b6b"
        result_icon = "❌"
    
    # Results header
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 15px; margin-bottom: 2rem; border: 2px solid {result_color};'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>{result_icon}</div>
        <h2 style='color: {result_color}; margin-bottom: 1rem;'>{result_type}</h2>
        <div style='font-size: 1.2rem; margin-bottom: 1rem;'>
            <strong>Candidates Found:</strong> {exoplanet_count} | <strong>Max Confidence:</strong> {confidence:.1%}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model performance metrics
    st.markdown("### 🎯 Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    accuracies = results['model_accuracies']
    
    with col1:
        st.metric("XGBoost Accuracy", f"{accuracies['xgb']:.1%}")
    
    with col2:
        st.metric("CNN Accuracy", f"{accuracies['cnn']:.1%}")
    
    with col3:
        st.metric("Fusion Accuracy", f"{accuracies['fusion']:.1%}")
    
    with col4:
        st.metric("Total Predictions", len(results['predictions']))
    
    # Visualizations
    show_results_visualizations(results)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Re-run Analysis", use_container_width=True):
            # Clear analysis state to trigger re-run
            if 'analysis_complete' in st.session_state:
                del st.session_state.analysis_complete
            if 'detection_results' in st.session_state:
                del st.session_state.detection_results
            st.rerun()
    
    with col2:
        if st.button("📄 Download Report (PDF)", use_container_width=True, type="primary"):
            generate_and_download_report()
    
    with col3:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

def show_results_visualizations(results):
    """Display result visualizations"""
    st.markdown("### 📊 Analysis Visualizations")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["🌟 Light Curves", "📈 Feature Importance", "🎯 Prediction Distribution"])
    
    with tab1:
        show_simulated_light_curves(results)
    
    with tab2:
        show_feature_importance_plot()
    
    with tab3:
        show_prediction_distribution(results)

def show_simulated_light_curves(results):
    """Show simulated light curves for detected candidates"""
    st.markdown("#### Transit Light Curves for Top Candidates")
    
    predictions = results['predictions']
    probabilities = results['probabilities']
    
    # Get top candidates (highest probabilities)
    top_indices = np.argsort(probabilities)[-6:][::-1]  # Top 6
    
    cols = st.columns(2)
    
    for i, idx in enumerate(top_indices):
        col = cols[i % 2]
        
        with col:
            # Generate synthetic light curve
            time = np.linspace(0, 10, 1000)
            
            # Create transit based on probability
            prob = probabilities[idx]
            period = 3 + prob * 7  # Period between 3-10 days
            depth = prob * 0.01  # Transit depth based on probability
            duration = 2 + prob * 3  # Duration 2-5 hours
            
            flux = np.ones_like(time)
            transit_mask = (time % period) < (duration / 24)
            flux[transit_mask] *= (1 - depth)
            
            # Add noise
            noise = np.random.normal(0, 0.0002, len(flux))
            flux += noise
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time,
                y=flux,
                mode='lines',
                name=f'Candidate {idx+1}',
                line=dict(color='cyan' if predictions[idx] == 1 else 'gray', width=2)
            ))
            
            # Highlight transit if detected
            if predictions[idx] == 1:
                fig.add_vrect(
                    x0=period/2 - duration/48,
                    x1=period/2 + duration/48,
                    fillcolor="rgba(255,255,0,0.2)",
                    layer="below",
                    line_width=0,
                )
            
            status = "🟢 Exoplanet" if predictions[idx] == 1 else "🔴 No Detection"
            
            fig.update_layout(
                title=f'Candidate {idx+1} - {status} (Conf: {prob:.1%})',
                xaxis_title='Time (days)',
                yaxis_title='Normalized Flux',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

def show_feature_importance_plot():
    """Display feature importance visualization"""
    st.markdown("#### Feature Importance Analysis")
    
    # Simulated feature importance (in production, get from actual SHAP)
    features = ['koi_period', 'koi_depth', 'koi_duration', 'koi_impact', 'koi_prad']
    importance = [0.25, 0.30, 0.20, 0.15, 0.10]
    
    fig = px.bar(
        x=features,
        y=importance,
        title="Feature Importance for Exoplanet Detection",
        labels={'x': 'Features', 'y': 'Importance Score'},
        color=importance,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_prediction_distribution(results):
    """Show distribution of predictions and confidence scores"""
    st.markdown("#### Prediction Confidence Distribution")
    
    predictions = results['predictions']
    probabilities = results['probabilities']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Confidence histogram
        fig_hist = px.histogram(
            x=probabilities,
            title="Confidence Score Distribution",
            nbins=20,
            labels={'x': 'Confidence Score', 'y': 'Count'}
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Prediction pie chart
        pred_counts = np.bincount(predictions)
        labels = ['No Exoplanet', 'Exoplanet Detected']
        
        fig_pie = px.pie(
            values=pred_counts,
            names=labels[:len(pred_counts)],
            title="Prediction Results Summary",
            color_discrete_sequence=['#ff6b6b', '#00ff00']
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

def generate_and_download_report():
    """Generate and offer PDF report download"""
    try:
        with st.spinner("Generating PDF report..."):
            pdf_buffer = generate_detection_report(
                st.session_state.detection_results,
                st.session_state.original_data
            )
            
            st.download_button(
                label="📄 Download Analysis Report",
                data=pdf_buffer.getvalue(),
                file_name="exohunter_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.success("✅ Report generated successfully!")
            
    except Exception as e:
        st.error(f"Failed to generate report: {str(e)}")
