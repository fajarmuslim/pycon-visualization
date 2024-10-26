import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from text import df, text_from_df

def count_label(df:pd.DataFrame, label:str):
    st.write(f"**{label.capitalize()} Distribution Histogram**")
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, y=f"{label}", palette='viridis')

    plt.title(f"Distribution of {label}", fontsize=12)
    plt.xlabel("Label", fontsize=8)
    plt.ylabel("Count", fontsize=8)
    st.pyplot(plt)

def wordcloud(text:str):    
    st.write("**WordCloud Generator**")

    max_words = int(0.1*len(text.split()))
    wordcloud = WordCloud(width=800, height=400, max_words=max_words, background_color="white").generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def word_frequency(text:str, k:int =10):
    st.write(f"**Word Frequency Chart for the top {k} words**")

    word_counts = Counter(text.split())
    top_words = word_counts.most_common(k)

    # Extract words and their counts
    words, counts = zip(*top_words)

    plt.figure(figsize=(8, 6))
    sns.barplot(x=list(counts), y=list(words), palette='viridis')
    plt.title(f"Top {k} word frequency", fontsize=8)
    plt.xlabel("Words", fontsize=8)
    plt.ylabel("Frequency", fontsize=8)

    st.pyplot(plt)

def data_sample(df:pd.DataFrame, k:int=10):
    st.write(f"**Recent Top {k} Text Data**")
    st.write(df.head(k))


col1, col2 = st.columns(2)
with col1:
    count_label(df=df, label='sentiment')
with col2:
    count_label(df=df, label='emotion')

word_frequency(text=text_from_df, k=10)
wordcloud(text=text_from_df)
data_sample(df=df, k=10)
