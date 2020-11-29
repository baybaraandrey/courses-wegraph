SHELL := /bin/bash

run:
	go run app/courses-api/main.go

tidy:
	go mod tidy
	go mod vendor

deps-cleancache:
	go clean -modcache
