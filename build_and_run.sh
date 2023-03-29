docker build -t 'wapp:latest' .
docker run -d --rm -p 80:8080 --name wapp_container wapp
