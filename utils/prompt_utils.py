def build_prompt(context_docs, user_query):
    context = "\n".join([f"- {doc}" for doc, _ in context_docs])
    return f"""You are a helpful assistant. Use the following tweets as context to answer the question.

Context:
{context}

Question: {user_query}
Answer:"""
