import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def handle_data_upload(uploaded_file):
    """Handle CSV file upload and preprocessing"""
    try:
        # Read CSV file, handling potential comment lines
        df = pd.read_csv(uploaded_file, comment='#')
        
        # Basic data validation
        if df.empty:
            st.error("The uploaded file is empty.")
            return None
            
        # Store original data
        st.session_state.original_data = df.copy()
        
        # Clean numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())
        
        return df
        
    except Exception as e:
        st.error(f"Error processing uploaded file: {str(e)}")
        return None

def show_dataset_insights():
    """Display comprehensive dataset insights"""
    st.markdown("## 📈 Dataset Insights")
    
    # Check if data is available
    if 'original_data' not in st.session_state:
        st.info("Please upload a dataset in the AI Detection tab to view insights.")
        return
    
    df = st.session_state.original_data
    
    # Dataset overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{df.shape[0]:,}")
    
    with col2:
        st.metric("Features", df.shape[1])
    
    with col3:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        st.metric("Numeric Features", len(numeric_cols))
    
    with col4:
        missing_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        st.metric("Missing Data %", f"{missing_percentage:.1f}%")
    
    # Data quality overview
    st.markdown("### Data Quality Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Missing data heatmap
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            fig_missing = px.bar(
                x=missing_data.index,
                y=missing_data.values,
                title="Missing Values by Column",
                labels={'x': 'Columns', 'y': 'Missing Count'}
            )
            fig_missing.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            st.success("✅ No missing values detected!")
    
    with col2:
        # Data types distribution
        dtype_counts = df.dtypes.value_counts()
        fig_dtypes = px.pie(
            values=dtype_counts.values,
            names=dtype_counts.index.astype(str),
            title="Data Types Distribution"
        )
        fig_dtypes.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_dtypes, use_container_width=True)
    
    # Statistical summary for numeric columns
    if numeric_cols:
        st.markdown("### Statistical Summary")
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
        # Distribution plots
        st.markdown("### Feature Distributions")
        
        # Select columns for distribution plots
        selected_cols = st.multiselect(
            "Select columns to visualize:",
            numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
        
        if selected_cols:
            for col in selected_cols:
                fig_dist = px.histogram(
                    df,
                    x=col,
                    title=f"Distribution of {col}",
                    marginal="box"
                )
                fig_dist.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_dist, use_container_width=True)
    
    # Correlation analysis
    if len(numeric_cols) > 1:
        st.markdown("### Correlation Analysis")
        corr_matrix = df[numeric_cols].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            title="Feature Correlation Matrix",
            color_continuous_scale="RdBu_r",
            aspect="auto"
        )
        fig_corr.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Raw data preview
    st.markdown("### Raw Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

def process_uploaded_csv_for_detection(uploaded_data):
    """Process uploaded CSV specifically for exoplanet detection"""
    # Check for exoplanet-specific columns
    exoplanet_columns = ['koi_period', 'koi_depth', 'koi_duration', 'koi_impact', 'koi_prad']
    
    processed_data = {}
    
    # Check if uploaded data has label/disposition column
    if 'label' in uploaded_data.columns:
        n_planets = uploaded_data['label'].sum()
        processed_data['has_known_labels'] = True
        processed_data['known_exoplanets'] = int(n_planets)
    elif 'koi_disposition' in uploaded_data.columns:
        candidates = uploaded_data['koi_disposition'].str.contains('CANDIDATE|CONFIRMED', case=False, na=False).sum()
        processed_data['has_known_labels'] = True
        processed_data['known_exoplanets'] = int(candidates)
    else:
        processed_data['has_known_labels'] = False
        processed_data['known_exoplanets'] = 0
    
    # Check data quality
    processed_data['total_records'] = len(uploaded_data)
    processed_data['complete_records'] = len(uploaded_data.dropna())
    processed_data['data_quality'] = (processed_data['complete_records'] / processed_data['total_records']) * 100
    
    return processed_data
