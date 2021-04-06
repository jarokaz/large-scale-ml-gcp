# BERT Fine Tuning Assets

1. Install TF models nightly or official
2. Copy tf model git repo
3. Download GLUE datasets - see script in glue folder
4. Run the script to create fine tuning data - pay attention to the task you want to use 

To create assets run:
```
export GLUE_DIR=./glue/glue_data
export BERT_DIR=gs://cloud-tpu-checkpoints/bert/keras_bert/uncased_L-24_H-1024_A-16

export TASK_NAME=COLA
export OUTPUT_DIR=gs://bert-assets/fine-tuning-data
python ~/models/official/nlp/data/create_finetuning_data.py \
 --input_data_dir=${GLUE_DIR}/${TASK_NAME}/ \
 --vocab_file=${BERT_DIR}/vocab.txt \
 --train_data_output_path=${OUTPUT_DIR}/${TASK_NAME}_train.tf_record \
 --eval_data_output_path=${OUTPUT_DIR}/${TASK_NAME}_eval.tf_record \
 --meta_data_file_path=${OUTPUT_DIR}/${TASK_NAME}_meta_data \
 --fine_tuning_task_type=classification --max_seq_length=128 \
 --classification_task_name=${TASK_NAME}
```