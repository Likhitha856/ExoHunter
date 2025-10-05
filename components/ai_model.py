import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb

# Try importing optional dependencies
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    
import io
import time

def load_or_generate_dataset():
    """Load NASA KOI dataset or generate synthetic data - using exact code from provided file"""
    KOI_URL = "https://exoplanetarchive.ipac.caltech.edu/TblView/nph-tblView?config=KOI&format=csv"
    
    try:
        st.info("Attempting to download KOI CSV from NASA Exoplanet Archive...")
        # skip comment lines
        df = pd.read_csv(KOI_URL, comment='#')
        st.success(f"Downloaded KOI table with shape: {df.shape}")
        
        # Keep only relevant columns
        cols = [c for c in ['koi_period','koi_depth','koi_duration','koi_impact','koi_prad','koi_disposition'] if c in df.columns]
        df = df[cols].copy()
        
        # Normalize disposition
        if 'koi_disposition' in df.columns:
            df['koi_disposition'] = df['koi_disposition'].astype(str).str.upper()
            df = df[df['koi_disposition'].isin(['CANDIDATE','CONFIRMED','FALSE POSITIVE','FALSE_POSITIVE','FALSE_POS'])]
            df['label'] = df['koi_disposition'].apply(lambda x: 0 if 'FALSE' in x else 1)
        else:
            raise ValueError("Disposition column missing in KOI fetch -> fallback")
            
        # Fill numeric columns
        for c in ['koi_period','koi_depth','koi_duration','koi_impact','koi_prad']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(df[c].median())
            else:
                df[c] = 0
                
        df = df[['koi_period','koi_depth','koi_duration','koi_impact','koi_prad','label']].dropna().reset_index(drop=True)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        if df.shape[0] < 500:
            raise ValueError("KOI table too small, using synthetic instead.")
            
        return df
        
    except Exception as e:
        st.warning(f"Could not download KOI CSV. Generating synthetic dataset. Error: {e}")
        # synthetic dataset - exact code from provided file
        n = 9000
        rng = np.random.RandomState(42)
        koi_period = 10**rng.uniform(np.log10(0.3), np.log10(500), n)
        koi_depth = rng.exponential(scale=200, size=n) / 1e5
        koi_duration = np.clip(rng.normal(3,1,n), 0.1, 20)
        koi_impact = np.clip(rng.beta(2,2,n), 0, 1)
        koi_prad = np.clip(rng.normal(2,1,n), 0.1, 20)
        prob = (koi_depth*1e5) * (1/(1+np.exp(-(koi_prad-1.2)))) * (1/(1+np.log1p(koi_period)))
        prob = (prob - prob.min())/(prob.max()-prob.min())
        label = (prob + 0.1*rng.randn(n) > 0.5).astype(int)
        
        df = pd.DataFrame({
            'koi_period': koi_period,
            'koi_depth': koi_depth,
            'koi_duration': koi_duration,
            'koi_impact': koi_impact,
            'koi_prad': koi_prad,
            'label': label
        })
        return df

@st.cache_resource
def train_models():
    """Train the hybrid XGBoost + CNN model - using exact code from provided file"""
    with st.spinner("Training AI models..."):
        # Load dataset
        df = load_or_generate_dataset()
        
        # Preprocessing
        X = df[['koi_period','koi_depth','koi_duration','koi_impact','koi_prad']].values
        y = df['label'].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
        
        # XGBoost Model - exact code
        xgb_model = xgb.XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss')
        xgb_model.fit(X_train, y_train)
        
        # Test predictions
        y_pred_xgb = xgb_model.predict(X_test)
        xgb_acc = accuracy_score(y_test, y_pred_xgb)
        
        # CNN Model (if TensorFlow is available)
        cnn_model = None
        cnn_acc = 0.0
        fusion_acc = xgb_acc
        
        if TF_AVAILABLE:
            # Simple CNN Model - exact code
            X_train_cnn = X_train.reshape(-1,5,1)
            X_test_cnn = X_test.reshape(-1,5,1)
            
            cnn_model = models.Sequential([
                layers.Conv1D(32, 2, activation='relu', input_shape=(5,1)),
                layers.MaxPooling1D(2),
                layers.Flatten(),
                layers.Dense(32, activation='relu'),
                layers.Dense(1, activation='sigmoid')
            ])
            cnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            cnn_model.fit(X_train_cnn, y_train, epochs=5, batch_size=32, verbose=0)
            
            y_pred_cnn = (cnn_model.predict(X_test_cnn) > 0.5).astype(int)
            y_pred_fusion = ((y_pred_xgb + y_pred_cnn.flatten()) / 2 > 0.5).astype(int)
            
            # Calculate accuracies
            cnn_acc = accuracy_score(y_test, y_pred_cnn)
            fusion_acc = accuracy_score(y_test, y_pred_fusion)
        
        return {
            'xgb_model': xgb_model,
            'cnn_model': cnn_model,
            'scaler': scaler,
            'test_data': (X_test, y_test),
            'accuracies': {
                'xgb': xgb_acc,
                'cnn': cnn_acc,
                'fusion': fusion_acc
            },
            'tf_available': TF_AVAILABLE
        }

def run_ai_detection(uploaded_data):
    """Run AI detection on uploaded data"""
    # Get trained models
    model_data = train_models()
    xgb_model = model_data['xgb_model']
    cnn_model = model_data['cnn_model']
    scaler = model_data['scaler']
    tf_available = model_data.get('tf_available', False)
    
    # Prepare uploaded data
    required_cols = ['koi_period','koi_depth','koi_duration','koi_impact','koi_prad']
    
    # Check if uploaded data has the required columns
    if all(col in uploaded_data.columns for col in required_cols):
        X_user = uploaded_data[required_cols].values
    else:
        # If columns are missing, try to map or use first 5 numeric columns
        numeric_cols = uploaded_data.select_dtypes(include=[np.number]).columns.tolist()[:5]
        if len(numeric_cols) >= 5:
            X_user = uploaded_data[numeric_cols].values
        else:
            st.error("Uploaded data doesn't have enough numeric columns for prediction.")
            return None
    
    # Scale the data
    X_user_scaled = scaler.transform(X_user)
    
    # Make predictions
    pred_xgb = xgb_model.predict(X_user_scaled)
    prob_xgb = xgb_model.predict_proba(X_user_scaled)[:, 1]
    
    if tf_available and cnn_model is not None:
        pred_cnn = (cnn_model.predict(X_user_scaled.reshape(-1,5,1)) > 0.5).astype(int)
        prob_cnn = cnn_model.predict(X_user_scaled.reshape(-1,5,1)).flatten()
        pred_fusion = ((pred_xgb + pred_cnn.flatten()) / 2 > 0.5).astype(int)
        prob_fusion = (prob_xgb + prob_cnn) / 2
    else:
        # Use only XGBoost if TensorFlow is not available
        pred_cnn = pred_xgb
        prob_cnn = prob_xgb
        pred_fusion = pred_xgb
        prob_fusion = prob_xgb
    
    # Determine overall result
    exoplanet_count = pred_fusion.sum()
    confidence = prob_fusion.max()
    
    result = {
        'predictions': pred_fusion,
        'probabilities': prob_fusion,
        'exoplanet_count': exoplanet_count,
        'confidence': confidence,
        'model_accuracies': model_data['accuracies'],
        'individual_preds': {
            'xgb': pred_xgb,
            'cnn': pred_cnn.flatten() if isinstance(pred_cnn, np.ndarray) else pred_cnn
        }
    }
    
    return result

def get_model_explainability(uploaded_data):
    """Generate SHAP values for model explainability"""
    if not SHAP_AVAILABLE:
        return None, None
        
    model_data = train_models()
    xgb_model = model_data['xgb_model']
    scaler = model_data['scaler']
    
    # Prepare data
    required_cols = ['koi_period','koi_depth','koi_duration','koi_impact','koi_prad']
    
    if all(col in uploaded_data.columns for col in required_cols):
        X_user = uploaded_data[required_cols].values
    else:
        numeric_cols = uploaded_data.select_dtypes(include=[np.number]).columns.tolist()[:5]
        X_user = uploaded_data[numeric_cols].values
    
    X_user_scaled = scaler.transform(X_user)
    
    # Generate SHAP values
    explainer = shap.Explainer(xgb_model)
    shap_values = explainer(X_user_scaled)
    
    return shap_values, required_cols
