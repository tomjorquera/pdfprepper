FROM debian:trixie-slim

RUN apt-get update && \
    apt-get install -y \
            ghostscript \
            python3 \
            python3-pip \
            python3-venv \
            poppler-utils \
            imagemagick \
            texlive-extra-utils \
    && \
    apt-get clean

# Need to adjust ghostscript security policy to enable pdf version conversion
RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-7/policy.xml

ADD requirements.txt /requirements.txt

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN  pip install -r /requirements.txt

ADD pdfprepper /pdfprepper/
ADD static /static/

EXPOSE 80

CMD ["uvicorn", "pdfprepper.serve:app", "--host", "0.0.0.0", "--port", "80"]
