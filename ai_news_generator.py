import streamlit as st
from config import GOOGLE_API_KEY, SERPER_API_KEY, BLOG_POST, TOPIC
from graph import create_graph

def main():
    """
    The main function for the Streamlit UI.
    """
    # Check for API Keys first
    if not GOOGLE_API_KEY or not SERPER_API_KEY:
        st.error("API keys (GOOGLE_API_KEY, SERPER_API_KEY) not set. Please check your .env file.")
        st.stop()

    # Streamlit page config
    st.set_page_config(page_title="AI News Generator", page_icon="📰", layout="wide")

    # Title and description
    st.title("🤖 AI News Generator, powered by LangGraph and Google's Gemini")
    st.markdown("Generate comprehensive blog posts about any topic using AI agents.")

    # Sidebar
    with st.sidebar:
        st.header("Content Settings")
        topic_input = st.text_area(
            "Enter your topic",
            height=100,
            placeholder="Enter the topic you want to generate content about..."
        )
        st.markdown("### Advanced Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7) # Note: This is not yet wired up to the LLM
        st.markdown("---")
        generate_button = st.button("Generate Content", type="primary", use_container_width=True)
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. Enter your desired topic in the text area above
            2. Adjust the temperature if needed (higher = more creative)
            3. Click 'Generate Content' to start
            4. Wait for the AI to generate your article
            5. Download the result as a markdown file
            """)

    # Main content area
    if generate_button and topic_input:
        with st.spinner("🤖 AI agents are working their magic..."):
            try:
                graph = create_graph(temperature=temperature)
                result = graph.invoke({TOPIC: topic_input})
                blog_post = result.get(BLOG_POST, "Failed to generate content.")

                st.markdown("---")
                st.subheader("Generated Article")
                st.markdown(blog_post)

                st.download_button(
                    label="Download Article",
                    data=blog_post,
                    file_name=f"{topic_input.replace(' ', '_')}_article.md",
                    mime="text/markdown",
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
