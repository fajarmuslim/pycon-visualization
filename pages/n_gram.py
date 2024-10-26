import streamlit as st
import pandas as pd
from nltk import ngrams
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from text import df

# Download NLTK resources
nltk.download('punkt')

# Function to generate N-grams
def generate_ngrams(text, n):
    tokens = nltk.word_tokenize(text)
    return list(ngrams(tokens, n))

# Function to get most common N-grams
def get_most_common_ngrams(text_series, n, top_n=10):
    all_ngrams = []
    for text in text_series:
        all_ngrams.extend(generate_ngrams(text, n))
    ngram_counts = Counter(all_ngrams)
    return ngram_counts.most_common(top_n)

# Title of the app
st.title("N-gram Analysis Dashboard")

# Select N-gram type
n = st.selectbox("Select N-gram type:", [1, 2, 3], format_func=lambda x: f"{x}-grams")

# Get the most common N-grams
most_common_ngrams = get_most_common_ngrams(df['text'], n)

# Create DataFrame for plotting
ngram_df = pd.DataFrame(most_common_ngrams, columns=['N-gram', 'Count'])
ngram_df['N-gram'] = ngram_df['N-gram'].apply(lambda x: ' '.join(x))

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x='Count', y='N-gram', data=ngram_df, palette='viridis')
plt.title(f'Most Common {n}-grams', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel(f'{n}-gram', fontsize=12)

# Display the plot in Streamlit
st.pyplot(plt)

