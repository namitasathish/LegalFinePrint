# backend/tasks.py

import torch
from transformers import pipeline
from celery import Celery
from config import Config
from classifier_utils import is_legal_document
from ocr_utils import extract_text
from nlp_utils import segment_and_score

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

# Load offline pipelines (do this only once)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")  
explainer = pipeline("text2text-generation", model="google/flan-t5-small")

@celery.task(bind=True)
def analyze_document(self, filepath):
    try:
        sample = extract_text(filepath)[:5000]
        if not is_legal_document(sample):
            return {"error": "NOT_LEGAL"}

        full_text = extract_text(filepath)
        clauses = segment_and_score(full_text)
        results = []

        for c in clauses:
            text = c["text"]

            summary = summarizer(text[:1024], max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
            
            prompt = f"Explain in simple, non-legal terms:\n{text}"
            explanation = explainer(prompt, max_length=200, do_sample=False)[0]["generated_text"]

            results.append({
                "text": text,
                "risk_label": c["risk_label"],
                "summary": summary,
                "analysis": explanation
            })

        return {"results": results}

    except Exception as e:
        return {"error": "PROCESSING_FAILED", "message": str(e)}
