
all:		build

TARGET = csc558spring2020assn4

include ./makelib

clean:		subclean

build:
			echo "This makefile is for 'make turnitin' of project 4 data files only."
			bash -c "exit 1"

test:
