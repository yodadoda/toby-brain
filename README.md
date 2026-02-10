# 🧠 Project TOBY: The Brain Subsystem

## Introduction
Welcome to the **Brain** module of Project TOBY. This repository contains the code for the robot's central reasoning engine.

Unlike simple robots that follow hard-coded `if/else` rules, TOBY uses a **Small Language Model (SLM)** to understand natural language. This allows users to give complex commands without us needing to write specific code for every possible sentence.

### What does this module do?
1.  **Natural Language Understanding (NLU):** Converts messy human speech into structured data.
2.  **Reasoning:** Decides *what* to do based on the user's command.
3.  **Personality:** Generates the robot's spoken responses (via Text-to-Speech later).
4.  **Command Generation:** Outputs JSON instructions that the Navigation and Arm subsystems can execute.

## Architecture: How it Connects
The "Brain" sits in the middle of the robot's software stack. It does not see or hear directly; it processes text and outputs logic.

```mermaid
graph TD
    A[Microphone (Ear)] -->|Text| B(Brain / toby_brain)
    C[Camera (Eye)] -->|Object List| B
    B -->|JSON Command| D[Navigation Stack (Legs)]
    B -->|JSON Command| E[Robotic Arm (Hands)]
    B -->|Text Response| F[Speaker (Mouth)]