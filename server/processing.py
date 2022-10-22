from io import BytesIO

from pdfimpose.schema import saddle


def impose_pdf(source_pdf: str) -> BytesIO:
    "Impose a pdf in a booklet format."
    imposed = BytesIO()
    saddle.impose([source_pdf], imposed, folds="h")
    imposed.seek(0)
    return imposed
