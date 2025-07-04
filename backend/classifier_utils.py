import spacy
from spacy.matcher import PhraseMatcher
import openai
from config import Config

nlp = spacy.load("en_core_web_sm")
openai.api_key = Config.OPENAI_API_KEY

LEGAL_TERMS = [
    "agreement","party","hereby","witnesseth","term","renewal",
    "liability","indemnify","governing law","jurisdiction","confidential",
    "force majeure","intellectual property","termination","breach",
    "arbitration","severability","assignment","representation","warranty"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(term) for term in LEGAL_TERMS]
matcher.add("LEGAL_TERMS", patterns)

def is_legal_document(text: str, fallback_to_llm: bool = True) -> bool:
    doc = nlp(text)
    matches = matcher(doc)
    distinct = {doc[start:end].text.lower() for _, start, end in matches}
    match_count = len(distinct)
    sentence_count = max(len(list(doc.sents)), 1)
    density = match_count / sentence_count

    if match_count >= 5 or density >= 0.05:
        return True
    if match_count <= 1 and density < 0.01:
        return False

    if fallback_to_llm:
        prompt = (
            "You are a classifier. Answer ‘Yes’ or ‘No’ only.\n"
            "Is this an excerpt from a legal contract, agreement, or policy?\n\n"
            f"{text[:3000]}"
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                timeout=10
            )
            return resp.choices[0].message.content.strip().lower().startswith("yes")
        except:
            return False

    return False
