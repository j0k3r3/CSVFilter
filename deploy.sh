echo "Starting CSVFilter container"
docker build . -t csvfilter
docker run --rm -d -p 5001:8000 csvfilter