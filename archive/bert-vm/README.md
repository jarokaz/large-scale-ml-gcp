# BERT pre-training on Google Compute Engine

More assets to come, see shell scripts for running jobs and creating the infrastructure.

## Configuration 1: Single Node Training (TF 2.4, Py 3.7)

**VM Spec**
* 64 core N1
* 8 V100's
* Marketplace Deep Learning VM
    * Debian 9
    * CUDA 11
    * Tensorflow Enterprise 2.3

**VM Setup**
* SSH into your newly created instance
* [Install miniconda for linux](https://docs.conda.io/en/latest/miniconda.html)
* ```conda create -n tf24 python=3.7```
* ```conda activate tf24```
* ```pip install tensorflow==2.4.0rc4``` - This to [resolve the multiheadattention Keras error](https://github.com/tensorflow/models/issues/9357) when running pretraining
* ```pip install tf-models-official```
* We are now ready to start preparing training assets and running the training algorithms


**Running BERT**
1. Set up a VM
1. Prepare assets for training.  I suggest creating a bucket in Google Cloud Storage once you have your assets together, and as you use different services you can pull all your assets through the ```gsutil cp gs://bucketname``` command.
    1. Download [TF Model Garden](https://github.com/tensorflow/models)
    1. In official/nlp/data run the create_pretraining_data.py script.  You'll need an input directory, output directory, and a vocab file.  I used the vocab file in [wwm_uncased_L-24_H-1024_A-16](https://storage.googleapis.com/cloud-tpu-checkpoints/bert/keras_bert/wwm_uncased_L-24_H-1024_A-16.tar.gz).  Also ensure that your sequence length matches what you will be using when you run the pretraining algorithm later.
1. With the tfrecords created, we can now run pretraining.  Ensure that you have your environment setup with TF 2.4 & the model garden official release.  Running ```nvidia-smi``` to ensure your VM is setup with GPUs and the relevant libraries during this step ensure that everything is setup correctly.  You should see your GPUs and a CUDA version 11 or greater.
1. Run the pretraining script located in bert-run-training.sh.  Required flags include the input (tfrecords we created), batch size, gpu count, and the config file.  I used the config from the uncases assets we downloaded earlier: [wwm_uncased_L-24_H-1024_A-16](https://storage.googleapis.com/cloud-tpu-checkpoints/bert/keras_bert/wwm_uncased_L-24_H-1024_A-16.tar.gz).
1.  TODO - finetuning the training process, batch size, distribution strategy, saving and analyzing Tensorboard logs to improve this process.



