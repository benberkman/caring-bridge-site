from llama_cpp import Llama
import json
from datetime import datetime

class NERProcessor:
    def __init__(self, model_path):
        self.llm = Llama(model_path=model_path)

    def process_entry(self, entry):
        prompt = f"""
        Please analyze the following journal entry and extract information about people mentioned:
        
        Entry date: {entry['date']}
        Entry text: {entry['entry']}
        
        For each person mentioned, provide:
        1. Their name
        2. Their relationship to the author (if mentioned)
        3. Any significant events or emotions associated with them in this entry
        
        Return the results as a JSON object with the following structure:
        {{
            "date": "YYYY-MM-DD",
            "people": [
                {{
                    "name": "Person's name",
                    "relationship": "Relationship to author",
                    "context": "Brief description of their mention in the entry"
                }}
            ]
        }}
        """
        
        response = self.llm(prompt, max_tokens=2048, stop=["```"], echo=False)
        return json.loads(response['choices'][0]['text'])

    def process_all_entries(self, entries):
        results = []
        for entry in entries:
            results.append(self.process_entry(entry))
        return results

    def load_entries(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Extract only the 'entry' and 'date' fields from each JSON object
            entries = [{'date': item['date'], 'entry': item['entry']} for item in data]
        return entries

if __name__ == "__main__":
    # Example usage
    model_path = "/path/to/your/llama/model.bin"
    processor = NERProcessor(model_path)
    
    # Load entries from the JSON file
    entries = processor.load_entries('journalEntries_with_emotions.json')
    
    # Process a small subset of entries for testing
    test_entries = entries[:5]  # Process only the first 5 entries
    results = processor.process_all_entries(test_entries)
    
    # Print the results
    print(json.dumps(results, indent=2))
    
    print(f"Processed {len(results)} entries.")
