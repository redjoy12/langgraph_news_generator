# 🤖 Enhanced AI News Generator

An advanced AI-powered content generation system that uses a team of specialized AI agents to research, write, edit, and fact-check blog articles. Built with LangGraph, Streamlit, and Google's Gemini models.

## ✨ Key Enhancements

### 🚀 User Experience Improvements

- **Real-time Streaming**: Watch content being generated token by token for immediate feedback
- **Smart Progress Indicators**: Detailed status updates for each agent's work ("Researching...", "Writing...", "Editing...", "Fact-checking...")
- **Intelligent Caching**: Saves API costs and reduces wait times for repeated requests
- **Enhanced UI**: Modern, responsive interface with expandable sections for intermediate results

### 🧠 Multi-Agent Team

The application now features a specialized team of AI agents:

1. **🔍 Research Agent**: Gathers latest news and comprehensive information
2. **✍️ Writer Agent**: Creates engaging, well-structured blog posts
3. **📝 Editor Agent**: Polishes content for clarity, flow, and readability
4. **🔍 Fact-Checker Agent**: Verifies claims and ensures accuracy

### 🔧 Technical Improvements

- **Enhanced State Management**: Explicit input passing between agents
- **Better Error Handling**: Comprehensive error messages and recovery
- **Configurable Settings**: Temperature, caching, streaming controls
- **Download Functionality**: Save articles as Markdown files

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key (for Gemini models)
- Serper API Key (for news search)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd enhanced-ai-news-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run the application**
   ```bash
   streamlit run ai_news_generator.py
   ```

## 🎯 Usage Guide

### Basic Usage

1. **Enter Topic**: Type your desired topic in the sidebar text area
2. **Configure Settings**: 
   - Adjust temperature for creativity (0.0 = focused, 1.0 = creative)
   - Enable/disable caching for faster repeated requests
   - Choose streaming for real-time feedback
3. **Generate Content**: Click "Generate Content" and watch the AI agents work
4. **Download Results**: Save the final article as a Markdown file

### Advanced Features

#### Streaming Mode
- **Real-time Updates**: See each agent's progress in real-time
- **Intermediate Results**: View research reports, drafts, and edited versions
- **Progress Tracking**: Visual progress bar and detailed status messages

#### Caching System
- **Automatic Caching**: Results cached for 1 hour by default
- **Cache Indicators**: Clear notifications when cached results are used
- **Performance Boost**: Instant loading for repeated topics

#### Multi-Agent Pipeline
```
Topic → Research Agent → Writer Agent → Editor Agent → Fact-Checker Agent → Final Article
```

Each agent contributes specialized expertise to create high-quality content.

## 📁 File Structure

```
enhanced-ai-news-generator/
├── ai_news_generator.py      # Enhanced main Streamlit application
├── enhanced_graph.py         # Multi-agent workflow graph
├── enhanced_agents.py        # Specialized AI agents
├── enhanced_state.py         # State management system
├── config.py                 # Configuration and constants
├── tools.py                  # News search and utility tools
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🔧 Configuration Options

### Environment Variables

```env
GOOGLE_API_KEY="your_google_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"
```

### Application Settings

- **Temperature**: Controls creativity (0.0-1.0)
- **Caching**: Enable/disable result caching
- **Streaming**: Real-time output generation
- **Cache TTL**: Cache expiration time (default: 1 hour)

## 🎨 Features in Detail

### Enhanced Research Agent
- **Multi-source Research**: Gathers information from various news sources
- **Structured Reports**: Organized findings with source URLs
- **Recent Focus**: Prioritizes latest developments and trends

### Intelligent Writer Agent
- **Engaging Style**: Tech-savvy but accessible tone
- **Narrative Structure**: Clear introduction, body, and conclusion
- **SEO-Friendly**: Optimized headings and structure

### Professional Editor Agent
- **Clarity Enhancement**: Improves readability and flow
- **Style Consistency**: Ensures uniform tone throughout
- **Structure Optimization**: Better paragraph breaks and transitions

### Thorough Fact-Checker Agent
- **Claim Verification**: Cross-references with research sources
- **Accuracy Assurance**: Flags potential inaccuracies
- **Context Validation**: Ensures proper context for statistics

## 📊 Performance Optimizations

### Caching Strategy
- **Smart Key Generation**: Based on topic and settings
- **Memory Efficient**: Stores only essential data
- **TTL Management**: Automatic cache expiration

### Streaming Implementation
- **Progressive Loading**: Content appears as it's generated
- **Error Recovery**: Graceful handling of streaming interruptions
- **User Experience**: Immediate feedback and engagement

## 🛠️ Development

### Adding New Agents

1. **Define Agent Function** in `enhanced_agents.py`
2. **Update State** in `enhanced_state.py`
3. **Modify Graph** in `enhanced_graph.py`
4. **Update UI** in `ai_news_generator.py`

### Customizing Prompts

Edit the prompt templates in `enhanced_agents.py` to adjust agent behavior:

```python
CUSTOM_AGENT_PROMPT = PromptTemplate.from_template("""
Your custom instructions here...
Topic: {topic}
Previous work: {previous_output}
""")
```

### Testing

```bash
# Run tests
pytest tests/

# Check code quality
black .
flake8 .
mypy .
```

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add environment variables in settings
4. Deploy

### Docker
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "ai_news_generator.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Check the inline comments and docstrings
- **Community**: Join discussions in GitHub Discussions

## 🔮 Roadmap

- [ ] **SEO Optimizer Agent**: Keyword optimization and meta descriptions
- [ ] **Image Generator Agent**: AI-generated featured images
- [ ] **Social Media Agent**: Generate social media posts
- [ ] **Analytics Dashboard**: Track generation metrics
- [ ] **Multi-language Support**: Generate content in multiple languages
- [ ] **Custom Templates**: User-defined article templates
- [ ] **Collaboration Features**: Multi-user editing and review

---

Built with ❤️ using LangGraph, Streamlit, and Google Gemini