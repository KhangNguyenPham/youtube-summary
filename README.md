docker build -t youtube-summary .
docker run -d -p 8000:8000 --name youtube-summary-container -v "$(pwd)":/app youtube-summary
