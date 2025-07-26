"""
Authentication utilities for the Bigo Live Dashboard.
Handles user authentication and session management.
"""

import streamlit as st
import hashlib
from typing import Optional, Dict

# Default credentials (should be moved to environment variables in production)
DEFAULT_CREDENTIALS = {
    "admin": "admin123",
    "host1": "host123",
    "manager": "manager123"
}

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username: str, password: str, credentials: Optional[Dict[str, str]] = None) -> bool:
    """Verify user credentials."""
    if credentials is None:
        credentials = DEFAULT_CREDENTIALS
    
    if username in credentials:
        return credentials[username] == password
    return False

def login_form() -> Optional[str]:
    """Display login form and handle authentication."""
    st.subheader("🔐 Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if verify_credentials(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
                st.rerun()
                return username
            else:
                st.error("Invalid credentials")
    
    return None

def logout():
    """Handle user logout."""
    if "authenticated" in st.session_state:
        del st.session_state["authenticated"]
    if "username" in st.session_state:
        del st.session_state["username"]
    st.rerun()

def require_auth() -> Optional[str]:
    """Require authentication to access content."""
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        return login_form()
    
    # Add logout button in sidebar
    with st.sidebar:
        st.write(f"👤 Logged in as: {st.session_state.get('username', 'Unknown')}")
        if st.button("Logout"):
            logout()
    
    return st.session_state.get("username")

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[str]:
    """Get current authenticated user."""
    if is_authenticated():
        return st.session_state.get("username")
    return None
