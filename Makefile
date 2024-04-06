build:
	docker build -t dimplesingh11/jenkins_termination_project:v1 .
run:
	docker run -dp 9090:9090 dimplesingh11/jenkins_termination_project:v1
