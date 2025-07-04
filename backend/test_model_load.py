from transformers import pipeline

def test_model_loading():
    print("⏳ Loading summarizer...")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("✅ Summarizer loaded successfully!")

    print("⏳ Loading explainer...")
    explainer = pipeline("text2text-generation", model="google/flan-t5-small")
    print("✅ Explainer loaded successfully!")

if __name__ == "__main__":
    test_model_loading()
