from __future__ import annotations

import math
from pathlib import Path
from typing import Literal

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
PredictionLabel = Literal["spam", "ham"]


class PredictRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=20_000)


class PredictResponse(BaseModel):
    prediction: PredictionLabel
    confidence: float
    important_words: list[str]


app = FastAPI(
    title="Spam Mail Classifier API",
    description="Classifies email messages as spam or ham using TF-IDF and Multinomial Naive Bayes.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://spammailclassifier.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_model() -> Pipeline:
    if not MODEL_PATH.exists():
        raise RuntimeError("model.pkl not found. Run `python train.py` inside backend first.")
    return joblib.load(MODEL_PATH)


model = load_model()


def extract_important_words(pipeline: Pipeline, message: str, predicted_label: str) -> list[str]:
    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["classifier"]
    transformed = vectorizer.transform([message])
    feature_names = vectorizer.get_feature_names_out()
    class_index = list(classifier.classes_).index(predicted_label)

    row = transformed.tocoo()
    weighted_terms: list[tuple[str, float]] = []

    for _, feature_index, tfidf_value in zip(row.row, row.col, row.data):
        token = feature_names[feature_index]
        class_weight = classifier.feature_log_prob_[class_index][feature_index]
        weighted_terms.append((token, float(tfidf_value * math.exp(class_weight))))

    weighted_terms.sort(key=lambda item: item[1], reverse=True)
    return [term for term, _ in weighted_terms[:5]]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    probabilities = model.predict_proba([message])[0]
    classes = list(model.classes_)
    best_index = int(probabilities.argmax())
    prediction = classes[best_index]
    confidence = round(float(probabilities[best_index]), 4)
    important_words = extract_important_words(model, message, prediction)

    return PredictResponse(
        prediction=prediction,
        confidence=confidence,
        important_words=important_words,
    )
