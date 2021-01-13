from google.cloud import monitoring_v3
from pynvml import *
from pynvml.smi import nvidia_smi
import time
import os

# Docker run -e PROJECT_ID=abc -e var2=asd

project_ID = os.environ['PROJECT_ID']
print(project_ID)

# Don't think we'll need credentials since the GKE cluster service
# account would already have access to cloud monitoring
# cred = monitoring_v3.Client(credentials=credentials)
# Authenticate to gcloud project
# Specify a service account



def getGPUStats():
    nvsmi = nvidia_smi.getInstance()
    nvsmi.DeviceQuery('memory.free, memory.total')

def main():
    print("Starting monitoring service...")

    nvmlInit()
    print ("Driver Version:", nvmlSystemGetDriverVersion())
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print ("Device", i, ":", nvmlDeviceGetName(handle))

    
    starttime = time.time()
    while True:
        getGPUStats()
        time.sleep(5.0 - ((time.time() - starttime) % 60.0))

    client = monitoring_v3.MetricServiceClient()


main()
