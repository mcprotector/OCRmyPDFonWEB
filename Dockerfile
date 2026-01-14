FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-deu \
        tesseract-ocr-eng \
        tesseract-ocr-fra \
        tesseract-ocr-spa \
        tesseract-ocr-ita \
        tesseract-ocr-rus \
        tesseract-ocr-pol \
        tesseract-ocr-nld \
        ghostscript \
        pngquant \
        unpaper \
        qpdf \
        libleptonica-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "server.py"]