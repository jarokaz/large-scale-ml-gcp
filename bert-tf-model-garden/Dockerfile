ARG TF_VERSION=2-4
FROM gcr.io/deeplearning-platform-release/tf2-gpu.$TF_VERSION
ARG MODELS_BRANCH=master
WORKDIR /source
RUN git clone -b $MODELS_BRANCH  --single-branch https://github.com/tensorflow/models.git 
RUN pip install -r models/official/requirements.txt
COPY train.py .
COPY profile.py profile/ 
ENV PYTHONPATH=/source/models

ENTRYPOINT ["/bin/bash", "-c"]
#ENTRYPOINT ["python"]
CMD ["echo TensorFlow TF 2.4 Enterprise development image"]
#CMD ["-c", 'print("TensorFlow TF 2.4 Enterprise development image")']
