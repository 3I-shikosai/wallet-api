.PHONY: run setup top

run:
	poetry run gunicorn app.main:app \
		--workers 8 \
		--bind 0.0.0.0:8080 \
		--access-logfile - \
		--capture-output \
		--worker-class uvicorn.workers.UvicornWorker

setup:
	poetry install
	make -C ./DB build
	make -C ./DB run


stop:
	make -C ./DB stop
