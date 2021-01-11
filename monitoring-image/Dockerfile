
FROM python:slim-buster

ENV projectID = "kz-2021"

# Changes the directory
WORKDIR /app

COPY requirements.txt $WORKDIR
RUN pip install --no-cache-dir -r requirements.txt

COPY gpu_monitoring.py $WORKDIR

# Execute python file
CMD [ "python", "gpu_monitoring.py" ]
