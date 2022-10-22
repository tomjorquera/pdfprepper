import os
import subprocess
import tempfile
from io import BytesIO

from pdfimpose.schema import saddle


def process_pdf(
    source_pdf: BytesIO,
    impose: bool = True,
    toimg: bool = True,
    downgrade: bool = True,
) -> BytesIO:
    result = source_pdf
    if impose:
        result = impose_pdf(result)
    if toimg:
        result = convert_to_images(result)
    if downgrade:
        result = downgrade_version(result)
    return result


def impose_pdf(source_pdf: BytesIO) -> BytesIO:
    "Impose a pdf in a booklet format."
    imposed = BytesIO()
    with tempfile.NamedTemporaryFile() as source:
        source.write(source_pdf.read())
        saddle.impose([source.name], imposed, folds="h")
    imposed.seek(0)
    return imposed


def convert_to_images(source_pdf: BytesIO, ppi="300") -> BytesIO:
    "Convert content of pdf to images."
    res = BytesIO()
    with (
        tempfile.NamedTemporaryFile() as source_file,
        tempfile.TemporaryDirectory() as tmp_dir,
    ):
        result_file_name = f"{source_file.name}_converted.pdf"
        source_file.write(source_pdf.read())
        source_file.flush()
        subprocess.check_output(
            ["pdftoppm", source_file.name, "out", "-png", "-r", ppi], cwd=tmp_dir
        )
        subprocess.check_output(["convert", "out-*", result_file_name], cwd=tmp_dir)

        with open(result_file_name, "rb") as result_file:
            res.write(result_file.read())
        os.remove(result_file_name)

    res.seek(0)
    return res


def downgrade_version(source_pdf: BytesIO, target_version="1.2") -> BytesIO:
    "Downgrade pdf version to target."
    res = BytesIO()
    with (tempfile.NamedTemporaryFile() as source_file,):
        result_file_name = f"{source_file.name}_converted.pdf"
        source_file.write(source_pdf.read())
        source_file.flush()
        subprocess.check_output(
            [
                "gs",
                "-q",
                "-sDEVICE=pdfwrite",
                f"-dCompatibilityLevel={target_version}",
                "-o",
                result_file_name,
                source_file.name,
            ]
        )

        with open(result_file_name, "rb") as result_file:
            res.write(result_file.read())
        os.remove(result_file_name)

    res.seek(0)
    return res
