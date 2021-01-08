ARG TF_VERSION=2-4
FROM gcr.io/deeplearning-platform-release/tf2-gpu.$TF_VERSION
#ARG MODELS_BRANCH=r2.4.0
ARG MODELS_BRANCH=master
WORKDIR /source
RUN curl -O  https://storage.googleapis.com/kpt-dev/latest/linux_amd64/kpt \
&& chmod +x kpt \
&& mv kpt /usr/local/bin
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN git clone -b $MODELS_BRANCH  --single-branch https://github.com/tensorflow/models.git 


ENTRYPOINT ["/bin/bash", "-c"]
#ENTRYPOINT ["python"]
CMD ["echo TensorFlow TF 2.4 Enterprise development image"]
#CMD ["-c", 'print("TensorFlow TF 2.4 Enterprise development image")']