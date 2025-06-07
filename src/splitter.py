import re

abbreviations = {
    'Mr', 'Mrs', 'Ms', 'Dr', 'Dra', 'Prof', 'Sra', 'Sr', 'Jr', 'vs', 'etc', 'Inc', 'Corp',
    'Ltd', 'Co', 'St', 'Ave', 'Rd', 'Blvd', 'Apt', 'No', 'Vol', 'Ph', 'B.A', 'M.A', 'Ph.D',
    'M.D', 'B.S', 'M.S', 'U.S', 'U.K', 'U.N', 'E.U', 'FBI', 'CIA', 'NASA', 'NATO', 'CEO',
    'CFO', 'CTO', 'VP', 'SVP', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep',
    'Oct', 'Nov', 'Dec', 'S.T.A.R.S'
}

ABBR_PLACEHOLDER = '<<<ABBR>>>'
NUM_PLACEHOLDER = '<<<NUM>>>'

def split_text_safe(text):
    # Protege abreviações (case-insensitive)
    abbrev_pattern = r'\b(?:' + '|'.join(re.escape(abbr) for abbr in sorted(abbreviations, key=len, reverse=True)) + r')\.'
    text = re.sub(abbrev_pattern, lambda m: m.group(0).replace('.', ABBR_PLACEHOLDER), text, flags=re.IGNORECASE)

    # Protege números como "1. " ou "01. " seguidos de letra maiúscula
    text = re.sub(r'\b\d+\.(?=\s+[A-Z])', lambda m: m.group(0).replace('.', NUM_PLACEHOLDER), text)
    
    # Divide por pontuação de fim de frase ou nova linha, mas preserva informação sobre newlines
    parts = []
    segments = re.split(r'((?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])(?=\n)|(?<=\n))', text)
    
    for i, segment in enumerate(segments):
        if segment.strip():
            # Check if this segment was preceded by a newline split
            preceded_by_newline = i > 0 and '\n' in segments[i-1]
            restored_text = segment.replace(ABBR_PLACEHOLDER, '.').replace(NUM_PLACEHOLDER, '.').strip()
            parts.append((restored_text, preceded_by_newline))
    
    return parts

def split_text_advanced(text, target_chunk_size=5, max_chunk_size=7):
    if not text.strip():
        return []

    sentence_data = split_text_safe(text)  # Now returns (text, preceded_by_newline) tuples
    chunks = []

    for sentence_text, preceded_by_newline in sentence_data:
        words = sentence_text.split()
        if len(words) <= max_chunk_size:
            chunks.append((sentence_text, preceded_by_newline))
            continue

        chunk = []

        current = []
        for i, word in enumerate(words):
            current.append(word)
            if (len(current) >= max_chunk_size or
                (len(current) >= target_chunk_size and (
                    word.endswith(',') or
                    (i + 1 < len(words) and words[i + 1].lower() in {
                        'and', 'or', 'but', 'yet', 'so', 'for', 'nor',
                        'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from',
                        'the', 'a', 'an', 'this', 'that', 'these', 'those'
                    }))
                ) or i == len(words) - 1):
                chunk_text = ' '.join(current).strip()
                if chunk_text:
                    # Only the first chunk from a sentence keeps the newline flag
                    is_first_chunk = len(chunk) == 0
                    chunk.append((chunk_text, preceded_by_newline if is_first_chunk else False))
                current = []

        chunks.extend(chunk)

    return join_little_chunks(chunks)

def join_little_chunks(chunks):
    result = []
    for i, (chunk_text, preceded_by_newline) in enumerate(chunks):
        # Only join if chunk is small AND was not preceded by newline
        if i > 0 and len(chunk_text.split()) <= 2 and not preceded_by_newline:
            # Get the previous result text and update it
            prev_text = result[-1]
            result[-1] = prev_text + ' ' + chunk_text
        else:
            result.append(chunk_text)
    return result