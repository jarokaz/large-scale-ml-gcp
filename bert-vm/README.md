# BERT pre-training on Google Compute Engine

More assets to come, see shell scripts for running jobs and creating the infrastructure.

## Configuration 1 Single Node Training (TF 2.4, Py 3.7)

**VM Spec**
* 64 core N1
* 8 V100's
* Marketplace DLVM TFE 2.3 

**VM Workflow**
* Install conda
* Conda create -n tf24 python=3.7
* Conda activate tf24
* pip install tensorflow==2.4.0rc4 - apparently you need this for * multiheadattention now in Keras
* pip install tf-models-official
* Run pretraining code

