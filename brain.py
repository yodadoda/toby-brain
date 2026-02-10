import argparse
import json
import sys
from llama_cpp import Llama

class TobyBrain:
    def __init__(self, model_path, context_size=4096):

        """
        Initialize the Brain.
        DECISION: We load the model ONCE when the robot starts, not every time we ask a question.

        """
        print(f"Initializing TOBY Brain from {model_path}...")

        try:
            self.llm = Llama(
                model_path = model_path,
                n_ctx = context_size,  # Memory limit (tokens)
                n_gpu_layers = -1,     # -1 = Use GPU if available, 0 = CPU only
                verbose = False        # Keep the console clean
            )
            print("✅ Brain Loaded Successfully.")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)

        # DECISION: The System Prompt is the "Constituency" of the robot. 
        # It cannot be overridden by user chat.

        self.system_prompt = (
            "You are TOBY, a physical robot assistant. "
            "Directives: 1. Be concise. 2. If asked to move/act, output JSON only. "
            "3. Do not mention being an AI."
        )
        
        # The Short-Term Memory
        self.history = f"<|system|>\n{self.system_prompt}<|end|>\n"

    def think(self, user_input):
        """
        The main reasoning loop.
        1. Accept Input
        2. Append to Memory
        3. Generate Response
        4. Update Memory
        """

        # 1. Update History with User Input
        self.history += f"<|user|>\n{user_input}<|end|>\n"

        # 2. Prefill the Assistant tag to force the persona
        prompt_to_feed = self.history + "<|assistant|>\n"

        # 3. Run Inference (The actual "Thinking")
        output = self.llm(
            prompt_to_feed,
            max_tokens=200,      # DECISION: Cap response length for speed
            stop=["<|end|>", "<|user|>"], 
            temperature=0.2,     # DECISION: Low temp = precise/robotic. it can be between 0 and 1
            echo=False
        )
        response_text = output["choices"][0]["text"].strip()

        # 4. Save result to memory so we remember it next turn
        self.history += f"<|assistant|>\n{response_text}<|end|>\n"
        return response_text

# --- CLI HANDLER ---
# This block allows you to run "python brain.py" directly for testing
if __name__ == "__main__":
    # DECISION: Use argparse so we can change settings from the command line
    parser = argparse.ArgumentParser(description="TOBY Brain Interface")
    parser.add_argument("--model", type=str, default="./toby-brain-q4.gguf", help="Path to .gguf file")
    args = parser.parse_args()

    # Start the Brain
    bot = TobyBrain(model_path=args.model)

    print("\n🤖 TOBY is listening... (Type 'exit' to stop)\n")
    while True:
        try:
            user_in = input("You: ")
            if user_in.lower() in ["exit", "quit"]:
                break
            
            # The Magic Line:
            reply = bot.think(user_in)
            
            print(f"TOBY: {reply}")
            
        except KeyboardInterrupt:
            print("\nShutting down.")
            break