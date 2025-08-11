import ftfy
import re
import unicodedata

def normalize_punctuation(text):
    # Fix common unicode issues
    text = ftfy.fix_text(text)
    # Normalize Unicode form (e.g. é as single codepoint)
    text = unicodedata.normalize("NFC", text)
    # Replace German quotes with "
    text = text.replace("„", '"').replace("“", '"').replace("‚", "'").replace("‘", "'")
    # Replace ellipsis with three dots
    text = text.replace("…", "...")
    # Normalize dashes
    text = text.replace("–", "-").replace("—", "-")
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_empty_pair(src, tgt):
    return len(src.strip()) == 0 or len(tgt.strip()) == 0


def is_misaligned(src, tgt, max_len=100, length_ratio=3.0):
    src_tokens = src.split()
    tgt_tokens = tgt.split()
    
    # Too long sequences
    if len(src_tokens) > max_len or len(tgt_tokens) > max_len:
        return True
    
    # Length mismatch
    if len(src_tokens) == 0 or len(tgt_tokens) == 0:
        return True
    ratio = max(len(src_tokens) / len(tgt_tokens),
                len(tgt_tokens) / len(src_tokens))
    if ratio > length_ratio:
        return True
    
    return False
