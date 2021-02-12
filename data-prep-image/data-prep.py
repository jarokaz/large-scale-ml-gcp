# Outline
# Reference a stored GLUE dataset or pull it on the fly
# Run script in model garden to build the dataset
# 
# 
# 
# 
import tensorflow as tf
import tensorflow_datasets as tfds
from official import nlp
from official.nlp import bert


glue, info = tfds.load('glue/cola', with_info=True,
                       # It's small, load the whole dataset
                       batch_size=-1)

list(glue.keys())



