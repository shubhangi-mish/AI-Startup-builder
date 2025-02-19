import json
import os

class MemoryManager:
    """Handles iterative short-term memory updates for multiple agents."""

    def __init__(self, short_term_rounds=5, memory_file="memory.json"):
        self.memory_file = memory_file
        self.short_term_rounds = short_term_rounds
        self.memory = self.load_memory()

    def load_memory(self):
        """Load memory from file or initialize a new one."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print("⚠️ Warning: Memory file is corrupted. Reinitializing memory.")
                return self.initialize_memory()
        return self.initialize_memory()

    def initialize_memory(self):
        """Initialize default memory structure for all crews."""
        return {
            "user": [],
            "crews": {
                "technologist": [],
                "marketer": [],
                "designer": [],
                "product_manager": []
            }
        }

    def save_memory(self):
        """Save updated memory to file."""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memory, f, indent=4)
        except IOError as e:
            print(f"❌ Error saving memory: {e}")

    def load(self, agent_name):
        """Retrieve memory for an agent (last N interactions)."""
        if agent_name == "user":
            return self.memory["user"][-self.short_term_rounds:]
        return self.memory["crews"].get(agent_name, [])[-self.short_term_rounds:]

    def update_memory(self, agent_name, new_data):
        """Append new data to agent memory and retain only the last N rounds."""
        if agent_name == "user":
            self.memory["user"].append(new_data)
            self.memory["user"] = self.memory["user"][-self.short_term_rounds:]
        else:
            if agent_name not in self.memory["crews"]:
                self.memory["crews"][agent_name] = []
            self.memory["crews"][agent_name].append(new_data)
            self.memory["crews"][agent_name] = self.memory["crews"][agent_name][-self.short_term_rounds:]

        self.save_memory()
        print(f"✅ Memory updated for {agent_name}: {self.load(agent_name)}")  # Debugging info

    def integrate_feedback(self, user_feedback):
        """Store user feedback globally and propagate to all crews."""
        self.update_memory("user", user_feedback)
        for agent in self.memory["crews"]:
            self.update_memory(agent, f"User Feedback: {user_feedback}")
