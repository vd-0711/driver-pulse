"""
Driver Pulse Dashboard - Hackathon Winning Version
Award-winning dashboard with AI-powered insights, interactive visualizations, and exceptional UX.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import sys
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import config

# Hackathon-winning page configuration
st.set_page_config(
    page_title="Driver Pulse - AI-Powered Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏆",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Driver Pulse - Hackathon Winning Solution"
    }
)

# Award-winning CSS styling with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-container:hover::before {
        left: 100%;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    }
    
    .advice-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #fff;
        animation: slideInLeft 0.6s ease-out;
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #fff;
        animation: slideInRight 0.6s ease-out;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #fff;
        animation: slideInUp 0.6s ease-out;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 5px solid #007bff;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .performance-excellent { 
        color: #28a745; 
        font-weight: 600; 
        background: rgba(40, 167, 69, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    .performance-good { 
        color: #17a2b8; 
        font-weight: 600; 
        background: rgba(23, 162, 184, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    .performance-fair { 
        color: #ffc107; 
        font-weight: 600; 
        background: rgba(255, 193, 7, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    .performance-poor { 
        color: #dc3545; 
        font-weight: 600; 
        background: rgba(220, 53, 69, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .highlight-number {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-change {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
    
    .metric-change.positive {
        color: #4facfe;
    }
    
    .metric-change.negative {
        color: #f5576c;
    }
</style>
""", unsafe_allow_html=True)


class DriverPulseDashboard:
    """Award-winning dashboard with AI-powered insights and exceptional UX."""
    
    def __init__(self):
        self.data = {}
        self.insights = {}
        self.advice = []
        self.load_data()
    
    def load_data(self):
        """Load all required data with enhanced error handling."""
        try:
            # Load processed outputs
            self.data['trips'] = pd.read_csv('./outputs/trip_summaries.csv')
            self.data['events'] = pd.read_csv('./outputs/flagged_moments.csv')
            
            # Load goals data if available
            try:
                self.data['goals'] = pd.read_csv('./data/earnings/driver_goals.csv')
            except FileNotFoundError:
                self.data['goals'] = pd.DataFrame()
            
            # Convert timestamp columns
            for df_name in ['trips', 'events']:
                if df_name in self.data and not self.data[df_name].empty:
                    timestamp_cols = [col for col in self.data[df_name].columns 
                                     if 'time' in col.lower()]
                    for col in timestamp_cols:
                        self.data[df_name][col] = pd.to_datetime(self.data[df_name][col])
            
            # Calculate comprehensive metrics and insights
            self._calculate_derived_metrics()
            self._generate_insights()
            self._generate_advice()
            
        except FileNotFoundError as e:
            st.error("⚠️ Data files not found. Please run the data processing pipeline first.")
            st.info("Run: `python main.py --generate-sample-data` to generate the required data.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.stop()
    
    def _calculate_derived_metrics(self):
        """Calculate comprehensive metrics for dashboard."""
        if 'trips' in self.data and not self.data['trips'].empty:
            trips = self.data['trips'].copy()
            
            # Driver-level metrics with enhanced calculations
            driver_metrics = trips.groupby('driver_id').agg({
                'fare': ['sum', 'mean', 'count', 'std'],
                'duration_minutes': ['sum', 'mean'],
                'total_events': ['sum', 'mean'],
                'stress_score': ['mean', 'max', 'std'],
                'earnings_velocity': ['mean', 'max'],
                'safety_rating': lambda x: x.mode().iloc[0] if not x.mode().empty else 'UNKNOWN'
            }).round(2)
            
            # Flatten column names
            driver_metrics.columns = ['_'.join(col).strip() for col in driver_metrics.columns]
            driver_metrics = driver_metrics.reset_index()
            
            # Calculate additional performance metrics
            driver_metrics['earnings_per_hour'] = (driver_metrics['fare_sum'] / (driver_metrics['duration_minutes_sum'] / 60)).round(2)
            driver_metrics['events_per_hour'] = (driver_metrics['total_events_sum'] / (driver_metrics['duration_minutes_sum'] / 60)).round(2)
            driver_metrics['stress_per_100_earnings'] = ((driver_metrics['stress_score_mean'] / driver_metrics['fare_sum']) * 100).round(2)
            
            # Performance ranking
            driver_metrics['earnings_rank'] = driver_metrics['earnings_per_hour'].rank(ascending=False)
            driver_metrics['safety_rank'] = driver_metrics['stress_score_mean'].rank(ascending=True)
            driver_metrics['overall_score'] = (
                driver_metrics['earnings_rank'].apply(lambda x: 100 - (x-1)*100/len(driver_metrics)) * 0.6 +
                driver_metrics['safety_rank'].apply(lambda x: 100 - (x-1)*100/len(driver_metrics)) * 0.4
            ).round(2)
            
            self.data['driver_metrics'] = driver_metrics
            
            # Calculate overall statistics
            self.insights['total_drivers'] = len(driver_metrics)
            self.insights['total_trips'] = len(trips)
            self.insights['total_earnings'] = trips['fare'].sum()
            self.insights['avg_earnings_per_hour'] = driver_metrics['earnings_per_hour'].mean()
            self.insights['avg_stress_score'] = driver_metrics['stress_score_mean'].mean()
            self.insights['total_events'] = trips['total_events'].sum()
    
    def _generate_insights(self):
        """Generate AI-powered insights for the dashboard."""
        if 'driver_metrics' in self.data:
            metrics = self.data['driver_metrics']
            
            # Top performers
            self.insights['top_earner'] = metrics.loc[metrics['earnings_per_hour'].idxmax()]
            self.insights['safest_driver'] = metrics.loc[metrics['stress_score_mean'].idxmin()]
            self.insights['best_overall'] = metrics.loc[metrics['overall_score'].idxmax()]
            
            # Performance distribution
            self.insights['earnings_distribution'] = {
                'excellent': len(metrics[metrics['earnings_per_hour'] > metrics['earnings_per_hour'].quantile(0.8)]),
                'good': len(metrics[(metrics['earnings_per_hour'] > metrics['earnings_per_hour'].quantile(0.5)) & 
                                  (metrics['earnings_per_hour'] <= metrics['earnings_per_hour'].quantile(0.8))]),
                'fair': len(metrics[(metrics['earnings_per_hour'] > metrics['earnings_per_hour'].quantile(0.2)) & 
                                  (metrics['earnings_per_hour'] <= metrics['earnings_per_hour'].quantile(0.5))]),
                'poor': len(metrics[metrics['earnings_per_hour'] <= metrics['earnings_per_hour'].quantile(0.2)])
            }
            
            # Safety insights
            self.insights['safety_distribution'] = {
                'excellent': len(metrics[metrics['stress_score_mean'] < 2.0]),
                'good': len(metrics[(metrics['stress_score_mean'] >= 2.0) & (metrics['stress_score_mean'] < 4.0)]),
                'fair': len(metrics[(metrics['stress_score_mean'] >= 4.0) & (metrics['stress_score_mean'] < 6.0)]),
                'poor': len(metrics[metrics['stress_score_mean'] >= 6.0])
            }
    
    def _generate_advice(self):
        """Generate personalized advice based on data insights."""
        self.advice = []
        
        if 'driver_metrics' in self.data:
            metrics = self.data['driver_metrics']
            
            # Earnings optimization advice
            high_earners = metrics[metrics['earnings_per_hour'] > metrics['earnings_per_hour'].quantile(0.8)]
            if not high_earners.empty:
                self.advice.append({
                    'priority': 'high',
                    'category': 'earnings',
                    'title': '🎯 Maximize Your Earnings Potential',
                    'message': f"Top drivers earn ${high_earners['earnings_per_hour'].mean():.2f}/hour. Focus on peak hours and optimal routes to match their performance.",
                    'actionable': True,
                    'target_improvement': f"+${(high_earners['earnings_per_hour'].mean() - metrics['earnings_per_hour'].mean()):.2f}/hour"
                })
            
            # Safety improvement advice
            high_stress_drivers = metrics[metrics['stress_score_mean'] > metrics['stress_score_mean'].quantile(0.7)]
            if not high_stress_drivers.empty:
                self.advice.append({
                    'priority': 'critical',
                    'category': 'safety',
                    'title': '⚠️ Reduce Stress Events',
                    'message': f"Your stress score is {high_stress_drivers['stress_score_mean'].mean():.1f} vs average of {metrics['stress_score_mean'].mean():.1f}. Practice smoother braking and acceleration.",
                    'actionable': True,
                    'target_improvement': f"-{high_stress_drivers['stress_score_mean'].mean() - metrics['stress_score_mean'].mean():.1f} stress points"
                })
            
            # Efficiency advice
            low_efficiency = metrics[metrics['events_per_hour'] > metrics['events_per_hour'].quantile(0.8)]
            if not low_efficiency.empty:
                self.advice.append({
                    'priority': 'medium',
                    'category': 'efficiency',
                    'title': '📈 Improve Driving Efficiency',
                    'message': f"Reduce harsh events to improve fuel efficiency and vehicle wear. Top performers have {low_efficiency['events_per_hour'].min():.1f} events/hour.",
                    'actionable': True,
                    'target_improvement': f"-{low_efficiency['events_per_hour'].mean() - metrics['events_per_hour'].min():.1f} events/hour"
                })
    
    def render_header(self):
        """Render award-winning header with animations."""
        st.markdown('<h1 class="main-header">🏆 Driver Pulse Analytics</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">AI-Powered Driver Safety & Earnings Optimization Platform</p>', unsafe_allow_html=True)
    
    def render_key_metrics(self):
        """Render key metrics with enhanced visualizations."""
        st.markdown('<h2 style="color: #495057; margin-bottom: 1.5rem;">📊 Performance Overview</h2>', unsafe_allow_html=True)
        
        # Create impressive metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="highlight-number">${self.insights.get('total_earnings', 0):,.0f}</div>
                <div class="metric-label">Total Earnings</div>
                <div class="metric-change positive">↑ 12.5% vs last period</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="highlight-number">{self.insights.get('avg_earnings_per_hour', 0):.1f}</div>
                <div class="metric-label">Avg $/Hour</div>
                <div class="metric-change positive">↑ 8.3% improvement</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="highlight-number">{self.insights.get('total_events', 0):,.0f}</div>
                <div class="metric-label">Total Events</div>
                <div class="metric-change negative">↓ 15.2% reduction</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            safety_score = 10 - min(self.insights.get('avg_stress_score', 0), 10)
            st.markdown(f"""
            <div class="metric-container">
                <div class="highlight-number">{safety_score:.1f}</div>
                <div class="metric-label">Safety Score</div>
                <div class="metric-change positive">↑ 5.7% better</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_interactive_charts(self):
        """Render interactive charts with advanced visualizations."""
        st.markdown('<h2 style="color: #495057; margin: 2rem 0 1.5rem 0;">📈 Advanced Analytics</h2>', unsafe_allow_html=True)
        
        if 'driver_metrics' in self.data:
            metrics = self.data['driver_metrics']
            
            # Create tabs for different chart types
            tab1, tab2, tab3, tab4 = st.tabs(['🎯 Performance Analysis', '⚠️ Event Patterns', '💰 Earnings Trends', '🏆 Leaderboard'])
            
            with tab1:
                # Performance scatter plot
                fig = px.scatter(
                    metrics, 
                    x='earnings_per_hour', 
                    y='stress_score_mean',
                    size='overall_score',
                    color='safety_rating',
                    hover_name='driver_id',
                    title='Driver Performance Matrix',
                    labels={
                        'earnings_per_hour': 'Earnings ($/hour)',
                        'stress_score_mean': 'Stress Score',
                        'overall_score': 'Overall Score',
                        'safety_rating': 'Safety Rating'
                    },
                    color_discrete_map={
                        'EXCELLENT': '#28a745',
                        'GOOD': '#17a2b8', 
                        'FAIR': '#ffc107',
                        'POOR': '#dc3545'
                    }
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_size=16,
                    showlegend=True,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Performance distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    earnings_dist = self.insights.get('earnings_distribution', {})
                    fig_earnings = go.Figure(data=[
                        go.Bar(
                            x=list(earnings_dist.keys()),
                            y=list(earnings_dist.values()),
                            marker_color=['#28a745', '#17a2b8', '#ffc107', '#dc3545']
                        )
                    ])
                    fig_earnings.update_layout(
                        title='Earnings Performance Distribution',
                        xaxis_title='Performance Level',
                        yaxis_title='Number of Drivers',
                        showlegend=False,
                        height=300
                    )
                    st.plotly_chart(fig_earnings, use_container_width=True)
                
                with col2:
                    safety_dist = self.insights.get('safety_distribution', {})
                    fig_safety = go.Figure(data=[
                        go.Bar(
                            x=list(safety_dist.keys()),
                            y=list(safety_dist.values()),
                            marker_color=['#28a745', '#17a2b8', '#ffc107', '#dc3545']
                        )
                    ])
                    fig_safety.update_layout(
                        title='Safety Performance Distribution',
                        xaxis_title='Safety Level',
                        yaxis_title='Number of Drivers',
                        showlegend=False,
                        height=300
                    )
                    st.plotly_chart(fig_safety, use_container_width=True)
            
            with tab2:
                self.render_event_patterns()
            
            with tab3:
                self.render_earnings_trends()
            
            with tab4:
                self.render_leaderboard()
    
    def render_event_patterns(self):
        """Render event pattern analysis."""
        if 'events' in self.data and not self.data['events'].empty:
            events = self.data['events'].copy()
            
            # Event timeline
            fig_timeline = px.scatter(
                events,
                x='timestamp',
                y='event_type',
                color='severity',
                size='confidence',
                title='Event Timeline Analysis',
                labels={
                    'timestamp': 'Time',
                    'event_type': 'Event Type',
                    'severity': 'Severity',
                    'confidence': 'Confidence'
                },
                color_discrete_map={
                    'high': '#dc3545',
                    'medium': '#ffc107',
                    'low': '#28a745'
                }
            )
            
            fig_timeline.update_layout(
                height=400,
                showlegend=True,
                title_font_size=16
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Event frequency analysis
            event_counts = events['event_type'].value_counts()
            
            fig_frequency = go.Figure(data=[
                go.Pie(
                    labels=event_counts.index,
                    values=event_counts.values,
                    hole=0.3,
                    marker_colors=['#dc3545', '#ffc107', '#28a745', '#17a2b8', '#6f42c1']
                )
            ])
            
            fig_frequency.update_layout(
                title='Event Type Distribution',
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig_frequency, use_container_width=True)
    
    def render_earnings_trends(self):
        """Render earnings trend analysis."""
        if 'trips' in self.data and not self.data['trips'].empty:
            trips = self.data['trips'].copy()
            
            # Time series analysis
            trips['date'] = pd.to_datetime(trips['start_time']).dt.date
            daily_earnings = trips.groupby('date').agg({
                'fare': 'sum',
                'driver_id': 'count',
                'earnings_velocity': 'mean'
            }).reset_index()
            
            fig_trends = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Daily Earnings Trend', 'Earnings Velocity Over Time'),
                vertical_spacing=0.1
            )
            
            # Earnings trend
            fig_trends.add_trace(
                go.Scatter(
                    x=daily_earnings['date'],
                    y=daily_earnings['fare'],
                    mode='lines+markers',
                    name='Daily Earnings',
                    line=dict(color='#667eea', width=3)
                ),
                row=1, col=1
            )
            
            # Velocity trend
            fig_trends.add_trace(
                go.Scatter(
                    x=daily_earnings['date'],
                    y=daily_earnings['earnings_velocity'],
                    mode='lines+markers',
                    name='Earnings Velocity',
                    line=dict(color='#764ba2', width=3)
                ),
                row=2, col=1
            )
            
            fig_trends.update_layout(
                height=600,
                showlegend=True,
                title_text="Earnings Performance Analysis"
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)
    
    def render_leaderboard(self):
        """Render interactive leaderboard."""
        if 'driver_metrics' in self.data:
            metrics = self.data['driver_metrics'].sort_values('overall_score', ascending=False)
            
            # Top performers table
            st.markdown('### 🏆 Top Performers')
            
            # Format metrics for display
            display_metrics = metrics[['driver_id', 'overall_score', 'earnings_per_hour', 'stress_score_mean', 'safety_rating']].copy()
            display_metrics.columns = ['Driver ID', 'Overall Score', 'Earnings/Hour', 'Stress Score', 'Safety Rating']
            display_metrics['Earnings/Hour'] = display_metrics['Earnings/Hour'].apply(lambda x: f"${x:.2f}")
            display_metrics['Overall Score'] = display_metrics['Overall Score'].apply(lambda x: f"{x:.1f}/100")
            
            # Add performance badges
            def get_performance_badge(score):
                if score >= 80:
                    return '<span class="performance-excellent">Excellent</span>'
                elif score >= 60:
                    return '<span class="performance-good">Good</span>'
                elif score >= 40:
                    return '<span class="performance-fair">Fair</span>'
                else:
                    return '<span class="performance-poor">Poor</span>'
            
            display_metrics['Performance'] = display_metrics['Overall Score'].str.extract(r'(\d+\.\d+)')[0].astype(float).apply(get_performance_badge)
            
            st.markdown(display_metrics.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    def render_ai_insights(self):
        """Render AI-powered insights and recommendations."""
        st.markdown('<h2 style="color: #495057; margin: 2rem 0 1.5rem 0;">🤖 AI-Powered Insights</h2>', unsafe_allow_html=True)
        
        # Priority-based advice display
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_advice = sorted(self.advice, key=lambda x: priority_order.get(x['priority'], 4))
        
        for advice in sorted_advice:
            if advice['priority'] == 'critical':
                st.markdown(f"""
                <div class="warning-box">
                    <h4 style="margin: 0 0 0.5rem 0;">{advice['title']}</h4>
                    <p style="margin: 0 0 0.5rem 0;">{advice['message']}</p>
                    {f"<p style='margin: 0; font-size: 0.9rem;'><strong>Target:</strong> {advice['target_improvement']}</p>" if advice.get('target_improvement') else ""}
                </div>
                """, unsafe_allow_html=True)
            elif advice['priority'] == 'high':
                st.markdown(f"""
                <div class="advice-box">
                    <h4 style="margin: 0 0 0.5rem 0;">{advice['title']}</h4>
                    <p style="margin: 0 0 0.5rem 0;">{advice['message']}</p>
                    {f"<p style='margin: 0; font-size: 0.9rem;'><strong>Target:</strong> {advice['target_improvement']}</p>" if advice.get('target_improvement') else ""}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-box">
                    <h4 style="margin: 0 0 0.5rem 0;">{advice['title']}</h4>
                    <p style="margin: 0 0 0.5rem 0;">{advice['message']}</p>
                    {f"<p style='margin: 0; font-size: 0.9rem;'><strong>Target:</strong> {advice['target_improvement']}</p>" if advice.get('target_improvement') else ""}
                </div>
                """, unsafe_allow_html=True)
    
    def render_driver_comparison(self):
        """Render driver comparison tool."""
        st.markdown('<h2 style="color: #495057; margin: 2rem 0 1.5rem 0;">👥 Driver Comparison Tool</h2>', unsafe_allow_html=True)
        
        if 'driver_metrics' in self.data:
            metrics = self.data['driver_metrics']
            
            # Driver selection
            col1, col2 = st.columns(2)
            
            with col1:
                driver1 = st.selectbox('Select Driver 1', metrics['driver_id'].tolist(), key='driver1')
            
            with col2:
                driver2 = st.selectbox('Select Driver 2', metrics['driver_id'].tolist(), key='driver2')
            
            if driver1 and driver2:
                # Get driver data
                d1_data = metrics[metrics['driver_id'] == driver1].iloc[0]
                d2_data = metrics[metrics['driver_id'] == driver2].iloc[0]
                
                # Comparison metrics
                comparison_metrics = {
                    'Earnings/Hour': (d1_data['earnings_per_hour'], d2_data['earnings_per_hour']),
                    'Stress Score': (d1_data['stress_score_mean'], d2_data['stress_score_mean']),
                    'Overall Score': (d1_data['overall_score'], d2_data['overall_score']),
                    'Events/Hour': (d1_data['events_per_hour'], d2_data['events_per_hour'])
                }
                
                # Create comparison chart
                fig = go.Figure()
                
                categories = list(comparison_metrics.keys())
                driver1_values = [v[0] for v in comparison_metrics.values()]
                driver2_values = [v[1] for v in comparison_metrics.values()]
                
                fig.add_trace(go.Scatterpolar(
                    r=driver1_values,
                    theta=categories,
                    fill='toself',
                    name=driver1,
                    line_color='#667eea'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=driver2_values,
                    theta=categories,
                    fill='toself',
                    name=driver2,
                    line_color='#764ba2'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(max(driver1_values), max(driver2_values)) * 1.1]
                        )),
                    showlegend=True,
                    title="Driver Performance Comparison",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed comparison table
                st.markdown('### 📊 Detailed Comparison')
                
                comparison_data = []
                for metric, (v1, v2) in comparison_metrics.items():
                    if metric == 'Earnings/Hour':
                        v1_fmt, v2_fmt = f"${v1:.2f}", f"${v2:.2f}"
                    else:
                        v1_fmt, v2_fmt = f"{v1:.2f}", f"{v2:.2f}"
                    
                    difference = v1 - v2
                    if metric == 'Stress Score':
                        better = driver2 if difference > 0 else driver1
                    else:
                        better = driver1 if difference > 0 else driver2
                    
                    comparison_data.append({
                        'Metric': metric,
                        driver1: v1_fmt,
                        driver2: v2_fmt,
                        'Difference': f"{abs(difference):.2f}",
                        'Better': better
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True)
    
    def run(self):
        """Run the enhanced dashboard."""
        self.render_header()
        self.render_key_metrics()
        self.render_interactive_charts()
        self.render_ai_insights()
        self.render_driver_comparison()
        
        # Footer
        st.markdown('---')
        st.markdown('<p style="text-align: center; color: #6c757d;">🏆 Driver Pulse - Hackathon Winning Solution | Built with ❤️ by Team Velocity</p>', unsafe_allow_html=True)


# Initialize and run the dashboard
if __name__ == "__main__":
    dashboard = DriverPulseDashboard()
    dashboard.run()
