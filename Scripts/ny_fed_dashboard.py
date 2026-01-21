import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests

st.set_page_config(page_title="NY Fed Dashboard", layout="wide")

# Title
st.title("📊 NY Fed Economic Dashboard")
st.markdown("Real-time economic data from the Federal Reserve Bank of New York")

# Sidebar
st.sidebar.header("Dashboard Controls")
st.sidebar.markdown("---")

# Create tabs for different data categories
tab1, tab2, tab3 = st.tabs(["📈 Key Indicators", "💰 Treasury Rates", "ℹ️ About"])

with tab1:
    st.header("Key Economic Indicators")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Federal Funds Rate (Current)",
            value="4.50%",
            delta="+0.25%"
        )

    with col2:
        st.metric(
            label="10-Year Treasury Yield",
            value="4.42%",
            delta="-0.08%"
        )

    with col3:
        st.metric(
            label="Inflation (YoY)",
            value="3.2%",
            delta="-0.1%"
        )

    st.markdown("---")

    # Sample chart - Treasury yield curve
    st.subheader("Treasury Yield Curve")

    # Sample data for demonstration
    maturities = ['1 Mo', '3 Mo', '6 Mo', '1 Yr', '2 Yr', '5 Yr', '10 Yr', '30 Yr']
    yields = [5.30, 5.25, 5.15, 4.95, 4.70, 4.50, 4.42, 4.60]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=maturities,
        y=yields,
        mode='lines+markers',
        name='Current Yield Curve',
        line=dict(color='#0051a5', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        xaxis_title="Maturity",
        yaxis_title="Yield (%)",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Treasury Rates Over Time")

    # Sample historical data
    dates = pd.date_range(start='2024-01-01', end='2024-11-23', freq='W')

    df = pd.DataFrame({
        'Date': dates,
        '2-Year': [4.5 + (i % 10) * 0.05 for i in range(len(dates))],
        '10-Year': [4.3 + (i % 8) * 0.04 for i in range(len(dates))],
        '30-Year': [4.5 + (i % 6) * 0.03 for i in range(len(dates))]
    })

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=df['Date'], y=df['2-Year'],
        name='2-Year',
        line=dict(color='#00a86b')
    ))

    fig2.add_trace(go.Scatter(
        x=df['Date'], y=df['10-Year'],
        name='10-Year',
        line=dict(color='#0051a5')
    ))

    fig2.add_trace(go.Scatter(
        x=df['Date'], y=df['30-Year'],
        name='30-Year',
        line=dict(color='#ff6b35')
    ))

    fig2.update_layout(
        xaxis_title="Date",
        yaxis_title="Yield (%)",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Show data table
    st.subheader("Recent Data")
    st.dataframe(df.tail(10), use_container_width=True)

with tab3:
    st.header("About This Dashboard")
    st.markdown("""
    This dashboard displays economic data related to the Federal Reserve Bank of New York.

    **Data Sources:**
    - Federal Reserve Economic Data (FRED)
    - NY Fed Official Statistics

    **Features:**
    - Real-time key economic indicators
    - Treasury yield curve visualization
    - Historical rate trends

    **Note:** This is a demonstration dashboard. For live data integration,
    you can connect to the FRED API or NY Fed's data feeds.

    ---

    **To run this dashboard:**
    ```bash
    streamlit run ny_fed_dashboard.py
    ```
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Dashboard created with Streamlit")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
