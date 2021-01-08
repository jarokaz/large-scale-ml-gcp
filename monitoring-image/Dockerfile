
# FROM alpine:latest

# WORKDIR /apps


# ENTRYPOINT ["/bin/bash", "-c"]
# CMD ["echo executing "]



FROM python:3

# Changes the directory
WORKDIR /app

COPY requirements.txt $WORKDIR
RUN pip install --no-cache-dir -r requirements.txt

COPY gpu_monitoring.py $WORKDIR

# Execute python file
CMD [ "python", "gpu_monitoring.py" ]
