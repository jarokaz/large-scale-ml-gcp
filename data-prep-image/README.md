# Data Prep Image Guide

## Documentation



### Create and push container image

```
PROJECT_ID=kz-2021-267823
IMAGE_NAME=us.gcr.io/$PROJECT_ID/data-prep
docker build -t $IMAGE_NAME ./data-prep
docker push $IMAGE_NAME
```

### Run


t - TTY
i - interactive, keep stdin open
rm - remove container from node when finished running
```
docker run -it --rm \
--env PROJECT_ID=kz-2021-267823 \
us.gcr.io/$PROJECT_ID/data-prep
```

### References

* [DL images reference](https://cloud.google.com/ai-platform/deep-learning-containers/docs/choosing-container)



