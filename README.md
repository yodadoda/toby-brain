# Project TOBY: The Brain subsystem
___
## Introduction
Welcome to the Brain module of Project TOBY. This repository contains the code for the robot's central reasoning engine.

Unlike simple robots that follow hard-coded `if/else` rules, TOBY uses a quantized LLM model to understand natural language. This allows users to give complex commands without us needing to write specific code for every possible sentence.

### What does this module do?
1. **Natural Language Understanding (NLU):** Converts messy human speech into structured data.
2. **Reasoning:** Decides what to do based on the user's command.
3. **Personality: **Generates the robot's spoken responses (via Text-to-Speech later)
4. **Command Generation: **Outputs JSON instructions that the Navigation and Arm subsystems can execute.


```mermaid
graph TD
    A["Microphone (Ear)"] -->|Text| B("Brain / toby_brain")
    C["Camera (Eye)"] -->|Object List| B
    B -->|JSON Command| D["Navigation Stack (Legs)"]
    B -->|JSON Command| E["Robotic Arm (Hands)"]
    B -->|Text Response| F["Speaker (Mouth)"]
````

## Getting Started

### Prerequisites
- **Hardware:** A laptop (Windows/Mac/Linux) or NVIDIA Jetson. 8GB+ RAM recommended.
- **Software:** Python 3.10+, Git.

### 1. Clone the Repository
Open your terminal and download the code:

Bash
```
git clone https://github.com/yodadoda/toby-brain
cd toby-brain
```

### 2. Set Up the Virtual Environment
We use a virtual environment (`venv`) to keep our libraries isolated.

**Linux / Mac:**

Bash
```
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

PowerShell
```
python -m venv venv
.\venv\Scripts\Activate
```

_(You will see `(venv)` appear at the start of your terminal line when active.)_

### 3. Install Dependencies
Install the required Python libraries (mainly `llama-cpp-python` for running the AI):

Bash
```
pip install llama-cpp-python huggingface-hub
pip install -r requirements.txt
```

### 4. Download the Model
We use a **Quantized (Compressed)** version of Microsoft's Phi-3.5 model. It is hosted on our custom Hugging Face repo.

- **Model Link:** [yodadoda/toby](https://huggingface.co/yodadoda/toby/tree/main)
- **File to Download:** `toby-brain-q4.gguf`

**Option A: Automatic Download (Recommended)**
Run the setup script included in this repo:

Bash
```
python download_raw.py
```

**Option B: Manual Download**
1. Go to the [Model Link](https://huggingface.co/yodadoda/toby/tree/main).
2. Download `toby-brain-q4.gguf`.
3. Place the file directly inside this `toby-brain` folder.
---

## How to Run It

### The Interactive Mode
To chat with TOBY directly in your terminal:

Bash
```
python brain.py
```

- **Type:** "Hello, who are you?" -> TOBY should reply.
- **Type:** "Go to the kitchen." -> TOBY should output a JSON command.
- **Exit:** Type `exit` or `quit`.

### The CLI Mode (For Testing Inputs)
You can pipe a single command to see the output instantly:

Bash
```
python brain.py --prompt "Pick up the red ball"
```

---
## Configuration & Parameters
In `brain.py`, you will see several settings (parameters) that control the robot's "psychology." Here is what they mean and how to tune them.

| **Parameter**         | **Current Value** | **Description**                                                                                                                                                     |
| --------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`n_ctx`** (Context) | `4096`            | **Memory Size:** How many words TOBY remembers in the current conversation. Higher = Better memory, but slower and uses more RAM.                                   |
| **`temperature`**     | `0.2`             | **Creativity.**<br>• `0.0` = Robot logic (Always same answer).<br>• `1.0` = Creative writing (Unpredictable).<br><br>We keep this **low** so commands are reliable. |
| **`max_tokens`**      | `200`             | **Verbosity.** The maximum length of a reply. We limit this so the robot doesn't write a novel when you ask for the time.<br>                                       |
| **`top_p`**           | `0.95`            | **Focus.**"Nucleus Sampling." Limits the AI to choosing from the top 95% most likely words. Prevents gibberish.<br>                                                 |
| **`system_prompt`**   | _See code_        | **Identity.** The "Hidden Instructions" given to the brain before the conversation starts. This defines that it is a _robot_, not a chatbot.<br>                    |

### How to Change Them
You can modify these directly in the `TobyBrain` class inside `brain.py`:

Python
```
# Example: Making TOBY more creative
output = self.llm(
    prompt_to_feed,
    temperature=0.8,  # Changed from 0.2
    ...
)
```

---

## Contributing

1. **Create a Branch:** `git checkout -b feature/better-prompts`
2. **Make Changes:** Edit `brain.py`.
3. **Test:** Run `python brain.py` and verify TOBY still acts like a robot.
4. **Push:** `git push origin feature/better-prompts`    

---

## Troubleshooting

**"Model not found" error?**
- Ensure `toby-brain-q4.gguf` is in the **exact same folder** as `brain.py`.
- Check the filename spelling.

**"out of memory" error?**
- Try reducing `n_ctx` from 4096 to 2048 in `brain.py`.

**TOBY is speaking gibberish?**
- Check the `temperature`. If it's too high (> 0.8), tååååhe model hallucinates.
