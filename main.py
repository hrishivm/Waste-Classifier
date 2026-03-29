import os
import pathlib
import platform
import requests
from fastapi import FastAPI, File, UploadFile
from fastai.vision.all import load_learner
import uvicorn
import io
from PIL import Image

# Fix WindowsPath issue
if platform.system() != "Windows":
    pathlib.WindowsPath = pathlib.PosixPath

app = FastAPI(title="Waste Classifier API")

MODEL_URL = "https://huggingface.co/abhiramAnanathu/Repay-ai/resolve/main/waste_classifier_v3.pkl"
MODEL_PATH = "model.pkl"

learn = None  # global model


# ✅ Download model if not present
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")

        try:
            with requests.get(MODEL_URL, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(MODEL_PATH, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            print("✅ Model downloaded successfully")

        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            raise e


# ✅ Load model on startup (best practice)
@app.on_event("startup")
def load_model():
    global learn
    try:
        download_model()
        learn = load_learner(MODEL_PATH)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        learn = None


def filter_confidence(num):
    return num > 0.75


@app.get("/")
async def root():
    return {"message": "Waste Classifier API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if learn is None:
        return {"error": "Model not loaded"}

    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    pred, pred_idx, probs = learn.predict(img)
    confidence = float(probs[pred_idx])

    is_confident = filter_confidence(confidence)

    return {
        "prediction": str(pred),
        "confidence": confidence,
        "is_confident": is_confident,
        "message": f"Given image is {pred} with confidence {confidence:.4f}."
        if is_confident
        else "Model is not confident enough, need manual checking!",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
