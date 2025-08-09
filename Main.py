import os
import time
from LLM_model.dumb_tinyLLM import tinyLLM_infer

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

faceFrames = {"idle": open("images/ascii/face-idle-1.txt", "r").read(),
        "mouth-open-1": open("images/ascii/face-idle-mouth-open-1.txt", "r").read(), }


# testSpeak = "Hello, this is a test of the face animation system. It should display a simple animation of a face opening its mouth."
# Define your prompt
prompt = "Rose are red."
generated_text = prompt
print(prompt, end="")

for i in range(25):
    clear_console()
    print(faceFrames["idle"])
    generated_text = tinyLLM_infer(generated_text)
    print(generated_text)
    time.sleep(0.1)
    clear_console()
    print(faceFrames["mouth-open-1"])
    generated_text = tinyLLM_infer(generated_text)
    print(generated_text)
    time.sleep(0.1)