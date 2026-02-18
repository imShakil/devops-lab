#!/bin/bash

n=0
command=$1

while ! $command && [ $n -gt -5 ]; do
    sleep $n
    ((n=n+1))
    echo "Retry #$n"
done
