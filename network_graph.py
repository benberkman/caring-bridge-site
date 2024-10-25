import re
from collections import defaultdict, Counter

class NetworkGraphBuilder:
    def __init__(self):
        self.min_mentions = 2
        self.max_nodes = 40
        self.proximity_threshold = 4  # Words distance to establish a link
        
        # Add stopwords and invalid names
        self.stopwords = {
            'and', 'or', 'the', 'for', 'to', 'in', 'of', 'at', 'on', 'with',
            'by', 'from', 'up', 'about', 'into', 'over', 'after', 'but', 'who',
            'what', 'where', 'when', 'why', 'how', 'all', 'any', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'that', 'this', 'these',
            'those', 'you', 'your', 'yours', 'me', 'my', 'mine', 'his', 'her', 'hers',
            'their', 'theirs', 'its', 'our', 'ours', 'has', 'have', 'had', 'was',
            'were', 'been', 'being', 'do', 'does', 'did', 'doing', 'would', 'should',
            'could', 'might', 'must', 'shall', 'will', 'can', 'may',
            # Add common words that might be capitalized but aren't names
            'I', 'We', 'Us', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday', 'January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November', 'December',
            'American', 'French', 'English', 'German', 'Italian', 'Spanish',
            'God', 'Lord', 'Christmas', 'Easter', 'Thanksgiving', 'Paris', 'London',
            'New', 'York', 'France', 'America', 'England', 'Germany', 'Italy', 'Spain'
        }

    def is_valid_name(self, name):
        """Check if a string is likely to be a valid name."""
        name = name.strip()
        if (
            not name or
            len(name) < 2 or
            name.lower() in self.stopwords or
            name in self.stopwords or  # Check exact match too
            name.isnumeric() or
            not any(c.isalpha() for c in name) or
            all(c.islower() for c in name) or
            ' and ' in name.lower() or
            'the ' in name.lower() or
            name.endswith('ing') or
            name.endswith('ed') or
            name.endswith('ly')
        ):
            return False
        return True

    def find_names_with_positions(self, words):
        """Find potential names and their positions in word list."""
        names_with_pos = []
        name_pattern = r'^[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*$'
        
        for i, word in enumerate(words):
            if re.match(name_pattern, word):
                if self.is_valid_name(word):
                    names_with_pos.append((word, i))
        return names_with_pos

    def extract_relationships(self, entries):
        """Extract relationships between people based on word proximity."""
        relationships = defaultdict(set)
        mention_counts = Counter()
        
        for entry in entries:
            # Only look at the entry text, not comments
            text = entry['entry']
            
            # Split text into words
            words = text.split()
            
            # Find all valid names and their word positions
            names_with_pos = self.find_names_with_positions(words)
            
            # Count mentions
            for name, _ in names_with_pos:
                mention_counts[name] += 1
            
            # Link names that appear close to each other
            for i, (name1, pos1) in enumerate(names_with_pos):
                for name2, pos2 in names_with_pos[i+1:]:
                    # If names are within proximity threshold
                    if abs(pos2 - pos1) <= self.proximity_threshold:
                        if name1 != name2:  # Avoid self-loops
                            relationships[name1].add(name2)
                            relationships[name2].add(name1)

        # Filter out nodes with few mentions
        filtered_relationships = defaultdict(set)
        significant_people = {person for person, count in mention_counts.most_common(self.max_nodes)
                            if count >= self.min_mentions}
        
        # Only keep relationships between significant people
        for person1, connected_people in relationships.items():
            if person1 in significant_people:
                filtered_relationships[person1] = {
                    person2 for person2 in connected_people 
                    if person2 in significant_people
                }

        return filtered_relationships

    def create_network_data(self, relationships):
        """Convert relationships into network visualization format."""
        nodes = []
        edges = []
        seen_nodes = set()
        
        # Create nodes and edges
        for person1, connected_people in relationships.items():
            if person1 not in seen_nodes:
                nodes.append({
                    "id": person1,
                    "label": person1,
                    "group": "author" if person1 == "Willa Silverman" else "person",
                    "value": len(connected_people)  # Node size based on connections
                })
                seen_nodes.add(person1)
            
            for person2 in connected_people:
                if person2 not in seen_nodes:
                    nodes.append({
                        "id": person2,
                        "label": person2,
                        "group": "author" if person2 == "Willa Silverman" else "person",
                        "value": len(relationships[person2])  # Node size based on connections
                    })
                    seen_nodes.add(person2)
                
                edges.append({
                    "from": person1,
                    "to": person2,
                    "value": 1
                })
        
        return {
            "nodes": nodes,
            "edges": edges
        }
