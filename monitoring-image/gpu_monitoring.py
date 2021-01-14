from google.cloud import monitoring_v3
from pynvml import *
from pynvml.smi import nvidia_smi
import time
import os

# Docker run -e PROJECT_ID=abc -e var2=asd

project_id = os.environ['PROJECT_ID']
interval_seconds = os.environ['INTERVAL_SECONDS']

print("Project ID: %s" % project_id)

# Don't think we'll need credentials since the GKE cluster service
# account would already have access to cloud monitoring
# cred = monitoring_v3.Client(credentials=credentials)
# Authenticate to gcloud project
# Specify a service account

scheduler = sched.scheduler(time.time, time.sleep)
client = monitoring_v3.MetricServiceClient()

def getGPUStats():
    nvsmi = nvidia_smi.getInstance()
    print(nvsmi.DeviceQuery('memory.free, memory.total, utilization.gpu'))

def main():
    print("Starting monitoring service...")

    nvmlInit()
    print ("Driver Version:", nvmlSystemGetDriverVersion())
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print ("Device", i, ":", nvmlDeviceGetName(handle))

    while True:
        getGPUStats()
        time.sleep(interval_seconds)

    


main()
