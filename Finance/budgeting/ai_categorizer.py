import os
import pickle
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from .models import Transaction
from django.db import models


MODEL_PATH = "budgeting/trained_model.pkl"

def clean_text(text):
    """ Basic text cleaning: remove special characters & convert to lowercase """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    return text.strip()

def train_categorization_model():
    """ Train AI model with better preprocessing & scaling """

    transactions = Transaction.objects.exclude(category__isnull=True).exclude(category="")

    if not transactions.exists():
        print("⚠️ Not enough data to train the model.")
        return

    texts = [clean_text(txn.name) for txn in transactions]  # ✅ Cleaned text
    amounts = [float(txn.amount) for txn in transactions]
    categories = [txn.category for txn in transactions]

    # ✅ TF-IDF Vectorization
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Use bigrams for better text understanding
    text_features = vectorizer.fit_transform(texts).toarray()

    # ✅ Feature Scaling for Amounts
    scaler = StandardScaler()
    amounts_scaled = scaler.fit_transform(np.array(amounts).reshape(-1, 1))

    # ✅ Combine text features & scaled amounts
    features = np.column_stack((text_features, amounts_scaled))

    # ✅ Train a Random Forest model with better hyperparameters
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model.fit(features, categories)

    # ✅ Save the trained model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, scaler, model), f)

    print("✅ AI Model Trained & Improved!")


def predict_category(transaction_name, transaction_amount):
    """ Predicts category with confidence score """
    if not os.path.exists(MODEL_PATH):
        print("⚠️ No trained model found.")
        return None, None

    with open(MODEL_PATH, "rb") as f:
        vectorizer, scaler, model = pickle.load(f)

    cleaned_text = clean_text(transaction_name)
    text_feature = vectorizer.transform([cleaned_text]).toarray()
    amount_scaled = scaler.transform([[transaction_amount]])

    features = np.column_stack((text_feature, amount_scaled))
    prediction_proba = model.predict_proba(features)

    predicted_category = model.classes_[np.argmax(prediction_proba)]
    confidence = np.max(prediction_proba)  # ✅ Get highest probability

    return predicted_category, confidence

def evaluate_model_accuracy():
    """ Evaluates the AI model based on user feedback """
    total_transactions = Transaction.objects.filter(ai_predicted_category__isnull=False).count()
    correct_predictions = Transaction.objects.filter(ai_predicted_category=models.F("category"), ai_approved=True).count()

    if total_transactions == 0:
        return 0.0  # Avoid division by zero

    accuracy = (correct_predictions / total_transactions) * 100
    return round(accuracy, 2)