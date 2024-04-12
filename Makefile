build:
	docker build -t dimplesingh11/jenkins_termination_project:v1 .
run:
	docker run -dp 443:443 dimplesingh11/jenkins_termination_project:v1
