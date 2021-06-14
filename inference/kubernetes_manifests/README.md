# ML in Production. Homework 4

## 1. Развернуть кластер Kubernetes
Сервис: https://cloud.google.com/kubernetes-engine
Убедитесь, с кластер поднялся: `kubectl cluster-info`

## 2. Простой pod manifest
Предварительно запушить docker image в Docker Hub: см `online_inference/README.md`
Deploy: `kubectl apply -f kubernetes_manifests/online-inference-pod.yaml`
В манифесте прописаны requests/limits:
`requests` - прописывается, чтобы Kubernetes определил исходя из доступных ресурсов, на какой хост поместить pod,
чтобы не деплоить приложение на хост с недостаточным кол-вом ресурсов.
А также чтобы после выключения хоста под с прописанными ресурсами гарантированно переехал на новый хост.
`limits` - пороговые максимальные значения, в случае превышения этих значений K8s начнет
ограничивать (по CPU) или перезапускать контейнер (если по RAM).

## 3. Liveness & Readiness
Deploy: `kubectl apply -f kubernetes_manifests/online-inference-pod-probes.yaml`
Если добавить 30 sec sleep при старте приложения за счет readiness настройки k8s не помечает контейнер как Ready сразу же,
пока helth-check не прошел успешно (спустя 30 сек).
liveness проба проверяет приложение периодически, пока контейнер запущен - и если возникнут какие-то проблемы,
то K8s пометит контейнер как не Ready и запросы прекратят приниматься.

## 4. Replicaset
Deploy: `kubectl apply -f kubernetes_manifests/online-inference-replicaset.yaml`
При изменении версии докер образа и увеличении кол-ва реплик - добавляются новые поды с новой версией докер образа,
при этом старые йоды продолжают работать. Но если удалить один из старых подов,
ReplicaSet дополнит подами с новой версией докер образа до сконфигурированного кол-ва реплик.
При изменении версии докер образа и уменьшении кол-ва реплик - удаляются поды до нужного кол-ва.
При этом у меня было 2 пода V2 и 4 пода  V3, и когда я изменила версию на V2 и уменьшила replicas до 3 - осталось 2 пода V2, 1 под версии V3.

## 5. Deployment strategy
Deploy: `kubectl apply -f kubernetes_manifests/online-inference-deployment-blue-green.yaml`
deployment-blue-green: Если поставить maxUnavailable=0, maxSurge=кол-ву реплик (8),
то сначала поднимутся все поды с новой версией образа, а потом остановятся старые поды.
Deploy: `kubectl apply -f kubernetes_manifests/online-inference-deployment-rolling-update.yaml`
deployment-rolling-update: к примеру выставить maxUnavailable=2, maxSurge=4 (<кол-ва реплик),
то обновление будет происходить плавно, в какой-то момент времени будут и старые и новые приложения.

-------
Полезные команды:
kubectl port-forward pod/fastapi-ml 8000:8000
kubectl get pods -o wide
kubectl get services