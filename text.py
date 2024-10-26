import nltk
import random
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from datetime import datetime, timedelta
from db import merged_df

nltk.download('stopwords')

def remove_stopwords(text):
    indonesian_stopwords = set(stopwords.words('indonesian'))
    indonesian_stopwords.add('nya')

    words = text.split()
    cleaned_text = ' '.join([word for word in words if word.lower() not in indonesian_stopwords])
    
    return cleaned_text

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

# def random_timestamp(start, end):
#     return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# df = pd.read_csv('/Users/fajarmuslim/Documents/works/pycon/indonlu/dataset/smsa_doc-sentiment-prosa/train_preprocess.tsv', sep='\t', header=None)
# df = df.rename({0: 'text', 1: 'sentiment'}, axis=1)
# emotion = ['love', 'fear', 'anger', 'happy', 'sadness']
# df['emotion'] = np.random.choice(emotion, size=len(df))

df = merged_df

df['text'] = df['text'].apply(remove_punctuation)
df['text'] = df['text'].apply(remove_stopwords)
# df['text'] = df['text'].apply(lambda x: x.split())

documents = df['text']

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)

# df['timestamp'] = [random_timestamp(start_date, end_date) for _ in range(len(df))]
# df = df.sort_values(by='timestamp', ascending=False).reset_index(drop=True)

text_from_df = ' '.join(df['text'])
