FROM debian:bullseye-slim
MAINTAINER Tom Jorquera <tom@jorquera.net>

RUN apt-get update && \
    apt-get install -y \
            python3 \
            python3-pip \
            poppler-utils \
            imagemagick \
    && \
    apt-get clean

ADD requirements.txt /pdfbaf/requirements.txt
ADD server /pdfbaf/server

WORKDIR /pdfbaf

RUN pip install -r requirements.txt

WORKDIR /pdfbaf/server

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
