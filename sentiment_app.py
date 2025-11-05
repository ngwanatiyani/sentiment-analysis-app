import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Pro",
    page_icon="😊",
    layout="wide"
)

# Custom CSS with converted hex colors
st.markdown("""
<style>
    .main {
        background: #f7f9fc;
        color: #262626;
    }
    
    .stTextArea textarea {
        background: #f0f2f6;
        border: 2px solid #e1e5ee;
        border-radius: 12px;
        color: #262626;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f6af5;
        box-shadow: 0 0 0 2px rgba(79, 106, 245, 0.1);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #4f6af5 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px -4px rgba(79, 106, 245, 0.15);
        font-size: 14px;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px -4px rgba(79, 106, 245, 0.25);
    }
    
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border-left: 4px solid #4f6af5;
        margin: 12px 0px;
        box-shadow: 0 2px 12px -2px rgba(40, 42, 54, 0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -6px rgba(40, 42, 54, 0.15);
    }
    
    .sentiment-positive {
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px -4px rgba(16, 185, 129, 0.2);
        color: white;
    }
    
    .sentiment-negative {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px -4px rgba(239, 68, 68, 0.2);
        color: white;
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px -4px rgba(107, 114, 128, 0.2);
        color: white;
    }
    
    .header-section {
        background: linear-gradient(135deg, #4f6af5 0%, #8b5cf6 100%);
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
    }
    
    .sample-text-btn {
        background: #f0f2f6;
        color: #374151;
        border: 1px solid #e1e5ee;
        border-radius: 8px;
        padding: 10px 16px;
        margin: 5px 0;
        width: 100%;
        text-align: left;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .sample-text-btn:hover {
        background: #4f6af5;
        color: white;
        transform: translateX(5px);
    }
    
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid #e1e5ee;
    }
</style>
""", unsafe_allow_html=True)

# Header with gradient
st.markdown("""
<div class="header-section">
    <h1 style="margin:0; font-size: 2.5rem;">🎭 Sentiment Analysis Pro</h1>
    <p style="margin:10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">
        Analyze the emotional tone of your text using advanced VADER sentiment analysis
    </p>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Enter Your Text")
    user_input = st.text_area(
        "Type or paste your text below:",
        height=150,
        placeholder="Enter your text here to analyze sentiment...",
        label_visibility="collapsed"
    )
    
    analyze_btn = st.button("🚀 Analyze Sentiment", use_container_width=True)

with col2:
    st.subheader("📊 Quick Stats")
    if user_input and analyze_btn:
        score = analyzer.polarity_scores(user_input)
        
        # Metrics in cards
        col2_1, col2_2, col2_3 = st.columns(3)
        
        with col2_1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #10b981; margin:0; font-size: 0.9rem;">POSITIVE</h4>
                <h2 style="color: #10b981; margin:0; font-size: 2rem;">{score['pos']:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2_2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #ef4444; margin:0; font-size: 0.9rem;">NEGATIVE</h4>
                <h2 style="color: #ef4444; margin:0; font-size: 2rem;">{score['neg']:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2_3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #6b7280; margin:0; font-size: 0.9rem;">NEUTRAL</h4>
                <h2 style="color: #6b7280; margin:0; font-size: 2rem;">{score['neu']:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)

# Analysis Results
if user_input and analyze_btn:
    score = analyzer.polarity_scores(user_input)
    
    st.markdown("---")
    st.subheader("🎯 Analysis Results")
    
    # Overall Sentiment with enhanced styling
    col3, col4 = st.columns([1, 2])
    
    with col3:
        st.subheader("Overall Sentiment")
        compound_score = score['compound']
        
        if compound_score >= 0.05:
            st.markdown(f"""
            <div class="sentiment-positive">
                <h3 style="margin:0; font-size: 1.5rem;">😊 Positive</h3>
                <p style="margin:10px 0 0 0; font-size: 1rem; opacity: 0.9;">
                    The text expresses strong positive sentiment with {compound_score:.3f} confidence
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif compound_score <= -0.05:
            st.markdown(f"""
            <div class="sentiment-negative">
                <h3 style="margin:0; font-size: 1.5rem;">😠 Negative</h3>
                <p style="margin:10px 0 0 0; font-size: 1rem; opacity: 0.9;">
                    The text expresses strong negative sentiment with {compound_score:.3f} confidence
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="sentiment-neutral">
                <h3 style="margin:0; font-size: 1.5rem;">😐 Neutral</h3>
                <p style="margin:10px 0 0 0; font-size: 1rem; opacity: 0.9;">
                    The text expresses neutral sentiment with {compound_score:.3f} confidence
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        # Gauge Chart for Compound Score with matching colors
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=compound_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Sentiment Intensity", 'font': {'size': 20}},
            number={'font': {'size': 30}},
            gauge={
                'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#4f6af5"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#e1e5ee",
                'steps': [
                    {'range': [-1, -0.05], 'color': "#ef4444"},
                    {'range': [-0.05, 0.05], 'color': "#6b7280"},
                    {'range': [0.05, 1], 'color': "#10b981"}],
                'threshold': {
                    'line': {'color': "#4f6af5", 'width': 4},
                    'thickness': 0.75,
                    'value': compound_score
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=300,
            font={'color': "#262626", 'family': "Arial"},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Visualizations
    st.subheader("📈 Detailed Analysis")
    
    # Bar chart for sentiment scores
    col5, col6 = st.columns(2)
    
    with col5:
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
            title="Sentiment Score Distribution"
        )
        fig_bar.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "#262626"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col6:
        # Pie chart
        fig_pie = px.pie(
            sentiment_df,
            values='Score',
            names='Sentiment',
            title="Sentiment Proportion",
            color='Sentiment',
            color_discrete_map={
                'Positive': '#10b981',
                'Negative': '#ef4444',
                'Neutral': '#6b7280'
            }
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "#262626"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Radar chart for comprehensive view
    st.subheader("🎯 Sentiment Radar")
    
    categories = ['Positive', 'Negative', 'Neutral', 'Compound']
    values = [score['pos'], score['neg'], score['neu'], (score['compound'] + 1) / 2]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Sentiment Scores',
        line=dict(color='#4f6af5', width=2),
        fillcolor='rgba(79, 106, 245, 0.3)'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], color='#262626'),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#262626"}
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Raw scores in expandable section
    with st.expander("📋 View Raw Sentiment Scores"):
        st.json(score)

# Sample text for testing
with st.expander("💡 Need sample text?"):
    st.write("Try these examples:")
    samples = [
        "I absolutely love this product! It's amazing and works perfectly.",
        "This is the worst experience I've ever had. Terrible service!",
        "The weather is okay today. Nothing special, but not bad either."
    ]
    for sample in samples:
        if st.button(f"Use: '{sample[:30]}...'", key=sample):
            st.session_state.sample_text = sample
            st.rerun()

# Footer
st.markdown("""
<div class="footer">
    Powered by VADER Sentiment Analysis | Built with Streamlit
</div>
""", unsafe_allow_html=True)        
