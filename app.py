import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Taj Mahal Heritage Intelligence | Strategic Audit",
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@300;400;500&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f9f9f9;
    }
    .main { background-color: #FDFCF0; } /* Soft Ivory Background */
    h1, h2, h3, h4, h5, h6 {
        color: #8E6F3E;
        font-family: 'Montserrat', sans-serif;
        text-align: center;
    }
    h1 { font-size: 3rem; padding-bottom: 10px; }
    h2 { margin-top: 8px; }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #FFD700; /* golden left border */
        transition: transform 0.15s ease-in-out;
    }
    .stMetric:hover {
        transform: translateY(-4px);
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #2C3E50; 
        color: white; 
    }
    .stSidebar .css-10trblm { /* adjust sidebar text style */
        color: #ffffff;
        font-weight: 600;
    }
    .stSlider label { color: white !important; font-weight: bold; }
    .stButton>button {
        background_color: #8E6F3E !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
    }
    .stTabs [role="tab"] {
        font-weight: 600;
        color: #333;
    }
    /* sidebar collapse arrow should be white for visibility */
    [data-testid="collapsedControl"] svg {
        fill: white !important;
        color: white !important;
    }
    /* make sidebar selectbox labels white */
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    /* Plotly charts general styling */
    .plotly-graph-div {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("<h1>🏛️ THE LUSTER AUDIT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.2rem;'>Strategic Impact of Air Quality on Heritage Perception & Brand Equity</p>", unsafe_allow_html=True)


st.image("https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80", width=1200)

st.markdown("<h2 style='text-align:center; color:#333; margin-top:8px;'>Quantifying the Invisible: AI Sentiment vs. Environmental Decay at the Taj Mahal</h2>", unsafe_allow_html=True)

st.write("---")


@st.cache_data
def load_strategic_data():
    
    df = pd.read_csv('Taj_Mahal_BERT_Master_Final.csv')
    
    
    df_clean = df.dropna(subset=['BERT_Overall', 'Avg_Winter_AQI']).copy()
    
    
    if 'Year' in df_clean.columns:
        df_clean['Year'] = df_clean['Year'].astype(int)
    numeric_cols = ['Avg_Winter_AQI','BERT_Overall','rating','Luster_Concern_Density','LP_Freq','LN_Freq','Friction_Density','Luster_Praise_Density','Domestic_Total','Foreign_Total','Domestic_Base_Price','Foreign_Base_Price','Review_Vol']
    for c in numeric_cols:
        if c in df_clean.columns:
            df_clean[c] = pd.to_numeric(df_clean[c], errors='coerce')

    df_clean['Luster_Concern_Pct'] = df_clean['Luster_Concern_Density'] * 100
    return df_clean

try:
    df = load_strategic_data()

    
    st.sidebar.markdown("<h3 style='color:white; font-weight:700; margin:0;'>💎 Strategy Suite</h3>", unsafe_allow_html=True)
    st.sidebar.write("Advanced analytics for heritage brand management.")
    
    aqi_threshold = st.sidebar.slider(
        "Simulate AQI Level", 
        min_value=int(df['Avg_Winter_AQI'].min()), 
        max_value=int(df['Avg_Winter_AQI'].max()), 
        value=200
    )
    
    
    st.sidebar.markdown("<p style='color:white; font-weight:700; margin:6px 0 4px 0;'>Year</p>", unsafe_allow_html=True)
    
    years = [str(int(y)) for y in sorted(df['Year'].dropna().unique())]
    y_col1, y_col2 = st.sidebar.columns(2)
    start_year = y_col1.selectbox("From", years, index=0)
    end_year = y_col2.selectbox("To", years, index=len(years)-1)
    
    start_int = int(start_year.replace(',', ''))
    end_int = int(end_year.replace(',', ''))
    if start_int > end_int:
        start_int, end_int = end_int, start_int
    year_range = (start_int, end_int)

    
    filtered_df = df[(df['Avg_Winter_AQI'] >= aqi_threshold) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    
    
    st.markdown("### 📊 Core Brand Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sent = filtered_df['BERT_Overall'].mean() if not filtered_df.empty else 0
        delta_sent = ((filtered_df['BERT_Overall'].iloc[-1] - filtered_df['BERT_Overall'].iloc[0]) if len(filtered_df) > 1 else 0)
        st.metric("AI Brand Sentiment", f"{round(avg_sent, 2)} / 5.0", f"{round(delta_sent, 2)}", delta_color="off")
        
    with col2:
        avg_rating = filtered_df['rating'].mean() if not filtered_df.empty else 0
        st.metric("Visitor Star Rating", f"{round(avg_rating, 2)} / 5.0", "Positive Bias", delta_color="off")
        
    with col3:
        sentiment_gap = (filtered_df['rating'].mean() - filtered_df['BERT_Overall'].mean()) if not filtered_df.empty else 0
        st.metric("Politeness Gap", f"{round(sentiment_gap, 2)}", "Truth delta", delta_color="inverse")
        
    with col4:
        review_vol = filtered_df['Review_Vol'].sum() if not filtered_df.empty else 0
        st.metric("Total Reviews", f"{int(review_vol)}", "Data coverage")
    
    
    st.markdown("### 👥 Visitor Analytics")
    col5, col6, col7, col8 = st.columns(4)
    
    def _format_visitors(n):
        try:
            n = float(n)
        except Exception:
            return "0"
        if abs(n) >= 1_000_000:
            return f"{n/1_000_000:.2f}M"
        if abs(n) >= 1_000:
            return f"{n/1_000:.1f}K"
        return f"{int(n)}"

    with col5:
        
        def _format_millions(x):
            try:
                x = float(x)
                return f"{x:.2f}M"
            except Exception:
                return "0.00M"

        dom_visitors = filtered_df['Dom_Mn'].mean() if 'Dom_Mn' in filtered_df.columns and not filtered_df.empty else 0
        st.metric("Avg Domestic Visitors", _format_millions(dom_visitors), "Per Year")
        
    with col6:
        for_visitors = filtered_df['For_Mn'].mean() if 'For_Mn' in filtered_df.columns and not filtered_df.empty else 0
        st.metric("Avg Foreign Visitors", _format_millions(for_visitors), "Per Year")
        
    with col7:
        
        if not filtered_df.empty:
            if 'Dom_Mn' in filtered_df.columns and 'For_Mn' in filtered_df.columns:
                dom_mean = filtered_df['Dom_Mn'].mean()
                for_mean = filtered_df['For_Mn'].mean()
            else:
                dom_mean = filtered_df['Domestic_Total'].mean() if 'Domestic_Total' in filtered_df.columns else 0
                for_mean = filtered_df['Foreign_Total'].mean() if 'Foreign_Total' in filtered_df.columns else 0
            total = (dom_mean or 0) + (for_mean or 0)
            if total > 0:
                ratio = (for_mean or 0) / total
                st.metric("Foreign Visitor Share (%)", f"{round(ratio * 100, 1)}%", "Share of total visitors")
            else:
                st.metric("Foreign Visitor Share (%)", "0%", "No data")
        else:
            st.metric("Foreign Visitor Share (%)", "0%", "No data")
        
    with col8:
        price_domestic = filtered_df['Domestic_Base_Price'].mean() if not filtered_df.empty else 0
        st.metric("Domestic Base Price", f"₹{round(price_domestic, 0)}", "Avg rate")
    

    st.markdown("### 💭 Sentiment Composition Analysis")
    col9, col10, col11, col12 = st.columns(4)
    
    with col9:
        praise_freq = filtered_df['LP_Freq'].mean() if not filtered_df.empty else 0
        st.metric("Luster Praise Freq", f"{round(praise_freq, 0)}", "Positive mentions")
        
    with col10:
        concern_freq = filtered_df['LN_Freq'].mean() if not filtered_df.empty else 0
        st.metric("Luster Concern Freq", f"{round(concern_freq, 0)}", "Issues flagged")
        
    with col11:
        friction_dens = filtered_df['Friction_Density'].mean() if not filtered_df.empty else 0
        st.metric("Friction Density", f"{round(friction_dens, 2)}", "Complaint intensity")
        
    with col12:
        praise_dens = filtered_df['Luster_Praise_Density'].mean() if not filtered_df.empty else 0
        st.metric("Praise Density", f"{round(praise_dens, 2)}", "Satisfaction depth")

    st.write("---")

    
    st.markdown("### 📈 Strategic Intelligence Visualizations")
    
    
    tab1, tab2, tab3, tab4 = st.tabs(["Sentiment Trends", "Visitor Dynamics", "Price Elasticity", "Environmental Impact"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.subheader("AI Sentiment vs Standard Ratings")
            fig1 = px.scatter(
                filtered_df, x="rating", y="BERT_Overall",
                size="Review_Vol", color="Avg_Winter_AQI",
                hover_name="Year",
                color_continuous_scale='RdYlGn_r',
                labels={"BERT_Overall": "AI Real Sentiment", "rating": "Visitor Rating"},
                title="The Politeness Gap Analysis"
            )
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=400)
            st.plotly_chart(fig1, width=700)
        
        with col_chart2:
            st.subheader("Sentiment Trends Over Time")
            if not filtered_df.empty:
                fig2 = px.line(
                    filtered_df.sort_values('Year'), 
                    x='Year', 
                    y=['BERT_Overall', 'rating'],
                    markers=True,
                    labels={'value': 'Score', 'variable': 'Metric Type'},
                    title="Sentiment Evolution"
                )
                fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=400)
                fig2.update_xaxes(tickformat='d')
                st.plotly_chart(fig2, width=700)
    
    with tab2:
        col_chart3, col_chart4 = st.columns(2)
        with col_chart3:
            st.subheader("Domestic vs Foreign Visitors")
            if not filtered_df.empty:
                
                y_cols = []
                if 'Dom_Mn' in filtered_df.columns and 'For_Mn' in filtered_df.columns:
                    y_cols = ['Dom_Mn', 'For_Mn']
                else:
                    y_cols = [c for c in ['Domestic_Total', 'Foreign_Total'] if c in filtered_df.columns]

                fig3 = px.bar(
                    filtered_df.sort_values('Year'),
                    x='Year',
                    y=y_cols,
                    barmode='group',
                    labels={'value': 'Visitors', 'variable': 'Visitor Type'},
                    title="Visitor Composition"
                )
                fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=400)
                fig3.update_xaxes(tickformat='d')
                st.plotly_chart(fig3, width=700)
        
        with col_chart4:
            st.subheader("Monthly Visitor Trends")
            if not filtered_df.empty:
                
                yts = [c for c in ['Dom_Mn', 'For_Mn'] if c in filtered_df.columns]
                if yts:
                    fig4 = px.line(
                        filtered_df.sort_values('Year'),
                        x='Year',
                        y=yts,
                        markers=True,
                        labels={'value': 'Visitors (M)', 'variable': 'Visitor Type'},
                        title="Domestic & Foreign Monthly Pattern (Millions)"
                    )
                    fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=400)
                    fig4.update_xaxes(tickformat='d')
                    st.plotly_chart(fig4, width=700)
    
    with tab3:
        st.subheader("Pricing Strategy Analysis")
        col_chart5, col_chart6 = st.columns(2)
        with col_chart5:
            if not filtered_df.empty:
               
                df_dom = filtered_df.sort_values('Year')
                visitor_col_dom = 'Dom_Mn' if 'Dom_Mn' in df_dom.columns else ('Domestic_Total' if 'Domestic_Total' in df_dom.columns else None)
                fig5 = go.Figure()
                
                if 'Domestic_Base_Price' in df_dom.columns:
                    fig5.add_trace(go.Scatter(x=df_dom['Year'], y=df_dom['Domestic_Base_Price'], mode='lines+markers', name='Domestic Base Price', yaxis='y1'))
                
                if visitor_col_dom:
                    fig5.add_trace(go.Scatter(x=df_dom['Year'], y=df_dom[visitor_col_dom], mode='lines+markers', name='Visitors', yaxis='y2'))

                fig5.update_layout(
                    title='Domestic Price vs Visitors (Trend)',
                    xaxis=dict(title='Year', tickformat='d'),
                    yaxis=dict(title='Price (₹)'),
                    yaxis2=dict(title=('Visitors (M)' if visitor_col_dom == 'Dom_Mn' else 'Visitors'), overlaying='y', side='right') ,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig5, width=700)
        
        with col_chart6:
            if not filtered_df.empty:
                df_for = filtered_df.sort_values('Year')
                visitor_col_for = 'For_Mn' if 'For_Mn' in df_for.columns else ('Foreign_Total' if 'Foreign_Total' in df_for.columns else None)
                fig6 = go.Figure()
                if 'Foreign_Base_Price' in df_for.columns:
                    fig6.add_trace(go.Scatter(x=df_for['Year'], y=df_for['Foreign_Base_Price'], mode='lines+markers', name='Foreign Base Price', yaxis='y1'))
                if visitor_col_for:
                    fig6.add_trace(go.Scatter(x=df_for['Year'], y=df_for[visitor_col_for], mode='lines+markers', name='Visitors', yaxis='y2'))

                fig6.update_layout(
                    title='Foreign Price vs Visitors (Trend)',
                    xaxis=dict(title='Year', tickformat='d'),
                    yaxis=dict(title='Price (₹)'),
                    yaxis2=dict(title=('Visitors (M)' if visitor_col_for == 'For_Mn' else 'Visitors'), overlaying='y', side='right'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig6, width=700)
    
    with tab4:
        st.subheader("Air Quality Impact Analysis")
        col_chart7, col_chart8 = st.columns(2)
        with col_chart7:
            if not filtered_df.empty:
                fig7 = px.scatter(
                    filtered_df,
                    x='Avg_Winter_AQI',
                    y='BERT_Overall',
                    size='Review_Vol',
                    color='Friction_Density',
                    hover_name='Year',
                    trendline='ols',
                    title="AQI Impact on Sentiment"
                )
                fig7.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=400)
                st.plotly_chart(fig7, width=700)
        
        with col_chart8:
            if not filtered_df.empty:
                
                y_compare = [c for c in ['LP_Freq', 'LN_Freq'] if c in filtered_df.columns]
                if y_compare:
                    fig8 = px.bar(
                        filtered_df.sort_values('Year'),
                        x='Year',
                        y=y_compare,
                        barmode='group',
                        labels={'value': 'Frequency', 'variable': 'Mention Type'},
                        title="Praise vs Concern Mentions by Year (Comparison)"
                    )
                    fig8.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=400)
                    fig8.update_xaxes(tickformat='d')
                    st.plotly_chart(fig8, width=700)

    st.write("---")

    
    st.markdown("### 📋 Executive Data Summary")
    display_cols = ['Year', 'Avg_Winter_AQI', 'BERT_Overall', 'rating']
    
    if 'Dom_Mn' in filtered_df.columns and 'For_Mn' in filtered_df.columns:
        display_cols += ['Dom_Mn', 'For_Mn']
    else:
        display_cols += ['Domestic_Total', 'Foreign_Total']
    display_cols += ['Domestic_Base_Price', 'Foreign_Base_Price', 'Review_Vol', 'Friction_Density']
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    
    display_df = filtered_df[available_cols].copy()
    if 'Year' in display_df.columns:
        display_df['Year'] = display_df['Year'].astype(int).astype(str)
    if 'BERT_Overall' in display_df.columns:
        display_df['BERT_Overall'] = display_df['BERT_Overall'].round(2)
    if 'Friction_Density' in display_df.columns:
        display_df['Friction_Density'] = display_df['Friction_Density'].round(2)

    st.dataframe(display_df.sort_values('Year', ascending=False).reset_index(drop=True))

    
    st.markdown("### 🎯 Strategic Recommendations")
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.info(f"""
        **Sentiment Health:**
        - Current Brand Sentiment: {round(filtered_df['BERT_Overall'].mean(), 2)}/5.0
        - Visitor Rating Gap: {round(sentiment_gap, 2)} (Politeness Effect)
        - Recommadation: Address gap through transparency in guest feedback
        """)
    
    with col_insight2:
        st.warning(f"""
        **Environmental Concern:**
        - Average AQI Level: {round(filtered_df['Avg_Winter_AQI'].mean(), 0)}
        - Friction Events: {round(filtered_df['Friction_Density'].mean(), 2)}
        - Recommadation: Implement air quality monitoring & communication strategy
        """)

except Exception as e:
    st.error(f"An error occurred: {e}")