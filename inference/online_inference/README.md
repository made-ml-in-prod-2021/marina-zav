docker build -t marinazav/online_inference:v1 .

docker run -p 8000:8000 marinazav/online_inference:v1

docker push marinazav/online_inference:v1