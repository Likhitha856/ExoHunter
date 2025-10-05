import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from components.ai_model import get_model_explainability, train_models

try:
    import shap
    import matplotlib.pyplot as plt
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

def show_exovisuals():
    """Display interactive exoplanet visualizations"""
    st.markdown("## ☄️ ExoVisuals - Interactive Cosmic Data")
    
    if 'original_data' not in st.session_state:
        st.info("Please upload a dataset in the AI Detection tab to view visualizations.")
        show_demo_visualizations()
        return
    
    df = st.session_state.original_data
    
    # Create tabs for different visualization types
    tab1, tab2, tab3, tab4 = st.tabs(["🌟 Light Curves", "🪐 Planetary Properties", "🌌 3D Explorer", "📊 Statistical Plots"])
    
    with tab1:
        show_light_curve_plots(df)
    
    with tab2:
        show_planetary_properties(df)
    
    with tab3:
        show_3d_explorer(df)
    
    with tab4:
        show_statistical_plots(df)

def show_light_curve_plots(df):
    """Display transit light curve visualizations"""
    st.markdown("### 🌟 Simulated Transit Light Curves")
    
    # Generate sample light curves based on data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 3:
        # Select a few sample records
        sample_records = df.head(6)
        
        cols = st.columns(2)
        for idx, (_, row) in enumerate(sample_records.iterrows()):
            col = cols[idx % 2]
            
            with col:
                # Generate synthetic light curve based on row data
                time = np.linspace(0, 10, 1000)
                
                # Use period and depth from data if available
                period = row.get('koi_period', row.iloc[0] if len(row) > 0 else 5.0)
                depth = row.get('koi_depth', row.iloc[1] if len(row) > 1 else 0.001)
                duration = row.get('koi_duration', row.iloc[2] if len(row) > 2 else 2.0)
                
                # Create synthetic transit
                flux = np.ones_like(time)
                transit_mask = (time % period) < (duration / 24)  # Convert hours to days
                flux[transit_mask] *= (1 - abs(depth))
                
                # Add some noise
                noise = np.random.normal(0, 0.0001, len(flux))
                flux += noise
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=time,
                    y=flux,
                    mode='lines',
                    name=f'KOI {idx+1}',
                    line=dict(color='cyan', width=2)
                ))
                
                fig.update_layout(
                    title=f'Transit Light Curve - KOI {idx+1}',
                    xaxis_title='Time (days)',
                    yaxis_title='Normalized Flux',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)

def show_planetary_properties(df):
    """Display planetary properties visualizations"""
    st.markdown("### 🪐 Planetary Properties Analysis")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("Select X-axis:", numeric_cols, key="x_axis_planet")
        
        with col2:
            y_axis = st.selectbox("Select Y-axis:", numeric_cols, index=1, key="y_axis_planet")
        
        # Create scatter plot
        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{x_axis} vs {y_axis}",
            hover_data=numeric_cols[:3],
            color=numeric_cols[0] if len(numeric_cols) > 0 else None,
            size=numeric_cols[1] if len(numeric_cols) > 1 else None,
            size_max=20
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Planet size comparison
        if 'koi_prad' in df.columns:
            st.markdown("### Planet Size Distribution")
            fig_size = px.histogram(
                df,
                x='koi_prad',
                title="Planet Radius Distribution (Earth Radii)",
                nbins=30
            )
            fig_size.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_size, use_container_width=True)

def show_3d_explorer(df):
    """Display 3D visualization of planetary data"""
    st.markdown("### 🌌 3D Cosmic Explorer")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 3:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_3d = st.selectbox("X-axis:", numeric_cols, key="x_3d")
        with col2:
            y_3d = st.selectbox("Y-axis:", numeric_cols, index=1, key="y_3d")
        with col3:
            z_3d = st.selectbox("Z-axis:", numeric_cols, index=2, key="z_3d")
        
        # Create 3D scatter plot
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=df[x_3d],
            y=df[y_3d],
            z=df[z_3d],
            mode='markers',
            marker=dict(
                size=5,
                color=df[numeric_cols[0]] if len(numeric_cols) > 0 else 'cyan',
                colorscale='Viridis',
                showscale=True,
                opacity=0.8
            ),
            text=[f"Point {i+1}" for i in range(len(df))],
            hovertemplate=f'<b>%{{text}}</b><br>{x_3d}: %{{x}}<br>{y_3d}: %{{y}}<br>{z_3d}: %{{z}}<extra></extra>'
        )])
        
        fig_3d.update_layout(
            title="3D Planetary Data Explorer",
            scene=dict(
                xaxis_title=x_3d,
                yaxis_title=y_3d,
                zaxis_title=z_3d,
                bgcolor='rgba(0,0,0,0)'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=600
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)

def show_statistical_plots(df):
    """Display various statistical plots"""
    st.markdown("### 📊 Statistical Analysis")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        # Box plots
        selected_columns = st.multiselect(
            "Select columns for box plot analysis:",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if selected_columns:
            # Normalize data for comparison
            df_normalized = df[selected_columns].copy()
            for col in selected_columns:
                df_normalized[col] = (df_normalized[col] - df_normalized[col].mean()) / df_normalized[col].std()
            
            fig_box = go.Figure()
            for col in selected_columns:
                fig_box.add_trace(go.Box(
                    y=df_normalized[col],
                    name=col,
                    boxpoints='outliers'
                ))
            
            fig_box.update_layout(
                title="Normalized Feature Distributions",
                yaxis_title="Normalized Values",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            
            st.plotly_chart(fig_box, use_container_width=True)

def show_shap_explainability():
    """Display SHAP explainability analysis"""
    st.markdown("## 🔍 AI Model Explainability (SHAP Analysis)")
    
    if not SHAP_AVAILABLE:
        st.warning("⚠️ SHAP library is not available. Install it to enable model explainability features.")
        st.info("SHAP analysis provides insights into which features are most important for exoplanet detection.")
        return
    
    if 'original_data' not in st.session_state:
        st.info("Please upload a dataset in the AI Detection tab to view model explainability.")
        return
    
    with st.spinner("Generating SHAP explanations..."):
        try:
            df = st.session_state.original_data
            shap_values, feature_names = get_model_explainability(df)
            
            if shap_values is None:
                st.warning("SHAP analysis is currently unavailable.")
                return
            
            st.success("✅ SHAP analysis completed!")
            
            # SHAP Summary Plot
            st.markdown("### Feature Importance Summary")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
            
            shap.summary_plot(shap_values, feature_names=feature_names, show=False)
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            
            st.pyplot(fig, use_container_width=True)
            
            # Feature importance bar plot
            st.markdown("### Individual Feature Impact")
            
            mean_shap = np.abs(shap_values.values).mean(axis=0)
            
            fig_bar = px.bar(
                x=feature_names,
                y=mean_shap,
                title="Mean Absolute SHAP Values by Feature",
                labels={'x': 'Features', 'y': 'Mean |SHAP Value|'}
            )
            
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Explanation text
            st.markdown("""
            ### 🧠 Understanding SHAP Values
            
            **SHAP (SHapley Additive exPlanations)** values show how much each feature contributes to the model's prediction:
            
            - **Positive SHAP values** push the prediction towards "Exoplanet Present"
            - **Negative SHAP values** push the prediction towards "No Exoplanet"
            - **Larger absolute values** indicate more important features
            
            The summary plot above shows the distribution of SHAP values for each feature across all samples in your dataset.
            """)
            
        except Exception as e:
            st.error(f"Error generating SHAP explanations: {str(e)}")

def show_demo_visualizations():
    """Show demo visualizations when no data is uploaded"""
    st.markdown("### 🌟 Demo: Kepler Space Telescope Discoveries")
    
    # Generate demo data
    np.random.seed(42)
    n_samples = 1000
    
    demo_data = {
        'koi_period': 10**np.random.uniform(np.log10(0.3), np.log10(500), n_samples),
        'koi_depth': np.random.exponential(scale=200, size=n_samples) / 1e5,
        'koi_duration': np.clip(np.random.normal(3, 1, n_samples), 0.1, 20),
        'koi_prad': np.clip(np.random.normal(2, 1, n_samples), 0.1, 20)
    }
    
    demo_df = pd.DataFrame(demo_data)
    
    # 3D visualization
    fig_demo = go.Figure(data=[go.Scatter3d(
        x=demo_df['koi_period'],
        y=demo_df['koi_depth'],
        z=demo_df['koi_prad'],
        mode='markers',
        marker=dict(
            size=4,
            color=demo_df['koi_duration'],
            colorscale='Viridis',
            showscale=True,
            opacity=0.6
        ),
        text=[f"Candidate {i+1}" for i in range(len(demo_df))],
    )])
    
    fig_demo.update_layout(
        title="Demo: 3D Exoplanet Candidate Distribution",
        scene=dict(
            xaxis_title="Orbital Period (days)",
            yaxis_title="Transit Depth",
            zaxis_title="Planet Radius (Earth Radii)",
            bgcolor='rgba(0,0,0,0)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig_demo, use_container_width=True)
    
    st.info("This is a demonstration using simulated exoplanet data. Upload your own dataset to see real visualizations!")
