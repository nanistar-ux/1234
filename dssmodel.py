import joblib
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = os.path.join(os.path.dirname(__file__), "dss_model.pkl")

def train_dummy_model():
    """Train a small RandomForest model for land size → scheme mapping."""
    X = np.array([[0.5], [1.5], [3.0], [5.0], [8.0]])
    y = ["Small-Land Support", "Medium-Land Support", "Medium-Land Support", "Large-Land Support", "Large-Land Support"]
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    if not os.path.exists(MODEL_PATH):
        return train_dummy_model()
    return joblib.load(MODEL_PATH)

MODEL = load_model()

def recommend_schemes(fields: dict):
    """Use trained model to recommend schemes based on land size."""
    area = fields.get("area_ha")
    if not area:
        return ["Field Survey Required"]
    pred = MODEL.predict([[area]])[0]
    return [pred]
