.PHONY: build run stop

build:
	podman build -t postgres . --no-cache


run:
	podman run --name postgres -p 5432:5432 -d postgres


stop:
	podman stop postgres
