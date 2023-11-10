from flask import Flask, render_template
# Import the parsing functions from your parsing script
from your_parsing_script import read_journal, parse_journal_entries

app = Flask(__name__)

# Read and parse the journal entries
file_path = '/Users/benberkman/Desktop/cb/output.txt'  # Replace with your file path
journal_content = read_journal(file_path)
parsed_entries = parse_journal_entries(journal_content)

@app.route('/')
def home():
    # Create a list of tuples (index, entry) for use in the template
    entries_with_index = [(index, entry) for index, entry in enumerate(parsed_entries)]
    return render_template('home.html', entries=entries_with_index)

@app.route('/entry/<int:index>')
def show_entry(index):
    # Fetch the specific entry using the index
    entry = parsed_entries[index]
    return render_template('entry.html', entry=entry)

if __name__ == '__main__':
    app.run(debug=True)
