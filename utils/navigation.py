import streamlit as st

class NavigationManager:
    def __init__(self):
        self.pages = {
            "🏠 Dashboard": "main_dashboard",
            "💰 Host Pay Chart": "host_pay_chart", 
            "🏢 Agency Pay Chart": "agency_pay_chart",
            "📊 Analytics": "analytics",
            "🔧 Admin Panel": "admin_panel",
            "📈 Reports": "reports",
            "⚙️ Settings": "settings"
        }
    
    def render_sidebar(self):
        """Render enhanced sidebar navigation"""
        st.sidebar.title("🎯 Bigo Live Dashboard")
        
        # User role selection
        user_role = st.sidebar.selectbox(
            "Select Role",
            ["Host", "Agency", "Admin"],
            key="user_role"
        )
        
        # Filter pages based on role
        filtered_pages = self.filter_pages_by_role(user_role)
        
        selected_page = st.sidebar.radio(
            "Navigation",
            list(filtered_pages.keys()),
            key="navigation"
        )
        
        return filtered_pages[selected_page], user_role
    
    def filter_pages_by_role(self, role):
        """Filter pages based on user role"""
        if role == "Host":
            return {k: v for k, v in self.pages.items() 
                   if v in ["main_dashboard", "host_pay_chart", "analytics"]}
        elif role == "Agency":
            return {k: v for k, v in self.pages.items() 
                   if v not in ["admin_panel"]}
        else:  # Admin
            return self.pages