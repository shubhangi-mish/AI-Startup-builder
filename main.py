import sys
import warnings
import streamlit as st
import json
from datetime import datetime
from multiagent_startup_builder.crew import MultiagentStartupBuilder
from multiagent_startup_builder.memory import MemoryManager

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Initialize memory
memory = MemoryManager()
JSON_FILE = "conversation.json"  # File to save conversation history

def load_conversation():
    """Load previous conversation history from JSON file."""
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_conversation(conversation):
    """Save conversation history to a JSON file."""
    with open(JSON_FILE, "w") as f:
        json.dump(conversation, f, indent=4)

def run():
    """Run the multi-agent startup discussion."""
    st.title("🚀 Multi-Agent Startup Builder")
    st.write("Describe your startup idea and let AI agents collaborate!")

    # Load conversation history
    if "conversation" not in st.session_state:
        st.session_state["conversation"] = load_conversation()

    # Take user input
    user_input = st.text_area("Enter your startup idea:", "AI-driven recruitment platform")

    if st.button("Start Discussion"):
        inputs = {
            'topic': user_input,
            'current_year': str(datetime.now().year)
        }
        print(f"🔍 Inputs: {inputs}")

        try:
            crew_instance = MultiagentStartupBuilder().crew()
            print(f"🔍 Crew Instance: {crew_instance}")

            response = crew_instance.kickoff(inputs=inputs)
            print(f"🔍 Debug - Response Type: {type(response)} | Response: {response}")

            # Convert response to JSON-serializable format
            if isinstance(response, list):
                response = response[0] if response else "No valid response"
            response_str = str(response)

            # Update memory and session state
            memory.update_memory("user", response_str)
            st.session_state["conversation"].append({"iteration": len(st.session_state["conversation"]) + 1, "response": response_str})

            # Save conversation history
            save_conversation(st.session_state["conversation"])

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Display conversation history
    st.subheader("Conversation History")
    for entry in st.session_state["conversation"]:
        st.write(f"**Iteration {entry['iteration']}:**")
        st.text(entry["response"])

    # Feedback Loop
    feedback = st.text_area("Provide feedback for agents:", "")
    if st.button("Submit Feedback"):
        memory.update_memory("user", f"User Feedback: {feedback}")
        st.session_state["conversation"].append({"iteration": len(st.session_state["conversation"]) + 1, "response": f"User Feedback: {feedback}"})
        save_conversation(st.session_state["conversation"])  # Save feedback
        st.success("Feedback recorded! Agents will improve in the next iteration.")

if __name__ == "__main__":
    run()
