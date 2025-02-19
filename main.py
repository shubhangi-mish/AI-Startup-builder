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

    if st.button("Start Discussion"):
        inputs = {
            'topic': user_input,
            'current_year': str(datetime.now().year)
        }
        print(f"🔍 Inputs: {inputs}")

        try:
            # Create MultiagentStartupBuilder instance
            startup_builder = MultiagentStartupBuilder()
            crews = startup_builder.run_all_crews()

            st.subheader("🗣️ Multi-Agent Discussion")
            col1, col2 = st.columns(2)

            i = 0  # Track column placement

            for crew_name, crew in crews.items():
                print(f"\n🚀 **Executing {crew_name}**")
                output = crew.kickoff()
                print(type(output))  # Debugging: Show output type
                print(f"\n📝 **{crew_name} Output:**")
                print(output)

                # Convert CrewOutput to text if needed
                response_text = output.text if hasattr(output, "text") else str(output)
                agent_name = CREW_NAMES.get(crew_name, crew_name)

                # Display response in styled box
                response_box = f"""
                    <div style="border: 2px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0; 
                                background-color: {'#f9f9f9' if i % 2 == 0 else '#eaf4fc'};">
                        <h4>{agent_name}</h4>
                        <p>{response_text}</p>
                    </div>
                """
                if i % 2 == 0:
                    with col1:
                        st.markdown(response_box, unsafe_allow_html=True)
                else:
                    with col2:
                        st.markdown(response_box, unsafe_allow_html=True)
                
                i += 1  # Alternate columns for display

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run()
