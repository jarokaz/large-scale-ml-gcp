# Fine-tuning Sentence Classification with BERT on GCP A2 nodes

## Overview

* TF 2.4 Enterprise is used for all the samples
* Terraform is used to provision the training environment
* The code samples leverage the models from TF model garden

## Setting up the environment

### Create a training container image

```
cd dev-image
```

```
PROJECT_ID=jk-mlops-dev
IMAGE_NAME=gcr.io/$PROJECT_ID/hugging-face-torch17
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME
```

## Run Sentence Prediction experiment

### Run MNLI fine-tuning

```
docker run -it --rm --gpus device=0 \
--env TASK_NAME=MNLI \
--env OUTPUT_DIR=gs://jk-bert-lab-bucket/hgf \
gcr.io/jk-mlops-dev/hugging-face-torch17 \
'python transformers/examples/text-classification/run_glue.py \
  --model_name_or_path bert-base-cased \
  --task_name $TASK_NAME \
  --do_train \
  --do_eval \
  --max_seq_length 128 \
  --per_device_train_batch_size 32 \
  --learning_rate 2e-5 \
  --num_train_epochs 3 \
  --output_dir $OUTPUT_DIR/$TASK_NAME/'

```




