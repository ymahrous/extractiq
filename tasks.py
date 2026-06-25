import time
from sqlmodel import Session, select
from database import engine
from models import Document, Extraction
from celery_app import celery_app
import storage_client
import requests # We'll use this to download the image from Supabase

@celery_app.task
def process_document_task(document_id: str):
    """
    This function runs in a completely separate process/server.
    It does NOT have access to FastAPI's request/response cycle.
    """
    print(f"Celery received job for document: {document_id}")
    
    with Session(engine) as session:
        # 1. Get document from DB
        document = session.get(Document, document_id)
        if not document:
            return {"error": "Document not found"}
        
        try:
            # 2. Update status to PROCESSING
            document.status = "PROCESSING"
            session.add(document)
            session.commit()

            # 3. SIMULATE ML PROCESSING
            # In Week 3, we will replace this with HuggingFace/Groq API calls
            time.sleep(5) 
            
            # 4. Create fake extracted data
            fake_data = {
                "vendor": "Simulated Corp",
                "total_amount": "$1,234.56",
                "date": "2023-10-27"
            }

            # 5. Save the extraction results to the DB
            extraction = Extraction(
                document_id=document_id,
                extracted_data=fake_data,
                confidence_score=0.92
            )
            session.add(extraction)
            
            # 6. Mark document as COMPLETED
            document.status = "COMPLETED"
            session.add(document)
            session.commit()

            print(f"Successfully processed document: {document_id}")
            return {"status": "success", "document_id": document_id}

        except Exception as e:
            # If anything fails, mark as FAILED so the UI knows
            document.status = "FAILED"
            session.add(document)
            session.commit()
            print(f"failed to process document: {e}")
            return {"status": "failed", "error": str(e)}