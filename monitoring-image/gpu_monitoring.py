from google.cloud import monitoring_v3
from pynvml import *
from pynvml.smi import nvidia_smi
import time
import os
import socket




def getGPUStats(project_id):
    nvsmi = nvidia_smi.getInstance()
    print(nvsmi.DeviceQuery('memory.free, memory.total, utilization.gpu, stats'))
    # Returns a dictionary
    # gpu, list of gpus, dict of k/v you get from the gpus
    statsDict = nvsmi.DeviceQuery('memory.free, memory.total, utilization.gpu, stats')

    # TODO
    # Average all the gpus, or send each one to cloud monitoring?
    print(statsDict["gpu"][0]["utilization"])
    print(statsDict["gpu"][0]["utilization"]["gpu_util"])
    # Write metrics to cloud monitoring

    client = monitoring_v3.MetricServiceClient()
    machine_identifier = socket.gethostname()
    gpu_util = statsDict["gpu"][0]["utilization"]["gpu_util"]
    
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/gpu/utilization"
    series.resource.type = "gce_instance"
    series.resource.labels["instance_id"] = machine_identifier
    series.resource.labels["zone"] = "us-west1-b"
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point = monitoring_v3.Point({"interval": interval, "value": {"double_value": gpu_util}})
    series.points = [point]
    client.create_time_series(request={"name": project_name, "time_series": [series]})
    print("Successfully wrote time series.")

# Custom metric naming: custom.googleapis.com/instance/cpu/utilization
def createMonitoringMetrics(project_id):
    
    client = monitoring_v3.MetricServiceClient()
    machine_identifier = socket.gethostname()
    print(machine_identifier)
    
    project_name = f"projects/{project_id}"
    
    descriptor = ga_metric.MetricDescriptor()
    descriptor.type = f"custom.googleapis.com/{machine_identifier}/gpu/utilization" + str(uuid.uuid4())
    descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = "GPU Utilization, as a percentage."
    descriptor = client.create_metric_descriptor(
        name=project_name, metric_descriptor=descriptor
    )
    print("Created {}.".format(descriptor.name))

def main():
    print("Starting monitoring service...")

    try:
        project_id = os.environ['PROJECT_ID']
        interval_seconds = os.environ['INTERVAL_SECONDS']
    except ValueError:
        print("INTERVAL_SECONDS must be numeric.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        
    print("Project ID: %s" % project_id)
    print("Metric interval: %s seconds" % interval_seconds)
    
#     createMonitoringMetrics(project_id)
  
    # Print basic GPU info
    nvmlInit()
    print ("Driver Version:", nvmlSystemGetDriverVersion())
    deviceCount = nvmlDeviceGetCount()
    
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print ("Device", i, ":", nvmlDeviceGetName(handle))

    while True:
        getGPUStats(project_id)
        time.sleep(int(interval_seconds))

main()
