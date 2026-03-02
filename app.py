import os
from inference import WasteClassifier # Import your class

clf = WasteClassifier('waste_model_448_v2.pkl')

def main():
    print("--- Waste Classification CLI ---")
    test_img = r"D:\Desktop\Samples\Correct\metal_1.jpg"

    if os.path.exists(test_img):
        result = clf.predict(test_img)
        print(f"Result: {result}")
    else:
        print(f"Error: {test_img} not found.")

if __name__ == "__main__":
    main()