import re
import spacy as nlp

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

    
def process_tweet(text):
    
    """
    This function cleans and tokenizes each tweet.
    
    It does the following:
        1. removes emojis
        2. removes URLs
        3. removes newlines
        4. removes stopwords
        5. removes punctuation
    """
    
    # string edits
    text = deEmojify(text)
    text = re.sub(r"http\S+", "", text)
    text = text.replace('\n', '')
    text = re.sub(r'\d+', '', text)
    text = re.sub('\s+', ' ', text).strip()
    text = "".join([char for char in text if char.isalpha() or char==' '])
    
    # token edits
    all_stopwords = nlp.Defaults.stop_words
    all_stopwords |= {'rt','abd'}
    doc = nlp(text)
    doc = [token.lemma_.lower() for token in doc if token.lemma_!='-PRON-' and token.lemma_ not in all_stopwords]
    return doc

