from google.cloud import monitoring_v3
from pynvml import *

cred = monitoring_v3.Client(credentials=credentials)
# Authenticate to gcloud project
# Specify a service account
# Maybe pass in the credentials to the docker run command? 


def main():
    print("Hello world")
    client = monitoring_v3.MetricServiceClient()

    # Send metrics every X seconds as specified

main()
