import streamlit as st
import hashlib
import os

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def handle_authentication():
    """Handle user authentication (signup/login)"""
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; margin-bottom: 0.5rem;'>
            🪐 ExoHunter
        </h1>
        <p style='font-size: 1.2rem; color: #00ffff; margin-bottom: 2rem;'>
            Explore the Unknown. Detect the Undiscovered.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and signup
    tab1, tab2 = st.columns(2)
    
    with tab1:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.subheader("🚀 Login")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="explorer@exohunter.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if email and password:
                    # Simple authentication (in production, use proper database)
                    if authenticate_user(email, password):
                        st.session_state.authenticated = True
                        st.session_state.username = email.split('@')[0].capitalize()
                        st.session_state.page = "dashboard"
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Try demo@exohunter.com / demo123")
                else:
                    st.error("Please fill in all fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.subheader("🌟 Sign Up")
        
        with st.form("signup_form"):
            new_email = st.text_input("Email", placeholder="your.email@domain.com")
            new_password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            signup_btn = st.form_submit_button("Sign Up", use_container_width=True)
            
            if signup_btn:
                if new_email and new_password and confirm_password:
                    if new_password == confirm_password:
                        if register_user(new_email, new_password):
                            st.session_state.authenticated = True
                            st.session_state.username = new_email.split('@')[0].capitalize()
                            st.session_state.page = "dashboard"
                            st.success("Account created successfully!")
                            st.rerun()
                        else:
                            st.error("Email already exists")
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Please fill in all fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    
    with col3:
        if st.button("About NASA Data →", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()

def authenticate_user(email, password):
    """Authenticate user credentials"""
    # Demo credentials for testing
    demo_users = {
        "demo@exohunter.com": hash_password("demo123"),
        "explorer@exohunter.com": hash_password("explore123")
    }
    
    hashed_password = hash_password(password)
    return email in demo_users and demo_users[email] == hashed_password

def register_user(email, password):
    """Register new user (simplified for demo)"""
    # In production, store in database
    if email not in ["demo@exohunter.com", "explorer@exohunter.com"]:
        return True
    return False

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.page = "landing"
    st.rerun()
