import csv
import json

def add_emotions_to_entries():
    # Load the existing journal entries
    with open('journalEntries.json', 'r') as f:
        entries = json.load(f)

    # Read the emotions CSV file
    with open('emotions.csv', 'r') as f:
        csv_reader = csv.DictReader(f)
        emotions_data = list(csv_reader)

    # Ensure the number of entries matches the number of rows in the CSV
    if len(entries) != len(emotions_data):
        raise ValueError("The number of entries in journalEntries.json does not match the number of rows in emotions.csv")

    # Add emotion data to each entry
    for entry, emotion_row in zip(entries, emotions_data):
        entry['label'] = emotion_row['label']
        entry['score'] = float(emotion_row['score'])
        entry['anger'] = float(emotion_row['anger'])
        entry['disgust'] = float(emotion_row['disgust'])
        entry['fear'] = float(emotion_row['fear'])
        entry['joy'] = float(emotion_row['joy'])
        entry['neutral'] = float(emotion_row['neutral'])
        entry['sadness'] = float(emotion_row['sadness'])
        entry['surprise'] = float(emotion_row['surprise'])

    # Save the updated entries back to the JSON file
    with open('journalEntries_with_emotions.json', 'w') as f:
        json.dump(entries, f, indent=2)

    print("Emotions data added to journal entries and saved to journalEntries_with_emotions.json")

if __name__ == "__main__":
    add_emotions_to_entries()
