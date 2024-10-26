import streamlit as st
import pandas as pd
import gensim
from gensim import corpora
import pyLDAvis.gensim_models
import pyLDAvis
import matplotlib.pyplot as plt
import seaborn as sns
from text import df

documents = df['text'].apply(lambda x: x.split())

# Create a dictionary and corpus for LDA
dictionary = corpora.Dictionary(documents)
corpus = [dictionary.doc2bow(doc) for doc in documents]

# Train the LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)

# Display topics
st.write("Top words for each topic:")
for i, topic in lda_model.show_topics(formatted=False, num_words=3):
    st.write(f"Topic {i + 1}: {[word[0] for word in topic]}")

# Visualize topics using pyLDAvis
st.write("LDA Topic Visualization:")
lda_vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
html_string = pyLDAvis.prepared_data_to_html(lda_vis)
st.components.v1.html(html_string, width=1300, height=800)

# Get the topic distribution for each document
topic_distribution = []
for doc in corpus:
    topic_probabilities = lda_model.get_document_topics(doc)
    topic_distribution.append(max(topic_probabilities, key=lambda x: x[1])[0])  # Get the topic with the highest probability

# Create a DataFrame to count the number of documents for each topic
topic_counts = pd.Series(topic_distribution).value_counts().sort_index()

# Create a histogram
plt.figure(figsize=(10, 6))
sns.barplot(x=topic_counts.index, y=topic_counts.values, palette='viridis')
plt.title('Number of Documents per Topic', fontsize=16)
plt.xlabel('Topic', fontsize=12)
plt.ylabel('Number of Documents', fontsize=12)
plt.xticks(ticks=topic_counts.index, labels=[f'Topic {i}' for i in topic_counts.index])
st.pyplot(plt)