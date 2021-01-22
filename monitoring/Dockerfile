FROM python:slim-buster
WORKDIR /source
COPY monitor_gpu.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "monitor_gpu.py"]
