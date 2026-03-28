from fastai.vision.all import *

class WasteClassifier:
    def __init__(self):
        self.learn = load_learner('waste_classifier_v3.pkl') 

    def predict(self, image):
        pred, pred_idx, probs = self.learn.predict(image)
        check = self.filter(probs[pred_idx])

        print("\n\n---------------RESULT---------------")
        if check == True:
            print(f"Given image is {pred} with confidence {probs[pred_idx]:.4f}.")
        else:
            print(f"Model is not confident enough, need manual checking!")

    def filter(self, num):
        if num > 0.7500:
            return True
        return False


if __name__ == "__main__":
    model = WasteClassifier()
    image = "D:\Desktop\waste-classifier\Samples_v3\Images\wrong_charger_0.581.jpg"
    model.predict(image)