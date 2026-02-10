import os
import urllib.request

MODEL_PATH = "toby-brain-q4.gguf"
MODEL_URL = "https://huggingface.co/path/to/your/model/resolve/main/toby-brain-q4.gguf"

if not os.path.exists(MODEL_PATH):
    print(f"Downloading model to {MODEL_PATH}...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Download complete!")
else:
    print("Model already exists.")
