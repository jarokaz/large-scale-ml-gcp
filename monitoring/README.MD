# GPU Monitoring Guide

## Dashboard commands

1. Create dashboard from Cloud Monitoring UI
2. Get Dashboard ID from the URL
3. Use the describe command to get the etag, and add the etag to the dashboard.json
4. Update the dashboard

```
DASHBOARD_ID=abc123
```

**Describe dashboard**
```
gcloud monitoring dashboards describe $DASHBOARD_ID 
```

**Update dashboard**
```
gcloud monitoring dashboards update $DASHBOARD_ID --config-from-file=dashboard.json
```

## Running and building the image

**Build**
```
export IMAGE_NAME=monitoring_image
docker build -t $IMAGE_NAME ./monitoring
```

**Run**
```
docker run --rm --gpus all monitoring_image
```

