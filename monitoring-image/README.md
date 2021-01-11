# Monitoring Image Guide

## Documentation

### Python libs used
* [NVML - for monitoring GPU](https://pypi.org/project/pynvml/)
* [GCP monitoring - sending stats to the GCP api](https://googleapis.dev/python/monitoring/latest/index.html)


### Create a training container image

```
cd dev-image
```

```
PROJECT_ID=kz-2021-267823
IMAGE_NAME=us.gcr.io/$PROJECT_ID/gpu-monitoring
docker build -t $IMAGE_NAME ./monitoring-image
docker push $IMAGE_NAME
```

### run
```
docker run $
```


