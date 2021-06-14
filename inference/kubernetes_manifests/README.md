
//kubectl installed
//google cloud kit installed
gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project helical-clock-316811 --verbosity=debug
kubectl cluster-info
cd inference
kubectl apply -f kubernetes_manifests/online-inference-pod.yaml
kubectl port-forward pod/fastapi-ml 8000:8000
///
docker build -t marinazav/online_inference:v2 .
docker run -p 8000:8000 marinazav/online_inference:v2
docker push marinazav/online_inference:v2
///
kubectl apply -f kubernetes_manifests/online-inference-pod-probes.yaml