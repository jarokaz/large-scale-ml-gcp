export BERT_BASE_DIR=/home/kyleziegler_google_com/bert-assets/wwm_uncased_L-24_H-1024_A-16
export GLUE_DIR=/home/kyleziegler_google_com/bert-assets/glue_data
export PYTHONPATH=$PYTHONPATH:/home/kyleziegler_google_com/bert-assets/models

export PYTHONPATH=$PYTHONPATH:/home/kyleziegler_google_com/.local/lib/python3.7/

# Create dataset
python models/official/nlp/data/create_pretraining_data.py \
  --input_file=/home/kyleziegler_google_com/bert-assets/input/input.txt \
  --output_file=/home/kyleziegler_google_com/bert-assets/output/tf_examples.tfrecord \
  --vocab_file=/home/kyleziegler_google_com/bert-assets/wwm_uncased_L-24_H-1024_A-16/vocab.txt \
  --do_lower_case=True \
  --max_seq_length=512 \
  --max_predictions_per_seq=76 \
  --masked_lm_prob=0.15 \
  --random_seed=12345 \
  --dupe_factor=5

  # Note that args are different for TF garden vs Google research

# NOTE: Max_seq_length in the training must match the value you used
# when creating the dataset in create_pretraining_data.py

# Run pretraining, TF Garden repo
python models/official/nlp/bert/run_pretraining.py \
  --input_files=/home/kyleziegler_google_com/bert-assets/output/tf_examples.tfrecord \
  --train_batch_size=8 \
  --max_seq_length=512 \
  --max_predictions_per_seq=76 \
  --warmup_steps=5 \
  --learning_rate=2e-5 \
  --num_gpus=4 \
  --bert_config_file=/home/kyleziegler_google_com/bert-assets/wwm_uncased_L-24_H-1024_A-16/bert_config.json



# Run pretraining, Google Research repo
python models/official/nlp/bert/run_pretraining.py \
  --input_file=/home/kyleziegler_google_com/output/tf_examples.tfrecord \
  --output_dir=/home/kyleziegler_google_com/output/ \
  --do_train=True \
  --do_eval=True \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --train_batch_size=32 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=20 \
  --num_warmup_steps=10 \
  --learning_rate=2e-5

python run_classifier.py \
  --task_name=MRPC \
  --do_train=true \
  --do_eval=true \
  --data_dir=$GLUE_DIR/MRPC \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=/tmp/mrpc_output/

  python official/nlp/bert/run_pretraining.py \
  --input_file=/tmp/tf_examples.tfrecord \
  --output_dir=/tmp/pretraining_output \
  --do_train=True \
  --do_eval=True \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --train_batch_size=32 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=20 \
  --num_warmup_steps=10 \
  --learning_rate=2e-5