from flask import Flask, render_template, request
import json
from datetime import datetime, date
import re
from network_graph import NetworkGraphBuilder

app = Flask(__name__)

@app.template_filter('nl2br')
def nl2br(value):
    return value.replace('\n', '<br>\n')

def parse_comments(comments_str):
    if comments_str:
        comments = [comment.strip() for comment in comments_str.split('\n  —') if comment.strip()]
        if comments and comments[0].startswith('—'):
            comments[0] = comments[0][1:].strip()
        return comments
    return []

def clean_title(date, title):
    date_pattern = re.escape(date) + r'\s*-\s*'
    cleaned_title = re.sub(f'^{date_pattern}', '', title).strip()
    return cleaned_title

def load_entries():
    with open('journalEntries_with_emotions.json', 'r') as f:
        entries = json.load(f)
    
    for entry in entries:
        entry['comments'] = parse_comments(entry['comments'])
        entry['title'] = clean_title(entry['date'], entry['title'])
        for emotion in ['score', 'anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']:
            entry[emotion] = round(entry[emotion], 2)
    
    return sorted(entries, key=lambda x: datetime.strptime(x['date'], '%B %d, %Y'), reverse=True)

def get_top_entries_by_emotion(entries, emotion, limit=20):
    sorted_entries = sorted(entries, key=lambda x: x[emotion], reverse=True)
    return sorted_entries[:limit]

def get_entries_on_this_day(entries):
    today = date.today()
    on_this_day = [
        entry for entry in entries
        if datetime.strptime(entry['date'], '%B %d, %Y').date().replace(year=today.year) == today
    ]
    return on_this_day

@app.route('/')
def index():
    entries = load_entries()
    emotion = request.args.get('emotion', 'anger')
    top_entries = get_top_entries_by_emotion(entries, emotion)
    emotions = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
    on_this_day_entries = get_entries_on_this_day(entries)
    return render_template('index.html', entries=entries, top_entries=top_entries, emotions=emotions, selected_emotion=emotion, on_this_day_entries=on_this_day_entries)

@app.route('/entry/<int:entry_id>')
def entry(entry_id):
    entries = load_entries()
    if 0 <= entry_id < len(entries):
        return render_template('entry.html', entry=entries[entry_id])
    return "Entry not found", 404

@app.route('/network')
def network():
    entries = load_entries()
    graph_builder = NetworkGraphBuilder()
    relationships = graph_builder.extract_relationships(entries)
    network_data = graph_builder.create_network_data(relationships)
    return render_template('network.html', network_data=network_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # or any other available port
