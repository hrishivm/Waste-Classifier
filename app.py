import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from inference import WasteClassifier  # Your class from earlier

# 1. Initialize API and Model
app = FastAPI(title="ConvNeXt-50 Waste Classifier API")

# Add CORS so you can call this from a website or mobile app later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    clf = WasteClassifier('waste_model_448_final_v3.pkl')
except Exception as e:
    print(f"Error loading model: {e}")

@app.get("/")
def health_check():
    return {"status": "online", "model": "ConvNeXt-50", "resolution": "448px"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # 2. Read bytes and convert to PIL Image
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content)).convert("RGB")
        
        # 3. Run Inference
        # Note: Fastai's 'predict' method can take a PIL Image directly
        result = clf.predict(img)
        
        return {
            "filename": file.filename,
            "prediction": result["category"],
            "confidence": f"{result['confidence'] * 100:.2f}%",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run locally: uvicorn app:app --host 0.0.0.0 --port 8000