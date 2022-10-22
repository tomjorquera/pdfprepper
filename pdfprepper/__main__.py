#!/usr/bin/env python3

import argparse
import io
import os

from pdfprepper.processing import process_pdf


def main():
    """Main entrypoint for command line execution"""
    parser = argparse.ArgumentParser(description="Prepare PDF file for impression.")
    parser.add_argument("source_pdf", type=str, help="the PDF file to convert.")
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="output file path. (default: <source_pdf>_printready.pdf)",
    )
    parser.add_argument(
        "--impose",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Perform booklet imposition.",
    )
    parser.add_argument(
        "--toimg",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Convert content to images.",
    )
    parser.add_argument(
        "--downgrade",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Downgrade PDF version to 1.2.",
    )

    args = parser.parse_args()

    out_path = args.out
    if out_path is None:
        out_path = f"{os.path.splitext(args.source_pdf)[0]}_printready.pdf"

    source = io.BytesIO()
    with open(args.source_pdf, "rb") as source_file:
        source.write(source_file.read())
    source.seek(0)

    result = process_pdf(source, args.impose, args.toimg, args.downgrade)
    with open(out_path, "wb") as result_file:
        result_file.write(result.read())


main()
