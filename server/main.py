#!/usr/bin/env python3

import asyncio

from tempfile import NamedTemporaryFile

from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from processing import impose_pdf

app = FastAPI()


@app.post("/processpdf", response_class=StreamingResponse)
def process_pdf(pdf: UploadFile):
    with NamedTemporaryFile() as source:
        source.write(asyncio.run(pdf.read()))
        result = impose_pdf(source.name)
    return StreamingResponse(result, media_type="application/pdf")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
