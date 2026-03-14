from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.responses import StreamingResponse, FileResponse

from Parent_agent import parent_agent
import uuid
from pathlib import Path
from pydantic import BaseModel

class repo_input(BaseModel):
    job_id : str
    url : str
    owner : str
    repo_name : str
    branch : str

app=FastAPI()

@app.post('/create_folder')
async def Create_folder():
    job_id=str(uuid.uuid4())
    job_path=Path(job_id)
    job_path.mkdir(parents=True, exist_ok=True)
    
    return {'job_id': job_id}

@app.post('/github-repo')
async def Enter_Info(repo_input:repo_input):

    # To avoid the parameters being shown in url as query parameter
    # Making branch explicit as LLM tried either master or main
    message=f'Explain this repo---> url:{repo_input.url}, owner:{repo_input.owner}, repo_name:{repo_input.repo_name}, branch:{repo_input.branch}'
    job_path=Path(repo_input.job_id)
    try:
        return StreamingResponse(
            parent_agent(message=message, filename=job_path),
            media_type='text/markdown')
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )

#download the pdf file created
@app.get('/download')
async def Download_PDF(job_id:str):
    file_path=Path(job_id)
    pdf_path=file_path/'repo.pdf'
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="repo.pdf"
    )

# Websocket
@app.websocket("/query")
async def Chat(websocket:WebSocket, job_id:str)