#!/usr/bin/env python3

import asyncio
import io

from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from processing import convert_to_images, downgrade_version, impose_pdf

app = FastAPI()


@app.post("/processpdf", response_class=StreamingResponse)
def process_pdf(pdf: UploadFile):
    result = io.BytesIO(asyncio.run(pdf.read()))
    result = impose_pdf(result)
    result = convert_to_images(result)
    result = downgrade_version(result)
    return StreamingResponse(result, media_type="application/pdf")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
