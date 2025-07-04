import spacy

nlp = spacy.load("en_core_web_sm")

RISK_KEYWORDS = {
    "Auto-Renewal": ["renew automatically", "extension unless"],
    "Hidden Fee": ["may be billed", "additional charges"],
    "Unilateral Amendment": ["reserve the right to", "may amend terms"]
}

def segment_and_score(text: str):
    doc = nlp(text)
    clauses = []
    for sent in doc.sents:
        clause = sent.text.strip()
        score = 0
        label = "Normal"
        for lbl, kws in RISK_KEYWORDS.items():
            if any(kw in clause.lower() for kw in kws):
                score += 1
                label = lbl
        clauses.append({"text": clause, "risk_score": score, "risk_label": label})
    return sorted(clauses, key=lambda c: c["risk_score"], reverse=True)
