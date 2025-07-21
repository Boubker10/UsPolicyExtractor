FROM public.ecr.aws/lambda/python:3.10

RUN yum -y install \
    tesseract \
    poppler-utils \
    ghostscript \
    libSM \
    libXext \
    libXrender \
    && yum clean all

WORKDIR /var/task

COPY . .

RUN pip install --upgrade pip && pip install --no-cache-dir \
    pytesseract \
    pdf2image \
    sentence-transformers \
    scikit-learn \
    numpy \
    openai \
    Pillow \
    PyPDF2 \
    requests \
    python-dotenv

CMD ["src.lambda_handler.lambda_handler"]
