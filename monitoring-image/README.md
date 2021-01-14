# Monitoring Image Guide

## Documentation

### Library Documentation - Nvidia GPUs
* [NVML - for monitoring GPU](https://pypi.org/project/pynvml/)
* [GCP monitoring - sending stats to the GCP api](https://googleapis.dev/python/monitoring/latest/index.html)
* [Nvidia Developer - SMI PDF](http://developer.download.nvidia.com/compute/DCGM/docs/nvidia-smi-367.38.pdf)
* [NVML reference guide](https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html#group__nvmlDeviceQueries_1g540824faa6cef45500e0d1dc2f50b321)

### Google Cloud Docs
* (GCP Cloud Monitoring - Custom Metrics)[https://cloud.google.com/monitoring/custom-metrics/creating-metrics]

### Create and push container image

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


t - TTY
i - interactive, keep stdin open
rm - remove container from node when finished running
```
docker run -it --rm \
--env PROJECT_ID=kz-2021-267823 \
us.gcr.io/$PROJECT_ID/gpu-monitoring
```

### Troubleshooting

Pushing images to GCR
* docker-credential-gcr is not in system PATH: (stackoverflow fix)[https://stackoverflow.com/questions/49780218/docker-credential-gcloud-not-in-system-path]
* Ensure that authentication is set up correctly, (follow these steps)[https://cloud.google.com/artifact-registry/docs/docker/authentication]



