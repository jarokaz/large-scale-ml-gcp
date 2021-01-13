# Monitoring Image Guide

## Documentation

### Python libs used
* [NVML - for monitoring GPU](https://pypi.org/project/pynvml/)
* [GCP monitoring - sending stats to the GCP api](https://googleapis.dev/python/monitoring/latest/index.html)


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



