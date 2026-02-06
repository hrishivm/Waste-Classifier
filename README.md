
# ♻️Waste Classification AI

  A Deep Learning project to classify E-waste, HDPE, and PET plastics using ConvNeXt-Tiny.

## 🚀 Project Overview

  This project addresses the challenge of automated waste sorting. Using the FastAI framework and Progressive 
  Resizing (training first at 224px, then refining at 448px), the model achieves high accuracy on complex 
  materials like crushed plastics and electronic components.
    * Architecture: ConvNeXt-Tiny
    * Technique: Progressive Resizing (224px -> 448px)
    * Optimizer: Mixed Precision (FP16) for RTX 3050 optimization

## 📈 Performance & Results

  The model was trained for 3 epochs at 224px and further refined for 3 epochs at 448px.
    * Final Accuracy: 97.47%

## 📊 Dataset Setup

  Due to GitHub's file size limits, the dataset is hosted externally.
  1. Download: https://drive.google.com/file/d/1ktB-7vzbcAc5efoqpE6zTpd13vQ3HklH/view?usp=sharing
  2. Extract: Place the Train/ and Test/ folders in the root directory.
  3. Structure:
    ```text
    /Waste_Classifier
    ├── Train/ (HDPE, PET, E-waste)
    └── Test/  (HDPE, PET, E-waste)
     ```
  *"This dataset is a curated collection of images sourced from Kaggle (Waste Classification Dataset) and Roboflow (Plastic Sort). All rights belong to the original creators."
  
## 🛠️ Installation & Usage

  1. Clone & Environment
  ```bash
  git clone https://github.com/hrishivm/Waste-Classifier.git
  cd Waste-Classifier
  python -m venv venv
  source venv\Scripts\activate
  ```
  2. Install Dependencies
  ```bash
  pip install -r requirements.txt
  ```
  3. Run Inference To test a single image using the modular inference.py script:
  ```bash
  python app.py
  ```

## 📂 Project Structure

  * ai_model.ipynb: The complete training pipeline (Stages 1 & 2).
  * inference.py: A reusable Python class for model deployment.
  * app.py: Interface for testing images.
  * requirements.txt: List of required Python libraries.
  * .gitignore: Configured to exclude bulky environment files and model weights.
