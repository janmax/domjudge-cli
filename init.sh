#!/usr/bin/bash

for task in `seq -w 1 12`; do
    mkdir -p $task/{bin,input}
    for letter in {A..F}; do cp default $task/$letter.cpp; done
    ln Makefile $task/Makefile
    touch $task/input/{A..F}.in
done
