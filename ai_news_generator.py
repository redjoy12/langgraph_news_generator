import streamlit as st
import hashlib
import time
from typing import Dict, Any, Generator
from config import GOOGLE_API_KEY, SERPER_API_KEY, BLOG_POST, TOPIC
from graph import create_enhanced_graph

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
    graph = create_enhanced_graph(temperature=temperature, streaming=True)
    
    # Stream the graph execution
    for chunk in graph.stream({TOPIC: topic}):
        yield chunk

def main():
    """The main function for the enhanced Streamlit UI."""
    
    # Check for API Keys first
    if not GOOGLE_API_KEY or not SERPER_API_KEY:
        st.error("API keys (GOOGLE_API_KEY, SERPER_API_KEY) not set. Please check your .env file.")
        st.stop()

    # Streamlit page config
    st.set_page_config(
        page_title="Enhanced AI News Generator", 
        page_icon="📰", 
        layout="wide"
    )

    # Title and description
    st.title("🤖 Enhanced AI News Generator")
    st.markdown("Generate comprehensive, fact-checked blog posts using a team of AI agents.")
    
    # Sidebar
    with st.sidebar:
        st.header("Content Settings")
        topic_input = st.text_area(
            "Enter your topic",
            height=100,
            placeholder="Enter the topic you want to generate content about..."
        )
        
        st.markdown("### Advanced Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        use_caching = st.checkbox("Use caching for faster results", value=True)
        use_streaming = st.checkbox("Stream output (real-time)", value=True)
        
        st.markdown("---")
        generate_button = st.button("Generate Content", type="primary", use_container_width=True)
        
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            **Enhanced Features:**
            1. **Real-time Streaming**: Watch as content is generated live
            2. **Smart Caching**: Faster results for repeated topics
            3. **Multi-Agent Team**: Research → Write → Edit → Fact-check
            4. **Progress Tracking**: See exactly what each agent is doing
            
            **Usage:**
            1. Enter your topic above
            2. Adjust settings as needed
            3. Click 'Generate Content'
            4. Watch the AI agents collaborate in real-time
            """)

    # Main content area
    if generate_button and topic_input:
        
        # Check cache first if enabled
        if use_caching and not use_streaming:
            cache_key = generate_cache_key(topic_input, temperature)
            if st.cache_data.exists(cache_key):
                st.info("🚀 Found cached result! Loading instantly...")
                result = cached_generation(topic_input, temperature)
                display_final_result(result)
                return

        # Create containers for different sections
        progress_container = st.container()
        content_container = st.container()
        
        if use_streaming:
            # Streaming mode
            with progress_container:
                st.markdown("### 🤖 AI Agents Working...")
                
                # Create progress tracking
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                # Content placeholders
                research_placeholder = st.empty()
                draft_placeholder = st.empty()
                edited_placeholder = st.empty()
                final_placeholder = st.empty()
                
            # Stream the generation process
            try:
                total_steps = 4  # research, write, edit, fact-check
                current_step = 0
                
                for chunk in stream_generation(topic_input, temperature):
                    node_name = list(chunk.keys())[0] if chunk else "unknown"
                    node_data = chunk.get(node_name, {})
                    
                    # Update progress based on node
                    if node_name == "researcher":
                        current_step = 1
                        status_placeholder.info("🔍 **Research Agent**: Gathering latest news and information...")
                        if 'research_report' in node_data:
                            with research_placeholder.expander("📊 Research Report", expanded=False):
                                st.markdown(node_data['research_report'])
                    
                    elif node_name == "writer":
                        current_step = 2
                        status_placeholder.info("✍️ **Writer Agent**: Crafting engaging article...")
                        if 'blog_post' in node_data:
                            with draft_placeholder.expander("📝 Initial Draft", expanded=False):
                                st.markdown(node_data['blog_post'])
                    
                    elif node_name == "editor":
                        current_step = 3
                        status_placeholder.info("📝 **Editor Agent**: Polishing content and style...")
                        if 'edited_post' in node_data:
                            with edited_placeholder.expander("✨ Edited Version", expanded=False):
                                st.markdown(node_data['edited_post'])
                    
                    elif node_name == "fact_checker":
                        current_step = 4
                        status_placeholder.info("🔍 **Fact-Checker Agent**: Verifying claims and accuracy...")
                        if 'final_post' in node_data:
                            status_placeholder.success("✅ **Complete**: All agents finished!")
                            with final_placeholder:
                                st.markdown("### 🎉 Final Article")
                                st.markdown(node_data['final_post'])
                                
                                # Download button
                                st.download_button(
                                    label="📄 Download Article",
                                    data=node_data['final_post'],
                                    file_name=f"{topic_input.replace(' ', '_')}_article.md",
                                    mime="text/markdown",
                                )
                    
                    # Update progress bar
                    progress_bar.progress(current_step / total_steps)
                    time.sleep(0.1)  # Small delay for better UX
                    
            except Exception as e:
                st.error(f"An error occurred during streaming: {e}")
                
        else:
            # Non-streaming mode with caching
            with st.spinner("🤖 AI agents are working their magic..."):
                try:
                    if use_caching:
                        result = cached_generation(topic_input, temperature)
                    else:
                        graph = create_enhanced_graph(temperature=temperature)
                        result = graph.invoke({TOPIC: topic_input})
                    
                    display_final_result(result)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

def display_final_result(result: Dict[str, Any]):
    """Display the final result in a clean format."""
    
    final_post = result.get('final_post') or result.get(BLOG_POST, "Failed to generate content.")
    
    st.markdown("---")
    st.subheader("📰 Generated Article")
    st.markdown(final_post)
    
    # Show intermediate results in expandable sections
    if 'research_report' in result:
        with st.expander("📊 View Research Report"):
            st.markdown(result['research_report'])
    
    if 'blog_post' in result and result['blog_post'] != final_post:
        with st.expander("📝 View Initial Draft"):
            st.markdown(result['blog_post'])
    
    if 'edited_post' in result and result['edited_post'] != final_post:
        with st.expander("✨ View Edited Version"):
            st.markdown(result['edited_post'])
    
    # Download button
    st.download_button(
        label="📄 Download Article",
        data=final_post,
        file_name=f"ai_generated_article.md",
        mime="text/markdown",
    )

if __name__ == "__main__":
    main()
