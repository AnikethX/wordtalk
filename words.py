import random
import streamlit as st

# Telugu slang words collection
FALLBACK_WORDS = [
    "డబ్బు", "అమ్మ", "బండి", "చిన్నోడు", "గోలీ", "బ్రదర్", "వాడి", "పల్సు",
    "లైన్", "లవ్", "గోల", "పాన్", "కిర్రాక్", "ఫుల్", "దమ్ము", "జోష్",
    "పాట", "పంకా", "చిల్లర", "రేంజ్", "బ్రేకప్", "బిజీ", "సీన్", "క్యాచ్",
    "ఫాస్ట్", "బోర్", "గెప్", "లేటెస్ట్", "టెంపర్", "టచ్", "టైటిల్", "గిఫ్ట్",
    "బుక్", "వెయిట్", "చాన్స్", "లక్", "మూడ్", "ఆటో", "కాల్", "మెస్సేజ్",
    "ఫోటో", "వీడియో", "గేమ్", "చాట్", "ఫ్రెండ్", "గ్రూప్", "స్కూల్", "కాలేజ్"
]

# Categorized words for themed challenges
CATEGORY_WORDS = {
    "Youth Culture": ["బ్రదర్", "సిస్టర్", "కూల్", "స్టైల్", "ట్రెండ్", "వైబ్స్"],
    "Social Media": ["లైక్", "షేర్", "పోస్ట్", "స్టోరీ", "రీల్స్", "చాట్"],
    "Urban Slang": ["డబ్బు", "పైసా", "రేంజ్", "లెవెల్", "క్లాస్", "స్టేటస్"],
    "Entertainment": ["మూవీ", "సాంగ్", "డాన్స్", "పార్టీ", "ఫన్", "ఎంజాయ్"],
    "General": ["బండి", "అమ్మ", "నాన్న", "ఇల్లు", "స్కూల్", "కాలేజ్"]
}
def get_words(n=3):
    """Get random Telugu slang words"""
    if len(FALLBACK_WORDS) < n:
        return FALLBACK_WORDS
    return random.sample(FALLBACK_WORDS, n)

def get_themed_words(category, n=3):
    """Get words from a specific category"""
    if category in CATEGORY_WORDS:
        words = CATEGORY_WORDS[category]
        if len(words) < n:
            # Add some general words if category doesn't have enough
            words.extend(random.sample(FALLBACK_WORDS, n - len(words)))
        return random.sample(words, min(n, len(words)))
    return get_words(n)

def get_difficulty_words(difficulty, n=3):
    """Get words based on difficulty level"""
    if difficulty == "Easy":
        easy_words = ["అమ్మ", "నాన్న", "ఇల్లు", "స్కూల్", "బండి", "పాట"]
        return random.sample(easy_words, min(n, len(easy_words)))
    elif difficulty == "Hard":
        hard_words = ["కిర్రాక్", "పంకా", "గెప్", "టెంపర్", "రేంజ్", "లెవెల్"]
        return random.sample(hard_words, min(n, len(hard_words)))
    else:
        return get_words(n)

def get_challenge_words():
    """Get special challenge words"""
    challenge_types = [
        {"type": "Rhyme Challenge", "words": ["పాట", "గోట", "నోట"], "bonus": "Extra points for rhyming explanations!"},
        {"type": "Story Challenge", "words": ["హీరో", "విలన్", "క్లైమాక్స్"], "bonus": "Create a mini story!"},
        {"type": "Emotion Challenge", "words": ["జోష్", "టెన్షన్", "హ్యాపీ"], "bonus": "Express the emotions!"},
        {"type": "Action Challenge", "words": ["రన్", "జంప్", "డాన్స్"], "bonus": "Describe the actions!"}
    ]
    
    return random.choice(challenge_types)