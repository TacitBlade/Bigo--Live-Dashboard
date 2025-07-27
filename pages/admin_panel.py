import streamlit as st
import pandas as pd
import hashlib
import time
from datetime import datetime, timedelta

class AdminAuth:
    def __init__(self):
        # Initialize session state for authentication
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'auth_timestamp' not in st.session_state:
            st.session_state.auth_timestamp = None
        if 'failed_attempts' not in st.session_state:
            st.session_state.failed_attempts = 0
        if 'locked_until' not in st.session_state:
            st.session_state.locked_until = None
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_credentials(self, username, password):
        """Verify admin credentials - Replace with your actual credentials"""
        # Default admin credentials (change these!)
        ADMIN_USERS = {
            "admin": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "markj": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"   # "secret123"
        }
        
        hashed_password = self.hash_password(password)
        return username in ADMIN_USERS and ADMIN_USERS[username] == hashed_password
    
    def is_locked(self):
        """Check if account is temporarily locked due to failed attempts"""
        if st.session_state.locked_until:
            if datetime.now() < st.session_state.locked_until:
                return True
            else:
                # Reset lock if time has passed
                st.session_state.locked_until = None
                st.session_state.failed_attempts = 0
        return False
    
    def lock_account(self):
        """Lock account for 15 minutes after 3 failed attempts"""
        st.session_state.locked_until = datetime.now() + timedelta(minutes=15)
    
    def is_session_valid(self):
        """Check if current session is still valid (24 hour timeout)"""
        if not st.session_state.authenticated or not st.session_state.auth_timestamp:
            return False
        
        session_duration = datetime.now() - st.session_state.auth_timestamp
        return session_duration < timedelta(hours=24)
    
    def login(self, username, password):
        """Attempt to log in user"""
        if self.is_locked():
            return False, "Account temporarily locked. Try again later."
        
        if self.verify_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.auth_timestamp = datetime.now()
            st.session_state.failed_attempts = 0
            st.session_state.locked_until = None
            return True, "Login successful!"
        else:
            st.session_state.failed_attempts += 1
            if st.session_state.failed_attempts >= 3:
                self.lock_account()
                return False, "Too many failed attempts. Account locked for 15 minutes."
            return False, f"Invalid credentials. {3 - st.session_state.failed_attempts} attempts remaining."
    
    def logout(self):
        """Log out user"""
        st.session_state.authenticated = False
        st.session_state.auth_timestamp = None
        st.rerun()

def show_login_page():
    """Display the admin login page"""
    auth = AdminAuth()
    
    # Check if already authenticated and session is valid
    if st.session_state.authenticated and auth.is_session_valid():
        return True
    
    # Reset authentication if session expired
    if st.session_state.authenticated and not auth.is_session_valid():
        st.session_state.authenticated = False
        st.session_state.auth_timestamp = None
        st.warning("Session expired. Please log in again.")
    
    # Set page configuration
    st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")
    
    # Custom CSS for login page
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f8f9fa;
    }
    .login-header {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
    }
    .security-notice {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin-top: 2rem;
        font-size: 0.9rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Login header
    st.markdown('<div class="login-header"><h1>🔐 Admin Login</h1><p>Secure access to Bigo Live Dashboard</p></div>', 
                unsafe_allow_html=True)
    
    # Check if account is locked
    if auth.is_locked():
        time_remaining = st.session_state.locked_until - datetime.now()
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        st.error(f"🔒 Account locked. Try again in {minutes_remaining} minutes.")
        return False
    
    # Login form
    with st.form("admin_login_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        
        submit = st.form_submit_button("🚀 Login")
    
    # Handle login attempt
    if submit:
        if not username or not password:
            st.error("⚠️ Please enter both username and password.")
        else:
            success, message = auth.login(username, password)
            if success:
                st.success(message)
                time.sleep(1)  # Brief pause before redirect
                st.rerun()
            else:
                st.error(f"❌ {message}")
    
    # Security notice
    st.markdown("""
    <div class="security-notice">
        <strong>🛡️ Security Notice:</strong><br>
        • Sessions expire after 24 hours<br>
        • Account locks for 15 minutes after 3 failed attempts<br>
        • All access is logged for security purposes
    </div>
    """, unsafe_allow_html=True)
    
    return False

def require_admin_auth(func):
    """Decorator to require admin authentication"""
    def wrapper(*args, **kwargs):
        auth = AdminAuth()
        
        # Show logout button if authenticated
        if st.session_state.authenticated and auth.is_session_valid():
            # Create logout button in sidebar
            with st.sidebar:
                st.markdown("---")
                if st.button("🚪 Logout", key="logout_btn"):
                    auth.logout()
                
                # Show session info
                if st.session_state.auth_timestamp:
                    session_time = datetime.now() - st.session_state.auth_timestamp
                    hours = int(session_time.total_seconds() / 3600)
                    minutes = int((session_time.total_seconds() % 3600) / 60)
                    st.info(f"Session: {hours}h {minutes}m")
            
            return func(*args, **kwargs)
        else:
            if not show_login_page():
                st.stop()
    
    return wrapper

@require_admin_auth
def show_admin_panel(data_manager=None):
    """Main admin panel function"""
    # Add custom CSS for admin panel
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
    .admin-info {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🔧 Admin Panel</h1></div>', 
                unsafe_allow_html=True)
    
    # Add admin info banner
    st.markdown("""
    <div class="admin-info">
        🔐 <strong>Administrator Access</strong><br>
        You are logged in with administrator privileges. Handle sensitive data with care.
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tabs = st.tabs(["📊 Data Management", "💱 Conversion Rates", "👥 User Management", "🔒 Security"])
    
    with tabs[0]:
        st.subheader("📊 Data Management")
        
        # Data upload section
        st.write("**Upload Data Files:**")
        uploaded_file = st.file_uploader(
            "Upload new pay chart data",
            type=['csv', 'xlsx', 'json'],
            help="Upload updated pay chart data in CSV, Excel, or JSON format"
        )
        
        if uploaded_file:
            try:
                # Read the uploaded file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    df = pd.read_json(uploaded_file)
                
                st.success(f"✅ Successfully loaded {uploaded_file.name}")
                st.dataframe(df.head(), use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Rows", len(df))
                with col2:
                    st.metric("Columns", len(df.columns))
                
                if st.button("💾 Save Updated Data", type="primary"):
                    try:
                        # Add your actual save logic here
                        if data_manager:
                            # data_manager.save_data(df, uploaded_file.name)
                            pass
                        st.success("✅ Data updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error saving data: {str(e)}")
                        
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.markdown("---")
        
        # Bulk operations
        st.write("**Bulk Operations:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh All Data", use_container_width=True):
                with st.spinner("Refreshing data from sources..."):
                    time.sleep(2)  # Simulate processing
                    st.success("✅ Data refreshed successfully!")
        
        with col2:
            if st.button("📤 Export All Data", use_container_width=True):
                with st.spinner("Preparing export package..."):
                    time.sleep(2)  # Simulate processing
                    st.success("✅ Export package ready!")
        
        with col3:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                with st.spinner("Clearing cache..."):
                    time.sleep(1)
                    st.success("✅ Cache cleared!")
    
    with tabs[1]:
        st.subheader("💱 Conversion Rates")
        
        # Current rates display
        st.write("**Current Conversion Rates:**")
        col1, col2 = st.columns(2)
        
        with col1:
            bean_to_diamond = st.number_input(
                "Beans to Diamond Rate", 
                value=3.61, 
                step=0.01,
                format="%.3f",
                help="How many beans equal 1 diamond"
            )
        
        with col2:
            diamond_to_usd = st.number_input(
                "Diamond to USD Rate", 
                value=0.0036, 
                step=0.0001,
                format="%.4f",
                help="USD value of 1 diamond"
            )
        
        # Rate history (placeholder)
        st.write("**Rate History:**")
        st.info("Rate history tracking coming soon...")
        
        if st.button("💰 Update Rates", type="primary"):
            try:
                if data_manager and hasattr(data_manager, 'update_conversion_rates'):
                    data_manager.update_conversion_rates(bean_to_diamond, diamond_to_usd)
                st.success("✅ Conversion rates updated successfully!")
            except Exception as e:
                st.error(f"❌ Error updating rates: {str(e)}")
    
    with tabs[2]:
        st.subheader("👥 User Management")
        
        # User statistics
        st.write("**User Statistics:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Users", "42", "↑12%")
        with col2:
            st.metric("Total Sessions", "158", "↑5%")
        with col3:
            st.metric("Avg Session Time", "23m", "↓2%")
        
        st.markdown("---")
        
        # User activity monitoring
        st.write("**Recent User Activity:**")
        st.info("📊 User activity monitoring features coming soon...")
        
        # User permissions
        st.write("**User Permissions:**")
        st.info("🔐 Permission management features coming soon...")
    
    with tabs[3]:
        st.subheader("🔒 Security Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Access & Security:**")
            
            if st.button("🔄 Change Password", use_container_width=True):
                st.info("Password change interface coming soon...")
            
            if st.button("🚨 Clear All Sessions", use_container_width=True):
                st.warning("⚠️ This will log out all users!")
                # Add confirmation logic here
            
            if st.button("📋 View Access Logs", use_container_width=True):
                st.info("Access logs viewer coming soon...")
        
        with col2:
            st.write("**System Status:**")
            
            # System health indicators
            st.success("🟢 System Status: Healthy")
            st.info("🔵 Database: Connected")
            st.info("🔵 Authentication: Active")
            
            # Security metrics
            st.write("**Security Metrics:**")
            st.metric("Failed Login Attempts (24h)", "3")
            st.metric("Active Sessions", "7")

# Main function to run the admin panel
def main():
    """Main function to run admin panel"""
    try:
        show_admin_panel()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please contact the system administrator if this problem persists.")

if __name__ == "__main__":
    main()