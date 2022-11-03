import asyncio
import io
import os

from fastapi import FastAPI, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from pdfprepper import processing

app = FastAPI()


@app.post("/processpdf", response_class=StreamingResponse)
def process_pdf(
    pdf: UploadFile,
    impose: bool = Form(False),
    toa4: bool = Form(False),
    toimg: bool = Form(False),
    downgrade: bool = Form(False),
):
    resultname = f"{os.path.splitext(pdf.filename)[0]}_printready.pdf"
    result = processing.process_pdf(
        io.BytesIO(asyncio.run(pdf.read())),
        impose,
        toa4,
        toimg,
        downgrade,
    )
    return StreamingResponse(
        result,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'filename="{resultname}"',
        },
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
