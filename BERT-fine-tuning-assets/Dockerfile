
FROM python:3.7-slim

# Changes the directory
WORKDIR /app

COPY requirements.txt $WORKDIR
RUN pip install --no-cache-dir -r requirements.txt

COPY data-prep.py $WORKDIR

# Execute python file
CMD [ "python", "data-prep.py" ]
