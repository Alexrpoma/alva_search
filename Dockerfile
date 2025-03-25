FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
#RUN pip install --upgrade pip \
#     && pip install qdrant-client \
#     && pip install torch \
#     && pip install sentence-transformers \
#     && pip install "fastapi[standard]"
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]