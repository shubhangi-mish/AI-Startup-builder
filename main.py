import os
import warnings
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from multiagent_startup_builder.crew import MultiagentStartupBuilder
import litellm  

# ✅ Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL")

# ✅ Set up LiteLLM to use Gemini
litellm.model_list.append({
    "model_name": MODEL_NAME,
    "litellm_params": {"api_key": API_KEY, "temperature": 0.7},
    "provider": "google"
})

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Define Crew and Agent Names
CREW_NAMES = {
    "Tech Crew": "💡 Tech Innovator",
    "Marketing Crew": "📈 Market Analyst",
    "Design Crew": "🎨 UI/UX Designer",
    "Product Crew": "🚀 Product Manager"
}

# Function to generate startup name
def generate_startup_name(user_idea):
    prompt = f"Suggest 10 creative and unique startup names for this idea. Strictly names only, no explanation: {user_idea}"
    response = litellm.completion(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response.get("choices", [{}])[0].get("message", {}).get("content", "No name generated.")

# Function to generate lean business model
def generate_lean_business_model(user_idea):
    prompt = f"Generate a Lean Business Model Canvas for the following startup idea, strictly in 200 words: {user_idea}"
    response = litellm.completion(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response.get("choices", [{}])[0].get("message", {}).get("content", "No model generated.")

# Function to generate elevator pitch
def generate_elevator_pitch(user_idea):
    prompt = f"Write a concise and persuasive elevator pitch for this startup idea, strictly in 100 words: {user_idea}"
    response = litellm.completion(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response.get("choices", [{}])[0].get("message", {}).get("content", "No pitch generated.")

def run():
    """Run the multi-agent startup discussion."""
    st.title("🚀 Multi-Agent Startup Builder")
    st.write("Describe your startup idea and let AI agents collaborate!")

    # User Input
    user_input = st.text_area("Enter your startup idea:", st.session_state.get("user_input", "AI-driven recruitment platform"))

    if "iteration" not in st.session_state:
        st.session_state.iteration = 1
        st.session_state.agent_responses = []

    if st.button("Start Discussion"):
        st.session_state.user_input = user_input
        inputs = {'topic': user_input, 'current_year': str(datetime.now().year)}

        try:
            startup_builder = MultiagentStartupBuilder()
            crews = startup_builder.run_all_crews(inputs=inputs)

            st.subheader(f"🗣️ Multi-Agent Discussion (Iteration {st.session_state.iteration})")
            col1, col2 = st.columns(2)

            agent_responses = []
            i = 0

            for crew_name, crew in crews.items():
                output = crew.kickoff()
                response_text = output.text if hasattr(output, "text") else str(output)
                agent_name = CREW_NAMES.get(crew_name, crew_name)

                agent_responses.append(f"{agent_name}: {response_text}")

                # ✅ Adding a styled response box
                response_box = f"""
                    <div style="border: 2px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0; 
                                background-color: #ffffff; color: black;">
                        <h4 style="color: #007bff;">{agent_name}</h4>
                        <p style="color: #333; font-weight: bold;">{response_text}</p>
                    </div>
                """

                if i % 2 == 0:
                    with col1:
                        st.markdown(response_box, unsafe_allow_html=True)
                else:
                    with col2:
                        st.markdown(response_box, unsafe_allow_html=True)

                i += 1  

            st.session_state.agent_responses = agent_responses

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # **AI-Powered Startup Name Generator**
    st.subheader("🔤 AI-Powered Startup Name Generator")
    if st.button("Generate Name"):
        startup_name = generate_startup_name(user_input)
        st.success(f"✨ Suggested Startup Name: **{startup_name}**")
    
    # **Lean Business Model Canvas Generator**
    st.subheader("📌 Lean Business Model Canvas")
    if st.button("Generate Business Model"):
        business_model = generate_lean_business_model(user_input)
        st.info(f"📝 Lean Business Model Canvas:\n{business_model}")
    
    # **Elevator Pitch Generator**
    st.subheader("🎤 Elevator Pitch Generator")
    if st.button("Generate Elevator Pitch"):
        elevator_pitch = generate_elevator_pitch(user_input)
        st.success(f"🎙️ Elevator Pitch:\n{elevator_pitch}")

if __name__ == "__main__":
    run()
