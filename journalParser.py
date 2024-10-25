import re
from datetime import datetime
import json  # Add this import

# Function to clean the content by removing specific patterns
def clean_content(content):
    # Pattern to match 'numerator / 1.901' where numerator is <= 1.901
    pattern = r'\b([0-9]{1,2}(?:\.[0-9]{1,3})?) / 1\.901\b'
    content = re.sub(pattern, '', content)
    
    # Remove literal '\n' strings
    # content = content.replace('\\n', '')
    
    return content

# Function to read the content of the journal file
def read_journal(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def parse_journal_entries(content):
    entries = []
    # Pattern to identify the start of a journal entry (author and date)
    entry_pattern = re.compile(r'by (Willa Silverman|Ben Berkman|Ethan Silverman), \w+ \d{1,2}, \d{4}')

    entries_start = [match.start() for match in re.finditer(entry_pattern, content)]

    for i in range(len(entries_start)):
        start = entries_start[i]
        end = entries_start[i + 1] if i + 1 < len(entries_start) else len(content)

        # Extract the whole entry content
        entry_content = content[start:end].strip()

        # Extracting and formatting the title, author, and date
        title_start = content.rfind('\n', 0, start)
        title_end = content.rfind('\n', 0, title_start)
        title = content[title_end:title_start].strip()

        author_date_line = content[start:content.find('\n', start)].strip()
        author, date = author_date_line.split(',', 1)
        author = author.replace('by ', '').strip()
        date = date.strip()

        # Removing the redundant author-date line from the entry content
        entry_text = entry_content.replace(author_date_line, "", 1).strip()

        # Splitting entry content and comments
        comments_start = re.search(r'\nComments\n', entry_text)
        if comments_start:
            comments = entry_text[comments_start.end():].strip()
            entry_text = entry_text[:comments_start.start()].strip()
        else:
            comments = ""

        entries.append({
            'title': title,
            'author': author,
            'date': date,
            'entry': entry_text,
            'comments': comments
        })

    return entries

# Function to write entries to a JSON file
def write_entries_to_json(entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(entries, json_file, ensure_ascii=False, indent=4)

file_path = "journal_txt.txt"
journal_content = read_journal(file_path)
journal_content = clean_content(journal_content)  # Clean the content

parsed_entries = parse_journal_entries(journal_content)
write_entries_to_json(parsed_entries, "journalEntries.json")  # Call the new function