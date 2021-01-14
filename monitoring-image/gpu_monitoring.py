from google.cloud import monitoring_v3
from pynvml import *
from pynvml.smi import nvidia_smi
import time
import os

client = monitoring_v3.MetricServiceClient()

def getGPUStats():
    nvsmi = nvidia_smi.getInstance()
    print(nvsmi.DeviceQuery('memory.free, memory.total, utilization.gpu, stats'))
    # Returns a dictionary
    # gpu, list of gpus, dict of k/v you get from the gpus
    statsDict = nvsmi.DeviceQuery('memory.free, memory.total, utilization.gpu, stats')

    # TODO
    # Average all the gpus, or send each one to cloud monitoring?
    print(statsDict["gpu"][0]["utilization"])
    
def createMonitoringMetrics(project_id, description):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    descriptor = ga_metric.MetricDescriptor()
    descriptor.type = "custom.googleapis.com/my_metric" + str(uuid.uuid4())
    descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = description
    descriptor = client.create_metric_descriptor(
        name=project_name, metric_descriptor=descriptor
    )
    print("Created {}.".format(descriptor.name))

def main():
    print("Starting monitoring service...")

    try:
        project_id = os.environ['PROJECT_ID']
        interval_seconds = os.environ['INTERVAL_SECONDS']
        interval_seconds = os.environ['INTERVAL_SECONDS']
    except ValueError:
        print("INTERVAL_SECONDS must be numeric.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        
    print("Project ID: %s" % project_id)
    print("Metric interval: %s seconds" % interval_seconds)
    
    # Print basic GPU info
    nvmlInit()
    print ("Driver Version:", nvmlSystemGetDriverVersion())
    deviceCount = nvmlDeviceGetCount()
    
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print ("Device", i, ":", nvmlDeviceGetName(handle))

    while True:
        getGPUStats()
        time.sleep(int(interval_seconds))

main()
