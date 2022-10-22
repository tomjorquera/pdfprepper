#!/usr/bin/env python3

import asyncio
import io

from fastapi import FastAPI, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from processing import convert_to_images, downgrade_version, impose_pdf

app = FastAPI()


@app.post("/processpdf", response_class=StreamingResponse)
def process_pdf(
    pdf: UploadFile,
    impose: bool = Form(False),
    toimg: bool = Form(False),
    downgrade: bool = Form(False),
):
    result = io.BytesIO(asyncio.run(pdf.read()))
    if impose:
        result = impose_pdf(result)
    if toimg:
        result = convert_to_images(result)
    if downgrade:
        result = downgrade_version(result)
    return StreamingResponse(result, media_type="application/pdf")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
