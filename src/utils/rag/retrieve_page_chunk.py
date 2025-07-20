def trouver_page_du_chunk(chunk, ocr_texts):
    for i, page_text in enumerate(ocr_texts):
        if chunk.strip()[:50] in page_text:
            return i + 1  
    return None
