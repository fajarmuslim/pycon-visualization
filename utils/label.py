import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from text import df
from typing import Union

def format_text(metric:Union[int, float], percentage:bool):
    if percentage:
        return f"{int(round(100*(metric/len(df['text']))))}%"
    else:
        return metric
    
def show_scorecard(label:str, percentage:bool):
    text_count = len(df["text"].dropna())

    arr_col = st.columns(len(df[label].value_counts())+1)

    with arr_col[0]:
        st.metric(label="total", value=format_text(metric=text_count, percentage=percentage))

    idx = 1
    for label, count in df[label].value_counts().items():
        with arr_col[idx]:
            st.metric(label=label, value=format_text(metric=count, percentage=percentage))
        idx += 1

def select_df(df:pd.DataFrame, label:str):
    filter = st.selectbox(label=f"**Filter Data by {label.capitalize()}**", options=['All'] + list(df[label].unique()))

    if filter != 'All':
        filtered_df = df[df[label] == filter]
    else:
        filtered_df = df

    st.write(filtered_df)

def chart_overtime(label:str):
    # Ensure 'updated_at' is in datetime format
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    # Extract the date and time (minute-level granularity) from 'updated_at'
    df['rounded_updated_at'] = df['updated_at'].dt.floor('T')  # Grouping by minute ('T' stands for minute)

    # Count occurrences of each label at each date and time (grouped by minute)
    df_counts = df.groupby(['rounded_updated_at', label]).size().reset_index(name='count')

    # Create a line chart with Plotly
    fig = go.Figure()

    # Loop through each unique emotion label
    for label_ in df[label].unique():
        # Filter the DataFrame for each label category
        df_filtered = df_counts[df_counts[label] == label_]

        # Add a trace for each label with its count over time
        fig.add_trace(go.Scatter(x=df_filtered['rounded_updated_at'], 
                                y=df_filtered['count'],  # Plot the count of emotions on the y-axis
                                mode='lines+markers', 
                                name=label_,  # Use the actual emotion label dynamically
                                hoverinfo='text',  # Tooltip configuration
                                text=[f"Date-Time: {time}<br>{label_.capitalize()} Count: {count}"
                                    for time, count in zip(df_filtered['rounded_updated_at'], df_filtered['count'])]))

    # Add titles and axis labels
    fig.update_layout(
        title=f"{label.capitalize()} Trends Over Time (By Date and Minute)",
        xaxis_title="Date and Time (Minute-Level)",
        yaxis_title=f"{label.capitalize()} Count",
        hovermode="x unified"  # Unifies the tooltip when hovering over the x-axis
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)



