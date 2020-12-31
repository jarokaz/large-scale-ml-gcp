# Fine-tuning Sentece Classification with BERT on GCP A2 nodes

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
IMAGE_NAME=gcr.io/$PROJECT_ID/model-garden-tf24
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME
``` 

## Run MRPC experiment

### Prepare MRPC data

```
docker run -it --rm --gpus all \
--env GLUE_DIR=gs://jk-solution-assets/datasets/glue_data \
--env BERT_DIR=gs://cloud-tpu-checkpoints/bert/keras_bert/uncased_L-24_H-1024_A-16 \
--env TASK_NAME=MRPC \
--env OUTPUT_DIR=gs://labs-workspace/bert-dev/data \
gcr.io/jk-mlops-dev/model-garden-tf24 \
'python models/official/nlp/data/create_finetuning_data.py \
 --input_data_dir=${GLUE_DIR}/${TASK_NAME}/ \
 --vocab_file=${BERT_DIR}/vocab.txt \
 --train_data_output_path=${OUTPUT_DIR}/${TASK_NAME}/${TASK_NAME}_train.tf_record \
 --eval_data_output_path=${OUTPUT_DIR}/${TASK_NAME}/${TASK_NAME}_eval.tf_record \
 --meta_data_file_path=${OUTPUT_DIR}/${TASK_NAME}/${TASK_NAME}_meta_data \
 --fine_tuning_task_type=classification --max_seq_length=128 \
 --classification_task_name=${TASK_NAME}'
```

## Parking lot
### Configure VS Code

Update the `devcontainer.json` with your image.



### Get SOTA NLP models from the model garden

```
SRC_REPO=https://github.com/tensorflow/models
kpt pkg get $SRC_REPO/official/nlp@v2.4.0 sota-nlp-models
```



### Install dependencies

```
export PYTHONPATH=$PYTHONPATH:/path/to/models
```

