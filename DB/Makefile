.PHONY: build run stop restart

build:
	podman build -t postgres . --no-cache


run:
	podman run --name postgres -p 5432:5432 -d postgres


stop:
	podman stop postgres
	podman rm postgres

restart:
	podman stop postgres
	podman rm postgres
	podman build -t postgres . --no-cache
	podman run --name postgres -p 5432:5432 -d postgres
