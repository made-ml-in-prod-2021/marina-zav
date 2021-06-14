docker build -t online_inference:v1 .

docker run -p 8000:8000 online_inference:v1
