
import spacy

nlp = spacy.load("en_core_web_sm")

def split_text_advanced(text, min_chunk_size=3, target_chunk_size=5, max_chunk_size=8):
    """
    Advanced version with better phrase boundary detection.
    """
    import re
    
    text = text.strip()
    if not text:
        return []
    
    # Split into sentences first
    sentences = re.split(r'[.!?]+', text)
    all_chunks = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        words = sentence.split()
        if len(words) <= max_chunk_size:
            # If sentence is short enough, keep it as one chunk
            all_chunks.append(sentence)
            continue
        
        # Split longer sentences
        chunks = []
        current_chunk = []
        
        for i, word in enumerate(words):
            current_chunk.append(word)
            
            should_break = False
            
            # Force break at max size
            if len(current_chunk) >= max_chunk_size:
                should_break = True
            
            # Look for natural breaks after reaching target size
            elif len(current_chunk) >= target_chunk_size:
                # Break after commas
                if word.endswith(','):
                    should_break = True
                
                # Break before conjunctions and prepositions
                elif i + 1 < len(words):
                    next_word = words[i + 1].lower()
                    break_words = [
                        'and', 'or', 'but', 'yet', 'so', 'for', 'nor',  # conjunctions
                        'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from',  # prepositions
                        'the', 'a', 'an', 'this', 'that', 'these', 'those'  # articles
                    ]
                    if next_word in break_words:
                        should_break = True
            
            if should_break or i == len(words) - 1:
                chunk_text = ' '.join(current_chunk).strip()
                if chunk_text:
                    chunks.append(chunk_text)
                current_chunk = []
        
        all_chunks.extend(chunks)
    
    return all_chunks

def split_sentences(text):
    sentences = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        doc = nlp(line)
        sentences.extend([sent.text.strip() for sent in doc.sents])
    return sentences
