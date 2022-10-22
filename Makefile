.PHONY: testrequest
testrequest:
	curl -X 'POST' 'http://127.0.0.1:8000/processpdf' \
		-H 'accept: */*' \
		-H 'Content-Type: multipart/form-data' \
		--output 'result.pdf' \
		-F 'pdf=@template.pdf;type=application/pdf'

.PHONY: devserve
devserve:
	cd server && \
	uvicorn main:app --reload

.PHONY: dockerserve
dockerserve: dockerbuild
	docker run -it -p 8000:80 --rm pdfprepper

.PHONY: dockerbuild
dockerbuild:
	docker build -t pdfprepper .
