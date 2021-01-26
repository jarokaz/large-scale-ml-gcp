ARG TORCH_VERSION=1-7
FROM gcr.io/deeplearning-platform-release/pytorch-gpu.$TORCH_VERSION
ARG HF_DATASETS_BRANCH=master
ARG HF_TRANSFORMERS_BRANCH=master
WORKDIR /source

RUN curl -O  https://storage.googleapis.com/kpt-dev/latest/linux_amd64/kpt \
&& chmod +x kpt \
&& mv kpt /usr/local/bin

RUN git clone -b $HF_TRANSFORMERS_BRANCH https://github.com/huggingface/transformers.git \
&& cd transformers \
&& pip install -e .

RUN git clone -b $HF_DATASETS_BRANCH https://github.com/huggingface/datasets.git \
&& cd datasets \
&& pip install -e .

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["echo Hugging Face development image"]