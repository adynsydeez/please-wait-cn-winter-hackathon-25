# please-wait-cn-winter-hackathon-25

A simple Python application that combines a tiny language model with ASCII art face animation. The program generates text iteratively while displaying an animated face that appears to "speak" by alternating between idle and mouth-open states.

## Features

- Local tiny language model inference using Transformers
- ASCII art face animation synchronized with text generation
- Cross-platform console clearing (Windows, macOS, Linux)
- Customizable generation parameters

## Installation

### 1. Clone or download this repository

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up the model

Place your tiny language model files in the following directory structure:
```
LLM_model/
└── tiny_llm_weight/
    ├── config.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    ├── vocab.txt 
```

## Usage

Run the main application:

```bash
python Main.py
```

The program will:
1. Start with the prompt "Rose are red."
2. Generate text iteratively using the tiny LLM
3. Display an animated ASCII face that alternates between idle and speaking states
4. Continue for 25 iterations with 0.1-second delays between frames

## Configuration

You can modify the following parameters in `dumb_tinyLLM.py`:

- `max_new_tokens`: Number of new tokens to generate per iteration (default: 2)
- `temperature`: Controls randomness in generation (default: 1)
- `top_k`: Limits vocabulary for sampling (default: 50)
- `top_p`: Nucleus sampling parameter (default: 0.95)

## Requirements

- Python 3.7+
- PyTorch 2.8.0
- Transformers 4.55.0
- Compatible tiny language model files
- ASCII art face files