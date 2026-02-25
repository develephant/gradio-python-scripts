import json
import random
import os

def load_word_data(filename="chibi_word_data.json"):
    """Loads word lists and templates from a JSON file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Word data file '{filename}' not found.")
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def weighted_choice(word_list):
    """Selects a random word based on weights."""
    words, weights = zip(*word_list)
    return random.choices(words, weights=weights, k=1)[0]

def fix_indefinite_articles(sentence):
    """
    Replaces 'a' with 'an' before vowel sounds.
    Example: 'a alien' -> 'an alien'
    """
    words = sentence.split()
    for i in range(len(words) - 1):
        if words[i].lower() == "a" and words[i+1][0].lower() in "aeiou":
            words[i] = "an"
        elif words[i].lower() == "an" and words[i+1][0].lower() not in "aeiou":
            words[i] = "a"
    return " ".join(words)

def generate_sentence(data):
    """Generates a random sentence from templates and weighted word lists."""
    template = random.choice(data["templates"])
    sentence = template.format(
        age=weighted_choice(data["age"]),
        ethnicity=weighted_choice(data["ethnicity"]),
        body_type=weighted_choice(data["body_type"]),
        hair_length=weighted_choice(data["hair_length"]),
        hair_color=weighted_choice(data["hair_color"]),
        hair_style=weighted_choice(data["hair_style"]),
        eye_color=weighted_choice(data["eye_color"]),
        eye_wear=weighted_choice(data["eye_wear"]),
        mouth=weighted_choice(data["mouth"]),
        boobs=weighted_choice(data["boobs"]),
        nipples=weighted_choice(data["nipples"]),
        colors=weighted_choice(data["colors"]),
        chestwear=weighted_choice(data["chestwear"]),
        legwear=weighted_choice(data["legwear"]),
        footware=weighted_choice(data["footware"]),
        actions=weighted_choice(data["actions"]),
        place=weighted_choice(data["place"]),
        camera_shot=weighted_choice(data["camera_shot"]),
        camera_view=weighted_choice(data["camera_view"])
    )
    return fix_indefinite_articles(sentence)

def generate_paragraph(data, sentence_count=5):
    """Generates a paragraph with a given number of sentences."""
    sentences = [generate_sentence(data) for _ in range(sentence_count)]
    return " ".join(sentences)

def generate_story(data, paragraph_count=3, sentences_per_paragraph=5):
    """Generates multiple paragraphs."""
    return "\n\n".join(
        generate_paragraph(data, sentences_per_paragraph) for _ in range(paragraph_count)
    )

if __name__ == "__main__":
    try:
        data = load_word_data()
        print("📖 JSON-Powered Sentence Generator\n")
        story = generate_story(data, paragraph_count=2, sentences_per_paragraph=4)
        print(story)
    except Exception as e:
        print(f"Error: {e}")

