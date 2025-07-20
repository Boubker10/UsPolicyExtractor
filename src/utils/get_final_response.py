from openai import OpenAI
import os 
import json 
import sys 
import requests

def ai_agent_analyze_ocr(ocr_texts, question,client):

    full_text = "\n\n".join(ocr_texts)
    
    prompt = f"""
You are a legal assistant helping to analyze PDF documents extracted by OCR.

User question: {question}

Below is the extracted text from the PDF document (from OCR):

{full_text}

Please provide a clear and concise answer to the user's question based on the content of the document.
"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )
    
    answer = response.choices[0].message.content.strip()
    return answer