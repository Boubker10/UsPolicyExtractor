import os
import sys
import json
import logging
from typing import List, Dict, Any, Optional
import traceback
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.utils.reforumation import deepseek_client, reformuler_question_en_requete_usa
from src.utils.websearch import chercher_pdfs_via_serpapi
from src.utils.download_pdf import telecharger_pdf_dossier_temp
from src.utils.ocr import ocr
from src.utils.get_final_response import ai_agent_analyze_ocr
from src.utils.rag.semantic_chunking import semantic_chunking, model
from src.utils.rag.retrieve_page_chunk import trouver_page_du_chunk
from src.utils.rag.retrive_top_k_chunks import retrieve_top_k_chunks


class ReformulateQuestion(BaseEstimator, TransformerMixin):
    def __init__(self, client, question):
        self.client = client
        self.question = question

    def fit(self, X=None, y=None): return self

    def transform(self, X=None):
        query = reformuler_question_en_requete_usa(self.question, self.client)
        logger.info(f"[ReformulateQuestion] Reformulated query: {query}")
        return query


class SearchPDFs(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self

    def transform(self, query):
        urls = chercher_pdfs_via_serpapi(query)
        logger.info(f"[SearchPDFs] Found URLs: {urls}")
        if not urls:
            raise ValueError("No PDF URL found.")
        return urls[0]


class DownloadPDF(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self

    def transform(self, pdf_url):
        path = telecharger_pdf_dossier_temp(pdf_url)
        logger.info(f"[DownloadPDF] PDF downloaded at: {path}")
        return path


class OCRExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self

    def transform(self, pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        ocr_texts = ocr(pdf_bytes)
        logger.info(f"[OCRExtractor] Extracted OCR text from {len(ocr_texts)} pages.")
        return ocr_texts


class AIAgentAnswer(BaseEstimator, TransformerMixin):
    def __init__(self, client, question):
        self.client = client
        self.question = question

    def fit(self, X, y=None): return self

    def transform(self, ocr_texts):
        answer = ai_agent_analyze_ocr(ocr_texts, self.question, self.client)
        logger.info(f"[AIAgentAnswer] AI answer: {answer}")
        return {"ocr": ocr_texts, "ai_answer": answer}


class RAGRetriever(BaseEstimator, TransformerMixin):
    def __init__(self, model, question):
        self.model = model
        self.question = question

    def fit(self, X, y=None): return self

    def transform(self, data):
        ocr_texts = data["ocr"]
        full_text = " ".join(ocr_texts)
        chunks = semantic_chunking(full_text, self.model)
        chunk_embeddings = self.model.encode(chunks, normalize_embeddings=True)
        question_embedding = self.model.encode([self.question], normalize_embeddings=True)
        top_chunks = retrieve_top_k_chunks(question_embedding, chunks, chunk_embeddings, k=1)

        if top_chunks:
            chunk, _, _ = top_chunks[0]
            page = trouver_page_du_chunk(chunk, ocr_texts)
        else:
            chunk, page = "No relevant chunk found", None

        logger.info(f"[RAGRetriever] Top chunk: {chunk}")
        logger.info(f"[RAGRetriever] Found on page: {page}")

        return {
            "ai_answer": data["ai_answer"],
            "top_chunk": chunk,
            "page": page
        }


def build_pipeline(question: str):
    return make_pipeline(
        ReformulateQuestion(client=deepseek_client, question=question),
        SearchPDFs(),
        DownloadPDF(),
        OCRExtractor(),
        AIAgentAnswer(client=deepseek_client, question=question),
        RAGRetriever(model=model, question=question)
    )
