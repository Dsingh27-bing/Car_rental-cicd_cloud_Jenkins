build:
	docker build -t dimplesingh11/termination_project:drivenow .
run:
	docker run -dp 9090:9090 dimplesingh11/termination_project:drivenow