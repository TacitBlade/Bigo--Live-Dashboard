import streamlit as st
import pandas as pd
from typing import Dict, List, Optional

def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """Validate that DataFrame has required columns"""
    if df.empty:
        return False
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.warning(f"Missing columns: {', '.join(missing_columns)}")
        return False
    
    return True

def safe_date_conversion(df: pd.DataFrame, date_column: str = "Date") -> pd.DataFrame:
    """Safely convert date column to datetime with error handling"""
    if date_column not in df.columns:
        return df
    
    try:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        invalid_dates = df[date_column].isna().sum()
        if invalid_dates > 0:
            st.warning(f"⚠️ Found {invalid_dates} invalid dates that were set to NaT")
    except Exception as e:
        st.error(f"Error converting dates: {str(e)}")
    
    return df

def clean_text_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean text data by removing extra whitespace and handling nulls"""
    text_columns = df.select_dtypes(include=['object']).columns
    
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', '')
            df[col] = df[col].replace('None', '')
    
    return df

def get_data_summary(df: pd.DataFrame) -> Dict:
    """Get summary statistics for the DataFrame"""
    if df.empty:
        return {"total_rows": 0, "total_columns": 0, "memory_usage": "0 KB"}
    
    memory_usage = df.memory_usage(deep=True).sum()
    memory_mb = memory_usage / (1024 * 1024)
    
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "memory_usage": f"{memory_mb:.2f} MB" if memory_mb > 1 else f"{memory_usage / 1024:.2f} KB",
        "null_values": df.isnull().sum().sum(),
        "duplicate_rows": df.duplicated().sum()
    }

def display_data_info(df: pd.DataFrame, title: str = "Data Summary"):
    """Display data information in an expandable section"""
    with st.expander(f"📊 {title}"):
        summary = get_data_summary(df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", summary["total_rows"])
        with col2:
            st.metric("Total Columns", summary["total_columns"])
        with col3:
            st.metric("Memory Usage", summary["memory_usage"])
        with col4:
            st.metric("Null Values", summary["null_values"])
        
        if summary["duplicate_rows"] > 0:
            st.warning(f"⚠️ Found {summary['duplicate_rows']} duplicate rows")
        
        if not df.empty:
            st.subheader("Column Info")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            })
            st.dataframe(col_info, use_container_width=True)
