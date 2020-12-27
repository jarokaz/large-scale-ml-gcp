# Fine-tuning Sentece Classification with BERT on GCP A2 nodes

## Overview

* TF 2.4 Enterprise is used for all the samples
* Terraform is used to provision the training environment
* The code samples leverage the models from TF model garden

## Setting up the environment

### Create a training container image

```
cat > Dockerfile << EOF
FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-4
RUN apt-get install -y google-cloud-sdk-kpt
EOF
```

```
PROJECT_ID=jk-mlops-dev
IMAGE_NAME=gcr.io/$PROJECT_ID/tf24-bert-dev
docker build -t $IMAGE_NAME .
docker push
``` 

### Install `kpt`

```
sudo apt-get install google-cloud-sdk-kpt
kpt version
```

### Get SOTA NLP models from the model garden

```
SRC_REPO=https://github.com/tensorflow/models
kpt pkg get $SRC_REPO/nlp@v2.4.0 sota-nlp-models
```



### Install dependencies

```
export PYTHONPATH=$PYTHONPATH:/path/to/models
```

```

```