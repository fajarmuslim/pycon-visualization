import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from utils.label import select_df

# Sample DataFrame with 'text' column (replace this with your actual DataFrame)
from text import df

# Vectorize the text using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])

# KMeans Clustering
num_clusters = st.slider("Select number of clusters", 2, 5, 3)
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(tfidf_matrix)
df['cluster'] = kmeans.labels_

# Dimensionality Reduction using t-SNE
tsne = TSNE(n_components=2, random_state=42)
tsne_results = tsne.fit_transform(tfidf_matrix.toarray())

# Add t-SNE results to DataFrame
df['tsne_x'] = tsne_results[:, 0]
df['tsne_y'] = tsne_results[:, 1]

# Plot t-SNE Clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x='tsne_x', y='tsne_y', hue='cluster', data=df, palette='viridis', s=100)
plt.title('t-SNE Visualization of Document Clusters', fontsize=16)
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
st.pyplot(plt)

st.write(df[['text', 'cluster', 'tsne_x', 'tsne_y']])
