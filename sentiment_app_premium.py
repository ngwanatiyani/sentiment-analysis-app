import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

analyzer = SentimentIntensityAnalyzer()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

st.set_page_config(
    page_title="Sentiment Analysis Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

tab1, tab2, tab3, tab4 = st.tabs(["Home", "Analytics", "Reports", "About"])

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        color: #ff8c00 !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f5e6d3 0%, #d4b896 50%, #c9a87c 100%);
        min-height: 100vh;
        padding: 0;
        overflow-x: hidden;
    }
    
    .stApp {
        background: transparent;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(212, 184, 150, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(201, 168, 124, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(230, 210, 180, 0.3) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .hero-container {
        padding: 4rem 2rem;
        text-align: center;
        position: relative;
        z-index: 1;
    }
    
    .hero-glass {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 32px;
        padding: 4rem 2rem;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .hero-title {
        font-size: clamp(2.5rem, 6vw, 4rem);
        font-weight: 800;
        background: linear-gradient(135deg, #ff8c00 0%, #ff7f00 50%, #ff6347 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-tagline {
        font-size: clamp(1.1rem, 2.5vw, 1.4rem);
        color: #ff8c00;
        font-weight: 400;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .hero-graphic {
        width: 120px;
        height: 120px;
        margin: 0 auto 2rem auto;
        background: linear-gradient(135deg, #d4b896, #c9a87c);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        animation: pulse 3s ease-in-out infinite;
        box-shadow: 0 20px 40px rgba(201, 168, 124, 0.3);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .glass-panel {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-panel:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .input-section {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ff8c00;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        color: #ff8c00;
        font-size: 16px;
        font-weight: 400;
        padding: 1rem;
        transition: all 0.3s ease;
        resize: vertical;
        min-height: 150px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(201, 168, 124, 0.6);
        box-shadow: 0 0 0 4px rgba(201, 168, 124, 0.2);
        outline: none;
        background: rgba(255, 255, 255, 0.95);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
        color: #333333;
        border: none;
        border-radius: 16px;
        padding: 1rem 3rem;
        font-weight: 600;
        font-size: 18px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 25px rgba(135, 206, 235, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 15px 35px rgba(135, 206, 235, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #add8e6 0%, #9ccce8 100%);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .results-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .sentiment-result {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .sentiment-result:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .chart-glass {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

with tab1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-glass">
            <div class="hero-graphic">🧠</div>
            <h1 class="hero-title">Sentiment Analysis Pro</h1>
            <div class="hero-tagline">
                <p style="margin-bottom: 1.5rem; font-size: 1.2rem;">Follow these simple steps:</p>
                <div style="text-align: left; max-width: 500px; margin: 0 auto;">
                    <p style="margin: 0.8rem 0; font-size: 1rem;">Step 1: Enter your text in the input area below</p>
                    <p style="margin: 0.8rem 0; font-size: 1rem;">Step 2: Click the "Analyze Now" button</p>
                    <p style="margin: 0.8rem 0; font-size: 1rem;">Step 3: View your sentiment results and insights</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Analyze Your Text</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        user_input = st.text_area(
            "Enter your text for analysis:",
            height=150,
            placeholder="Type or paste your text here to discover its emotional tone and sentiment patterns...",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("Analyze Now", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if user_input and analyze_btn:
        score = analyzer.polarity_scores(user_input)
        
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Live Sentiment Metrics</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #10b981; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">POSITIVE</div>
                <div style="color: #10b981; font-size: 2.5rem; font-weight: 700;">{score['pos']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #ef4444; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">NEGATIVE</div>
                <div style="color: #ef4444; font-size: 2.5rem; font-weight: 700;">{score['neg']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #6b7280; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">NEUTRAL</div>
                <div style="color: #6b7280; font-size: 2.5rem; font-weight: 700;">{score['neu']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Overall Sentiment Analysis</h2>', unsafe_allow_html=True)
        
        result_col1, result_col2 = st.columns([1, 2], gap="large")
        
        with result_col1:
            compound_score = score['compound']
            
            if compound_score >= 0.05:
                st.markdown(f"""
                <div class="sentiment-result">
                    <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #10b981;">Positive Sentiment</h3>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; color: rgba(255, 255, 255, 0.8);">Confidence Score: {compound_score:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
            elif compound_score <= -0.05:
                st.markdown(f"""
                <div class="sentiment-result">
                    <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #ef4444;">Negative Sentiment</h3>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; color: rgba(255, 255, 255, 0.8);">Confidence Score: {compound_score:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="sentiment-result">
                    <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #6b7280;">Neutral Sentiment</h3>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; color: rgba(255, 255, 255, 0.8);">Confidence Score: {compound_score:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with result_col2:
            st.markdown('<div class="chart-glass">', unsafe_allow_html=True)
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=compound_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Sentiment Intensity", 'font': {'size': 20, 'color': '#ff8c00'}},
                number={'font': {'size': 28, 'color': '#ff8c00'}},
                gauge={
                    'axis': {'range': [-1, 1], 'tickcolor': 'rgba(255,255,255,0.8)'},
                    'bar': {'color': "#87ceeb", 'thickness': 0.3},
                    'bgcolor': "rgba(255,255,255,0.1)",
                    'borderwidth': 2,
                    'bordercolor': "rgba(255,255,255,0.3)",
                    'steps': [
                        {'range': [-1, -0.05], 'color': "rgba(239, 68, 68, 0.3)"},
                        {'range': [-0.05, 0.05], 'color': "rgba(107, 114, 128, 0.3)"},
                        {'range': [0.05, 1], 'color': "rgba(16, 185, 129, 0.3)"}
                    ]
                }
            ))
            
            fig_gauge.update_layout(
                height=350,
                font={'color': "#ff8c00", 'family': "Inter"},
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Detailed Analysis Dashboard</h2>', unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2, gap="large")
        
        with chart_col1:
            st.markdown('<div class="chart-glass">', unsafe_allow_html=True)
            
            sentiment_df = pd.DataFrame({
                'Sentiment': ['Positive', 'Negative', 'Neutral'],
                'Score': [score['pos'], score['neg'], score['neu']]
            })
            
            fig_bar = px.bar(
                sentiment_df,
                x='Sentiment',
                y='Score',
                color='Sentiment',
                color_discrete_map={
                    'Positive': '#10b981', 
                    'Negative': '#ef4444', 
                    'Neutral': '#6b7280'
                },
                title="Sentiment Score Breakdown"
            )
            
            fig_bar.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#ff8c00", 'family': "Inter"},
                title={'font': {'size': 18, 'color': '#ff8c00'}},
                xaxis={'color': '#ff8c00'},
                yaxis={'color': '#ff8c00'},
                margin=dict(l=20, r=20, t=60, b=20)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with chart_col2:
            st.markdown('<div class="chart-glass">', unsafe_allow_html=True)
            
            fig_pie = px.pie(
                sentiment_df,
                values='Score',
                names='Sentiment',
                color='Sentiment',
                color_discrete_map={
                    'Positive': '#10b981', 
                    'Negative': '#ef4444', 
                    'Neutral': '#6b7280'
                },
                title="Sentiment Distribution"
            )
            
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "#ff8c00", 'family': "Inter"},
                title={'font': {'size': 18, 'color': '#ff8c00'}},
                margin=dict(l=20, r=20, t=60, b=20)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-glass">
            <h1 class="hero-title">Analytics Dashboard</h1>
            <p class="hero-tagline">Advanced sentiment analysis metrics and insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with tab3:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-glass">
            <h1 class="hero-title">Reports</h1>
            <p class="hero-tagline">Generate and export detailed sentiment analysis reports</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with tab4:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-glass">
            <h1 class="hero-title">About SentimentPro</h1>
            <div class="hero-tagline" style="text-align: left; max-width: 700px; margin: 0 auto;">
                <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1.5rem;">
                    SentimentPro is a platform that uses a technique in Natural Language Processing (NLP) 
                    that uses machine learning and computational linguistics to automatically identify, 
                    extract, and quantify the subjective information and emotional tone within a piece of text.
                </p>
                <p style="font-size: 1rem; line-height: 1.6; opacity: 0.9;">
                    Our advanced AI algorithms analyze text sentiment with high accuracy, providing 
                    valuable insights for businesses, researchers, and individuals who need to understand 
                    the emotional context of textual data.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
