import streamlit as st
import hashlib
import time
import random
from typing import Dict, Any, Generator
from datetime import datetime
from config import GOOGLE_API_KEY, SERPER_API_KEY, BLOG_POST, TOPIC
from graph import create_enhanced_graph

# Custom CSS for modern UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark theme with gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    
    /* Main container glassmorphism effect */
    .main > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin-top: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .css-1d391kg .block-container, [data-testid="stSidebar"] .block-container {
        padding: 2rem 1rem;
    }
    
    /* Headers with gradient text */
    h1, h2, h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; /* This was missing */
        color: white; /* Fallback color */
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Text input styling */
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Slider styling */
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 4px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Info, success, error boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Custom card component */
    .custom-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Agent status cards */
    .agent-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.3) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    /* Animated gradient border */
    .gradient-border {
        position: relative;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2px;
    }
    
    .gradient-border::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 15px;
        padding: 2px;
        background: linear-gradient(45deg, #f79533, #f37055, #ef4e7b, #a166ab, #5073b8, #1098ad, #07b39b, #6fba82);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: exclude;
        mask-composite: exclude;
        animation: gradient-animation 3s ease infinite;
        background-size: 300% 300%;
    }
    
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Download button special styling */
    .download-btn button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Code blocks */
    code, pre {
        background: rgba(15, 12, 41, 0.6);
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        color: #e0e0e0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .raw-html {
        display: none;
    }
    
    /* Markdown content */
    .markdown-text-container {
        line-height: 1.8;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Loading animation */
    .loading-wave {
        display: inline-flex;
        gap: 4px;
    }
    
    .loading-wave span {
        width: 4px;
        height: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
        animation: wave 1.4s infinite ease-in-out;
    }
    
    .loading-wave span:nth-child(1) { animation-delay: -0.32s; }
    .loading-wave span:nth-child(2) { animation-delay: -0.16s; }
    .loading-wave span:nth-child(3) { animation-delay: 0; }
    
    @keyframes wave {
        0%, 60%, 100% {
            transform: scaleY(0.4);
        }
        30% {
            transform: scaleY(1);
        }
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_cache_key(topic: str, temperature: float) -> str:
    """Generate a cache key for the given topic and temperature."""
    return hashlib.md5(f"{topic}_{temperature}".encode()).hexdigest()

@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_generation(topic: str, temperature: float) -> Dict[str, Any]:
    """Cached version of content generation."""
    cache_key = generate_cache_key(topic, temperature)
    graph = create_enhanced_graph(temperature=temperature)
    result = graph.invoke({TOPIC: topic})
    return result

def stream_generation(topic: str, temperature: float) -> Generator[Dict[str, Any], None, None]:
    """Stream the generation process with progress updates."""
    graph = create_enhanced_graph(temperature=temperature)
    
    # Stream the graph execution
    for chunk in graph.stream({TOPIC: topic}):
        yield chunk

def create_agent_card(agent_name: str, status: str, icon: str, color: str):
    """Create a styled agent status card."""
    return f"""
    <div class="agent-card" style="border-left: 4px solid {color};">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">{icon}</div>
            <div>
                <h4 style="margin: 0; color: {color};">{agent_name}</h4>
                <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{status}</p>
            </div>
        </div>
    </div>
    """

def create_loading_animation():
    """Create a custom loading animation."""
    return """
    <div class="loading-wave">
        <span></span>
        <span></span>
        <span></span>
    </div>
    """

def main():
    """The main function for the enhanced Streamlit UI."""
    
    # Apply custom CSS
    load_custom_css()
    
    # Check for API Keys first
    if not GOOGLE_API_KEY or not SERPER_API_KEY:
        st.error("🔐 API keys (GOOGLE_API_KEY, SERPER_API_KEY) not set. Please check your .env file.")
        st.stop()

    # Streamlit page config
    st.set_page_config(
        page_title="AI News Generator Pro", 
        page_icon="🚀", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Animated header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3.5rem; margin: 0;">
            🚀 AI News Generator Pro
        </h1>
        <p style="font-size: 1.2rem; opacity: 0.8; margin-top: 0.5rem;">
            Transform ideas into compelling articles with AI-powered agents
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for main layout
    col1, col2 = st.columns([1, 2])
    
    # Sidebar content moved to left column
    with col1:
        st.markdown('<div class="gradient-border"><div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 13px;">', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Content Configuration")
        
        topic_input = st.text_area(
            "Enter your topic",
            height=120,
            placeholder="e.g., Latest developments in quantum computing...",
            help="Be specific for better results"
        )
        
        # Advanced settings in tabs
        tab1, tab2 = st.tabs(["⚙️ Settings", "📊 Info"])
        
        with tab1:
            temperature = st.slider(
                "Creativity Level", 
                0.0, 
                1.0, 
                0.7,
                help="Lower = More focused | Higher = More creative"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                use_caching = st.checkbox("⚡ Fast Mode", value=True, help="Use cached results")
            with col_b:
                use_streaming = st.checkbox("📡 Live Mode", value=True, help="Real-time updates")
        
        with tab2:
            st.markdown("""
            **🤖 AI Agents:**
            - Research Agent
            - Writer Agent
            - Editor Agent
            - Fact-Checker Agent
            
            **⏱️ Avg. Time:** 2-3 minutes
            **📝 Output:** 800-1200 words
            """)
        
        generate_button = st.button(
            "✨ Generate Article", 
            type="primary", 
            use_container_width=True,
            disabled=not topic_input
        )
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Stats cards
        st.markdown("### 📈 Quick Stats")
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.markdown("""
            <div class="custom-card" style="text-align: center;">
                <h3 style="margin: 0; font-size: 2rem;">4</h3>
                <p style="margin: 0; opacity: 0.7;">AI Agents</p>
            </div>
            """, unsafe_allow_html=True)
        with stat_col2:
            st.markdown("""
            <div class="custom-card" style="text-align: center;">
                <h3 style="margin: 0; font-size: 2rem;">∞</h3>
                <p style="margin: 0; opacity: 0.7;">Topics</p>
            </div>
            """, unsafe_allow_html=True)

    # Main content area (right column)
    with col2:
        if generate_button and topic_input:
            
            # Check cache first if enabled
            if use_caching and not use_streaming:
                cache_key = generate_cache_key(topic_input, temperature)
                if st.cache_data.exists(cache_key):
                    with st.spinner("⚡ Loading cached result..."):
                        time.sleep(0.5)  # Brief pause for UX
                    result = cached_generation(topic_input, temperature)
                    display_final_result(result)
                    return

            # Create containers for different sections
            agents_container = st.container()
            progress_container = st.container()
            content_container = st.container()
            
            if use_streaming:
                # Streaming mode with enhanced UI
                with agents_container:
                    st.markdown("### 🤖 AI Agents Pipeline")
                    agent_cols = st.columns(4)
                    
                    # Initialize agent status placeholders
                    agent_statuses = {
                        "researcher": agent_cols[0].empty(),
                        "writer": agent_cols[1].empty(),
                        "editor": agent_cols[2].empty(),
                        "fact_checker": agent_cols[3].empty()
                    }
                    
                    # Set initial status for all agents
                    agent_statuses["researcher"].markdown(
                        create_agent_card("Research", "Waiting...", "🔍", "#667eea"), 
                        unsafe_allow_html=True
                    )
                    agent_statuses["writer"].markdown(
                        create_agent_card("Writer", "Waiting...", "✍️", "#9CA3AF"), 
                        unsafe_allow_html=True
                    )
                    agent_statuses["editor"].markdown(
                        create_agent_card("Editor", "Waiting...", "📝", "#9CA3AF"), 
                        unsafe_allow_html=True
                    )
                    agent_statuses["fact_checker"].markdown(
                        create_agent_card("Fact Check", "Waiting...", "✅", "#9CA3AF"), 
                        unsafe_allow_html=True
                    )
                
                with progress_container:
                    progress_bar = st.progress(0)
                    status_placeholder = st.empty()
                    
                # Content placeholders with better organization
                with content_container:
                    tabs = st.tabs(["📊 Research", "📝 Draft", "✨ Edited", "🎉 Final"])
                    
                    with tabs[0]:
                        research_placeholder = st.empty()
                    with tabs[1]:
                        draft_placeholder = st.empty()
                    with tabs[2]:
                        edited_placeholder = st.empty()
                    with tabs[3]:
                        final_placeholder = st.empty()
                
                # Stream the generation process
                try:
                    total_steps = 4
                    current_step = 0
                    
                    for chunk in stream_generation(topic_input, temperature):
                        node_name = list(chunk.keys())[0] if chunk else "unknown"
                        node_data = chunk.get(node_name, {})
                        
                        # Update progress based on node
                        if node_name == "researcher":
                            current_step = 1
                            agent_statuses["researcher"].markdown(
                                create_agent_card("Research", "Active", "🔍", "#10B981"), 
                                unsafe_allow_html=True
                            )
                            status_placeholder.info("🔍 Gathering latest news and information...")
                            
                            if 'research_report' in node_data:
                                with research_placeholder.container():
                                    st.markdown("#### 📊 Research Complete!")
                                    st.markdown(node_data['research_report'])
                                
                                agent_statuses["researcher"].markdown(
                                    create_agent_card("Research", "Complete ✓", "🔍", "#10B981"), 
                                    unsafe_allow_html=True
                                )
                        
                        elif node_name == "writer":
                            current_step = 2
                            agent_statuses["writer"].markdown(
                                create_agent_card("Writer", "Active", "✍️", "#F59E0B"), 
                                unsafe_allow_html=True
                            )
                            status_placeholder.info("✍️ Crafting engaging article...")
                            
                            if 'blog_post' in node_data:
                                with draft_placeholder.container():
                                    st.markdown("#### 📝 Initial Draft")
                                    st.markdown(node_data['blog_post'])
                                
                                agent_statuses["writer"].markdown(
                                    create_agent_card("Writer", "Complete ✓", "✍️", "#10B981"), 
                                    unsafe_allow_html=True
                                )
                        
                        elif node_name == "editor":
                            current_step = 3
                            agent_statuses["editor"].markdown(
                                create_agent_card("Editor", "Active", "📝", "#8B5CF6"), 
                                unsafe_allow_html=True
                            )
                            status_placeholder.info("📝 Polishing content and style...")
                            
                            if 'edited_post' in node_data:
                                with edited_placeholder.container():
                                    st.markdown("#### ✨ Edited Version")
                                    st.markdown(node_data['edited_post'])
                                
                                agent_statuses["editor"].markdown(
                                    create_agent_card("Editor", "Complete ✓", "📝", "#10B981"), 
                                    unsafe_allow_html=True
                                )
                        
                        elif node_name == "fact_checker":
                            current_step = 4
                            agent_statuses["fact_checker"].markdown(
                                create_agent_card("Fact Check", "Active", "✅", "#EF4444"), 
                                unsafe_allow_html=True
                            )
                            status_placeholder.info("🔍 Verifying claims and accuracy...")
                            
                            if 'final_post' in node_data:
                                agent_statuses["fact_checker"].markdown(
                                    create_agent_card("Fact Check", "Complete ✓", "✅", "#10B981"), 
                                    unsafe_allow_html=True
                                )
                                status_placeholder.success("✅ Article generation complete!")
                                
                                with final_placeholder.container():
                                    st.balloons()
                                    st.markdown("#### 🎉 Final Article")
                                    
                                    # Article content with custom styling
                                    st.markdown(f"""
                                    <div class="gradient-border">
                                        <div style="background: rgba(0,0,0,0.3); padding: 2rem; border-radius: 13px;">
                                            <div class="markdown-text-container">
                                                {node_data['final_post']}
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Download button with custom class
                                    st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                                    st.download_button(
                                        label="📥 Download Article (Markdown)",
                                        data=node_data['final_post'],
                                        file_name=f"{topic_input.replace(' ', '_')}_article.md",
                                        mime="text/markdown",
                                    )
                                    st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Update progress bar with smooth animation
                        progress_bar.progress(current_step / total_steps)
                        time.sleep(0.1)  # Small delay for better UX
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
                    
            else:
                # Non-streaming mode with loading animation
                with st.container():
                    loading_placeholder = st.empty()
                    loading_placeholder.markdown(
                        f"""
                        <div style="text-align: center; padding: 3rem;">
                            <h3>🤖 AI agents are creating your article...</h3>
                            {create_loading_animation()}
                            <p style="margin-top: 1rem; opacity: 0.7;">This may take 2-3 minutes</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    try:
                        if use_caching:
                            result = cached_generation(topic_input, temperature)
                        else:
                            graph = create_enhanced_graph(temperature=temperature)
                            result = graph.invoke({TOPIC: topic_input})
                        
                        loading_placeholder.empty()
                        display_final_result(result)
                        
                    except Exception as e:
                        loading_placeholder.empty()
                        st.error(f"❌ An error occurred: {e}")
        
        else:
            # Welcome screen when no generation is active
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem;">
                <div style="font-size: 5rem; margin-bottom: 1rem;">🎨</div>
                <h2>Ready to Create Amazing Content?</h2>
                <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
                    Enter a topic in the configuration panel and let our AI agents craft 
                    a comprehensive, fact-checked article for you in minutes.
                </p>
                
                <div style="display: flex; gap: 2rem; justify-content: center; margin-top: 3rem;">
                    <div class="custom-card" style="flex: 1; max-width: 200px;">
                        <h3 style="font-size: 1.5rem;">🔍</h3>
                        <h4>Research</h4>
                        <p style="opacity: 0.7; font-size: 0.9rem;">Latest news & insights</p>
                    </div>
                    <div class="custom-card" style="flex: 1; max-width: 200px;">
                        <h3 style="font-size: 1.5rem;">✍️</h3>
                        <h4>Write</h4>
                        <p style="opacity: 0.7; font-size: 0.9rem;">Engaging content</p>
                    </div>
                    <div class="custom-card" style="flex: 1; max-width: 200px;">
                        <h3 style="font-size: 1.5rem;">✨</h3>
                        <h4>Polish</h4>
                        <p style="opacity: 0.7; font-size: 0.9rem;">Professional finish</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_final_result(result: Dict[str, Any]):
    """Display the final result in a clean format."""
    
    final_post = result.get('final_post') or result.get(BLOG_POST, "Failed to generate content.")
    
    st.markdown("---")
    st.markdown("### 📰 Your Generated Article")
    
    # Main article display with custom styling
    st.markdown(f"""
    <div class="gradient-border">
        <div style="background: rgba(0,0,0,0.3); padding: 2rem; border-radius: 13px;">
            <div class="markdown-text-container">
                {final_post}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metadata cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        word_count = len(final_post.split())
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{word_count}</h3>
            <p style="margin: 0; opacity: 0.7;">Words</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        read_time = max(1, word_count // 200)  # Assuming 200 words per minute
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{read_time}</h3>
            <p style="margin: 0; opacity: 0.7;">Min Read</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"""
        <div class="custom-card" style="text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{current_time}</h3>
            <p style="margin: 0; opacity: 0.7;">Generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show intermediate results in an accordion
    with st.expander("🔍 View Generation Process", expanded=False):
        tabs = st.tabs(["📊 Research", "📝 Initial Draft", "✨ Edited Version"])
        
        with tabs[0]:
            if 'research_report' in result:
                st.markdown("#### Research Report")
                st.markdown(result['research_report'])
            else:
                st.info("Research report not available")
        
        with tabs[1]:
            if 'blog_post' in result and result['blog_post'] != final_post:
                st.markdown("#### Initial Draft")
                st.markdown(result['blog_post'])
            else:
                st.info("Initial draft not available or same as final")
        
        with tabs[2]:
            if 'edited_post' in result and result['edited_post'] != final_post:
                st.markdown("#### Edited Version")
                st.markdown(result['edited_post'])
            else:
                st.info("Edited version not available or same as final")
    
    # Download section with custom styling
    st.markdown("### 💾 Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="download-btn">', unsafe_allow_html=True)
        st.download_button(
            label="📄 Download as Markdown",
            data=final_post,
            file_name=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Convert markdown to plain text for .txt download
        import re
        plain_text = re.sub(r'[#*`_~\[\]()>!-]', '', final_post)
        st.download_button(
            label="📝 Download as Text",
            data=plain_text,
            file_name=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

if __name__ == "__main__":
    main()