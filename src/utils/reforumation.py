from openai import OpenAI
import os 
import sys 
sys.path.append(r"C:\Users\o\agentflightbooking\fiancialAIAgent")


deepseek_client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/v1"
)

def reformuler_question_en_requete_usa(question, client):
    prompt = f"""
You are a legal research assistant for U.S. law.

Your job is to turn a user's natural language question into a focused Google search query
that finds relevant legal documents in PDF format on official U.S. government websites.
and as output give me just the query without explanations

Instructions:
- Use only the key legal terms (state, topic, law name if known).
- End the query with: site:.gov filetype:pdf
- Be concise and relevant.
- give just one query 

Example:
Question: What is the law about privacy rights in California?
Query: california privacy law site:.gov filetype:pdf

---

User question:
\"{question}\"

Google search query:
"""

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
