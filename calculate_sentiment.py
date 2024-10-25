import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np


def calculate_sentiment_scores(entries):
    # Load the model and tokenizer
    model_name = "j-hartmann/emotion-english-distilroberta-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    emotion_results = {}
    
    for entry in entries:
        # Tokenize and encode the entry
        inputs = tokenizer(entry['entry'], return_tensors="pt", truncation=True, max_length=512)
        
        # Get model output
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get probabilities
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Convert to numpy and get the highest probability
        probs_np = probs.numpy()
        label_id = np.argmax(probs_np)
        
        # Map the index to the corresponding emotion label
        emotion_labels = model.config.id2label
        emotion = emotion_labels[label_id]
        score = probs_np[0][label_id]
        
        # Store the emotion and its confidence score
        emotion_results[entry['date']] = {
            'emotion': emotion,
            'confidence': round(float(score), 2)
        }
    
    return emotion_results

def main():
    # Load entries
    with open('journalEntries.json', 'r') as f:
        entries = json.load(f)
    
    # Calculate emotion results
    emotion_results = calculate_sentiment_scores(entries)
    
    # Save emotion results
    with open('emotion_results.json', 'w') as f:
        json.dump(emotion_results, f)
    
    print("Emotion results calculated and saved to emotion_results.json")

if __name__ == "__main__":
    main()
