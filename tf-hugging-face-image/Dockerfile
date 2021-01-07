ARG TF_VERSION=2-4
FROM gcr.io/deeplearning-platform-release/tf2-gpu.$TF_VERSION
#ARG MODELS_BRANCH=r2.4.0
ARG MODELS_BRANCH=master
WORKDIR /source
RUN curl -O  https://storage.googleapis.com/kpt-dev/latest/linux_amd64/kpt \
&& chmod +x kpt \
&& mv kpt /usr/local/bin
RUN git clone https://github.com/huggingface/transformers.git \
&& cd transformers \
&& pip install -e

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["echo Hugging Face development image"]