FROM debian:bullseye-slim
MAINTAINER Tom Jorquera <tom@jorquera.net>

RUN apt-get update && \
    apt-get install -y \
            ghostscript \
            python3 \
            python3-pip \
            poppler-utils \
            imagemagick \
    && \
    apt-get clean

# Need to adjust ghostscript security policy to enable pdf version conversion
RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml

ADD requirements.txt /pdfbaf/requirements.txt
ADD server /pdfbaf/server

WORKDIR /pdfbaf

RUN pip install -r requirements.txt

WORKDIR /pdfbaf/server

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]