import ftfy
import re
import unicodedata
import json
import os



def normalize_punctuation(text):

    # Fix common unicode issues
    text = ftfy.fix_text(text)

    # Normalize Unicode form (e.g. é as single codepoint)
    text = unicodedata.normalize("NFC", text)

    # Replace German quotes with "
    text = text.replace("„", '"').replace("“", '"').replace("‚", "'").replace("‘", "'").replace("»", '"').replace("«", '"')

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




def preprocess(dataset):

    train = dataset['train']
    preprocessed_dataset = {}
    i = 0

    for pair in train:

        german_sentence = normalize_punctuation(pair['translation']['de'])
        english_sentence = normalize_punctuation(pair['translation']['en'])

        if is_empty_pair(german_sentence, english_sentence) or is_misaligned(german_sentence, english_sentence):
            i += 1
            continue

        translation = {'de': german_sentence, 'en': english_sentence}
        preprocessed_dataset[len(preprocessed_dataset)] = translation

    print(f'{i} pairs filtered')
    return preprocessed_dataset




def save_data(data, file_name='preprocessed_data.json'):
    data_folder = os.path.join('data')
    os.makedirs(data_folder, exist_ok=True)

    file_path = os.path.join(data_folder, file_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f'preprocessed data saved as "{file_path}"')