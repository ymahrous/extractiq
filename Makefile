.PHONY: help install run worker test clean

help:
    @echo "ExtractAPI Backend Commands:"
    @echo "---------------------------"
    @echo "make install   - Install all Python dependencies"
    @echo "make run       - Start the FastAPI web server"
    @echo "make worker    - Start the Celery background worker"
    @echo "make test      - Run tests (placeholder)"
    @echo "make clean     - Remove Python cache and compiled files"

install:
    pip install -r requirements.txt

run:
    uvicorn main:app --reload

worker:
    celery -A celery_app.celery_app worker --loglevel=info

test:
    pytest

clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +