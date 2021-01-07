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

## Run Sentence Prediction experiment

### Prepare MNLI dataset

docker run -it --rm --gpus all \
--env GLUE_DIR=gs://jk-solution-assets/datasets/glue_data \
--env BERT_DIR=gs://cloud-tpu-checkpoints/bert/keras_bert/uncased_L-24_H-1024_A-16 \
--env TASK_NAME=MNLI \
--env OUTPUT_DIR=gs://jk-bert-lab-bucket/data \
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

### Run MNLI fine tuning

```
docker run -it --rm --gpus all \
--env OUTPUT_DIR=gs://jk-bert-lab-bucket \
--env TASK=MNLI \
--env PARAMS=\
task.train_data.input_path=gs://jk-bert-lab-bucket/data/MNLI/MNLI_train.tf_record,\
task.validation_data.input_path=gs://jk-bert-lab-bucket/data/MNLI/MNLI_eval.tf_record,\
task.init_checkpoint=gs://cloud-tpu-checkpoints/bert/keras_bert/uncased_L-24_H-1024_A-16,\
runtime.distribution_strategy=mirrored,\
runtime.num_gpus=2 \
gcr.io/jk-mlops-dev/model-garden-tf24 \
'python3 models/official/nlp/train.py \
 --experiment=bert/sentence_prediction \
 --mode=train_and_eval \
 --model_dir=$OUTPUT_DIR/models/$TASK \
 --config_file=models/official/nlp/configs/experiments/glue_mnli_matched.yaml \
 --params_override=$PARAMS'
 ```


## Run MRPC experiment

### Prepare MRPC data

```
docker run -it --rm --gpus all \
--env GLUE_DIR=gs://jk-solution-assets/datasets/glue_data \
--env BERT_DIR=gs://cloud-tpu-checkpoints/bert/keras_bert/uncased_L-24_H-1024_A-16 \
--env TASK_NAME=MRPC \
--env OUTPUT_DIR=gs://jk-bert-lab-bucket/data \
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
### RUN MRPC fine-tuning

### RUN MRPC fine-tuning - legacy
```
docker run -it --rm --gpus all \
--env GLUE_DIR=gs://labs-workspace/bert-dev/data/MRPC \
--env BERT_DIR=gs://cloud-tpu-checkpoints/bert/keras_bert/uncased_L-24_H-1024_A-16 \
--env TASK=MRPC \
--env MODEL_DIR=gs://labs-workspace/bert-dev/models/mrpc/model_dir \
gcr.io/jk-mlops-dev/model-garden-tf24 \
'python models/official/nlp/bert/run_classifier.py \
  --mode='train_and_eval' \
  --input_meta_data_path=${GLUE_DIR}/${TASK}_meta_data \
  --train_data_path=${GLUE_DIR}/${TASK}_train.tf_record \
  --eval_data_path=${GLUE_DIR}/${TASK}_eval.tf_record \
  --bert_config_file=${BERT_DIR}/bert_config.json \
  --init_checkpoint=${BERT_DIR}/bert_model.ckpt \
  --train_batch_size=4 \
  --eval_batch_size=4 \
  --steps_per_loop=1 \
  --learning_rate=2e-5 \
  --num_train_epochs=3 \
  --model_dir=${MODEL_DIR} \
  --distribution_strategy=mirrored \
  --num_gpus=2'
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

