#!/bin/bash
echo "Starting CSVFilter container"
docker build . -t csvfilter
docker run --rm -d -p 5000:5000 csvfilter