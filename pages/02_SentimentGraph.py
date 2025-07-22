import streamlit as st
from textblob import TextBlob
import pandas as pd
import altair as alt

st.title("📈 Sentiment Graph of Retrieved Tweets")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.warning("No chat history yet. Ask something on the main page first.")
else:
    sentiment_results = []

    for i, msg in enumerate(st.session_state.history):
        query = msg["query"]
        retrieved_docs = msg.get("retrieved_docs", [])
        for doc, score in retrieved_docs:
            polarity = TextBlob(doc).sentiment.polarity
            sentiment_results.append({
                "Query": query,
                "Tweet": doc,
                "SimilarityScore": score,
                "SentimentPolarity": polarity
            })

    if not sentiment_results:
        st.info("No retrieved tweets to analyze.")
    else:
        df = pd.DataFrame(sentiment_results)

        st.dataframe(df)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Tweet:N', sort=None, axis=alt.Axis(labelAngle=-45)),
            y='SentimentPolarity:Q',
            color=alt.Color('Query:N'),
            tooltip=['Tweet', 'SentimentPolarity', 'Query']
        ).properties(
            width=700,
            height=400,
            title="Sentiment Polarity of Retrieved Tweets"
        )

        st.altair_chart(chart, use_container_width=True)
