from fastai.vision.all import *

class WasteClassifier:
    def __init__(self, model_path='waste_model_448_final_v3.pkl'):
        self.learn = load_learner(model_path)
        
    def predict(self, img_path):
        """Predicts the category of the given image"""
        pred, _, probs = self.learn.predict(img_path)
        return {"category": pred, "confidence": float(probs.max())}

