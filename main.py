from fastapi import FastAPI, File, UploadFile
from fastai.vision.all import *
import uvicorn
import io
from PIL import Image
import os

app = FastAPI(title="Waste Classifier API")

# Load model
model_path = 'waste_classifier_v3.pkl'
try:
    learn = load_learner(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
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
    
    # Read image
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # Fastai's predict works with PIL images if they are converted to fastai format or handled correctly
    # Alternatively, we can save temporarily or use the fastai way
    # For fastai learn.predict(img) usually works if img is a PIL image
    
    pred, pred_idx, probs = learn.predict(img)
    confidence = float(probs[pred_idx])
    
    is_confident = filter_confidence(confidence)
    
    return {
        "prediction": str(pred),
        "confidence": confidence,
        "is_confident": is_confident,
        "message": f"Given image is {pred} with confidence {confidence:.4f}." if is_confident else "Model is not confident enough, need manual checking!"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
