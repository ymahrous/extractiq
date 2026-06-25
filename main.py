from fastapi import FastAPI, UploadFile, File, Depends
from sqlmodel import Session
import database, models
from sqlmodel import select
import storage_client
from tasks import process_document_task

app = FastAPI(title="ExtractIQ API")

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.post("/test-upload/")
def test_upload(file: UploadFile = File(...), session: Session = Depends(database.get_session)):
    # 1. Read & Upload to Supabase (This is fast, keep it in the API)
    file_bytes = file.file.read()
    filename = file.filename
    public_url = storage_client.upload_to_storage(file_bytes, filename)
    
    # 2. Save to DB as PENDING
    db_doc = models.Document(
        filename=filename,
        s3_url=public_url,
        status="PENDING"
    )
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)
    
    # 3. SEND THE TASK TO CELERY (The magic line!)
    # .delay() sends this to Upstash Redis and returns immediately
    process_document_task.delay(db_doc.id)
    
    # 4. Return to the user instantly
    return {
        "message": "Document received and sent to ML queue!",
        "document_id": db_doc.id,
        "status": db_doc.status # Will be "PENDING"
    }

@app.get("/documents/")
def get_documents(session: Session = Depends(database.get_session)):
    # We join the Extraction table so we can see the ML results alongside the docs
    docs = session.exec(
        select(models.Document).order_by(models.Document.created_at.desc())
    ).all()
    return docs