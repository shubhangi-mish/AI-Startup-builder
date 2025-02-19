import warnings
import streamlit as st
from datetime import datetime
from multiagent_startup_builder.crew import MultiagentStartupBuilder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Define Crew and Agent Names
CREW_NAMES = {
    "Tech Crew": "💡 Tech Innovator",
    "Marketing Crew": "📈 Market Analyst",
    "Design Crew": "🎨 UI/UX Designer",
    "Product Crew": "🚀 Product Manager"
}

def run():
    """Run the multi-agent startup discussion."""
    st.title("🚀 Multi-Agent Startup Builder")
    st.write("Describe your startup idea and let AI agents collaborate!")

    # User Input
    user_input = st.text_area("Enter your startup idea:", "AI-driven recruitment platform")
    
    # Session State Initialization
    if "iteration" not in st.session_state:
        st.session_state.iteration = 1
        st.session_state.agent_responses = []
        st.session_state.show_feedback = False  # Ensure feedback always shows after first run

    if st.button("Start Discussion"):
        inputs = {
            'topic': user_input,
            'current_year': str(datetime.now().year)
        }
        print(f"🔍 Inputs: {inputs}")

        try:
            # Create MultiagentStartupBuilder instance
            startup_builder = MultiagentStartupBuilder()
            crews = startup_builder.run_all_crews(inputs=inputs)

            st.subheader(f"🗣️ Multi-Agent Discussion (Iteration {st.session_state.iteration})")
            col1, col2 = st.columns(2)

            agent_responses = []  # Store responses for LLM feedback
            i = 0  # Track column placement

            for crew_name, crew in crews.items():
                print(f"\n🚀 **Executing {crew_name}**")
                output = crew.kickoff()
                print(f"\n📝 **{crew_name} Output:**")

                # Convert CrewOutput to text if needed
                response_text = output.text if hasattr(output, "text") else str(output)
                agent_name = CREW_NAMES.get(crew_name, crew_name)
                
                agent_responses.append(f"{agent_name}: {response_text}")  # Store for feedback

                # Display response in styled box with RED FONT COLOR
                response_box = f"""
                    <div style="border: 2px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0; 
                                background-color: #ffffff; color: black;">
                        <h4 style="color: #007bff;">{agent_name}</h4>
                        <p style="color: red; font-weight: bold;">{response_text}</p>
                    </div>
                """
                if i % 2 == 0:
                    with col1:
                        st.markdown(response_box, unsafe_allow_html=True)
                else:
                    with col2:
                        st.markdown(response_box, unsafe_allow_html=True)
                
                i += 1  # Alternate columns for display

            # Store agent responses in session state
            st.session_state.agent_responses = agent_responses
            print(st.session_state.agent_responses)
            st.session_state.show_feedback = True  # Show feedback after first run

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Feedback Section (Always Visible After First Run)
    if st.session_state.show_feedback:
        st.subheader("💬 Provide Your Feedback")
        feedback = st.text_area("Enter your feedback about the discussion:")

        if st.button("Submit Feedback & Continue"):
            # Prepare input for next iteration
            full_input = f"Agent Responses:\n{chr(10).join(st.session_state.agent_responses)}\n\nUser Feedback:\n{feedback}"
            print("Feedback sent to LLM:", full_input)  # Debugging

            # Increment iteration
            st.session_state.iteration += 1

            # Restart discussion with feedback
            st.rerun()

if __name__ == "__main__":
    run()
