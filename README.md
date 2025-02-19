# 🚀 Multi-Agent Startup Builder

The **Multi-Agent Startup Builder** is an AI-powered web application that helps aspiring entrepreneurs and startup founders create and refine their business ideas. This tool leverages multiple AI agents to collaborate on various aspects of building a startup, including generating startup names, business models, and elevator pitches.

## Features

- **Multi-Agent Collaboration**: Multiple AI agents work together to discuss your startup idea from different perspectives.
  - **Tech Innovator**: Provides tech-related insights.
  - **Market Analyst**: Offers market analysis and strategy.
  - **UI/UX Designer**: Focuses on design and user experience.
  - **Product Manager**: Guides the product roadmap and features.
  
- **AI-Powered Generators**:
  - **Startup Name Generator**: Suggests creative and unique startup names.
  - **Lean Business Model Generator**: Creates a concise Lean Business Model Canvas for your idea.
  - **Elevator Pitch Generator**: Helps you craft a persuasive elevator pitch for investors or customers.

## Technologies Used

- **Streamlit**: For building the interactive web interface.
- **LiteLLM**: For integrating with the Gemini model for AI-based responses.
- **Multiagent Startup Builder**: Custom-built logic for managing multi-agent interactions.
- **CrewAI Tools**: AI tools like WebsiteSearchTool for gathering market data.
- **dotenv**: For securely managing API keys and environment variables.
- **Warnings**: To suppress unnecessary warnings during development.

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/multi-agent-startup-builder.git
   cd multi-agent-startup-builder
Install dependencies:

    ```bash
    pip install -r requirements.txt
    Set up your environment variables:

Create a .env file in the project root directory.

Add your Gemini API key and model name to the .env file:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_model_name_here
Run the Streamlit app:

streamlit run app.py
Navigate to http://localhost:8501 in your browser to use the app.

Usage
Enter Your Idea: Type your startup idea into the input field.
Start Discussion: Click the "Start Discussion" button to see the AI agents collaborate and provide their responses.
Generate Business Assets: You can generate:
A startup name.
A Lean Business Model Canvas.
An elevator pitch.
Example
Startup Idea: "AI-driven recruitment platform"

AI-Powered Startup Name: "HireAI", "TalentMatch"
Lean Business Model: A brief description of the business model for the startup.
Elevator Pitch: A concise pitch summarizing the business idea in under 100 words.
