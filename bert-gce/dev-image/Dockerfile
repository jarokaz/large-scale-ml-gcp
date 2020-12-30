ARG TF_VERSION=2-4
FROM gcr.io/deeplearning-platform-release/tf2-cpu.$TF_VERSION
ARG MODELS_BRANCH=r2.4.0
WORKDIR /source
RUN curl -O  https://storage.googleapis.com/kpt-dev/latest/linux_amd64/kpt \
&& chmod +x kpt \
&& mv kpt /usr/local/bin
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN git clone -b $MODELS_BRANCH  --single-branch https://github.com/tensorflow/models.git 

ENV PYTHONPATH="/source/models:${PYTHONPATH}"

ENTRYPOINT ["python"]