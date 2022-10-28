#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo "Usage: "$0" [path_to_pdf_dir (default: current directory)]

This script batch-process pdf files to prepare them for impression.
It expects to be given a directory containing one or more of the following subfolders:
- originals_onepage, containing unprocessed pdfs in a non-booklet format
- booklet, containing pdfs already in the booklet format

It will create a printready folder (if not already existing), with the resulting processed pdfs.
"
    exit
fi

FILESDIR="${1-}"

if [[ "$FILESDIR" == "" ]]; then
   FILESDIR="$PWD"
fi

FILESDIR=$(readlink -m "$FILESDIR")

# Ensure all subfolder exist

DIR_ORIGINALS="${FILESDIR}/originals_onepage"
DIR_BOOKLET="${FILESDIR}/booklet"
DIR_PRINTREADY="${FILESDIR}/printready"

if [ ! -d "$DIR_ORIGINALS" ]; then
    mkdir "$DIR_ORIGINALS"
fi

if [ ! -d "$DIR_BOOKLET" ]; then
    mkdir "$DIR_BOOKLET"
fi

if [ ! -d "$DIR_PRINTREADY" ]; then
    mkdir "$DIR_PRINTREADY"
fi

# Start conversion service

echo -n "Starting conversion service... "

CONTAINERNAME="pdfprepper_${RANDOM}"

docker run -d --rm \
    --volume="$DIR_ORIGINALS":/originals_onepage \
    --volume="$DIR_BOOKLET":/booklet \
    --volume="$DIR_PRINTREADY":/printready \
    --name="$CONTAINERNAME" \
    pdfprepper 1> /dev/null

echo "DONE"

# Do convertions

echo -n "Converting original pdf files to booklet... "

COMMAND_STAGE1='cd /;
for pdffile in /originals_onepage/*.pdf; do
    filename=$(basename "$pdffile")
    [ -e "$pdffile" ] || continue
    python3 -m pdfprepper --impose --out "/booklet/$filename" --impose --no-toimg --no-downgrade "$pdffile"
done'
docker exec "$CONTAINERNAME" bash -c "$COMMAND_STAGE1"

echo "DONE"

echo -n "Preparing booklet pdf files for printing... "

COMMAND_STAGE2='cd /;
for pdffile in /booklet/*.pdf; do
    filename=$(basename "$pdffile")
    [ -e "$pdffile" ] || continue
    python3 -m pdfprepper --impose --out "/printready/$filename" --no-impose --toimg --downgrade "$pdffile"
done'
docker exec "$CONTAINERNAME" bash -c "$COMMAND_STAGE2"

echo "DONE"

# We are done

docker stop "$CONTAINERNAME" 1> /dev/null

echo "Finished! print-ready pdf files in $DIR_PRINTREADY"
