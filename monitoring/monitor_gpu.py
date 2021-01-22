# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A command line utility that monitors attached GPUs and 
reports the stats to Cloud Monitoring"""

import time

from absl import app
from absl import flags
from absl import logging

from pynvml import smi

GPU_UTILIZATION_METRIC_NAME = 'gce/gpu/utilization'
GPU_MEMORY_UTILIZATION_METRIC_NAME = 'gce/gpu/memory_utilization'

FLAGS = flags.FLAGS

flags.DEFINE_integer('interval', 10, 'Sampling interval for collecting metrics', 
                     lower_bound=10)


def get_gpu_metrics():
    """
    Retrieves GPU and GPU memory utilization for all attached devices.
    """

    nvsmi = smi.nvidia_smi.getInstance()
    utilization_info = nvsmi.DeviceQuery(
        [smi.NVSMI_UTILIZATION_GPU, smi.NVSMI_UTILIZATION_MEM])
    return [device['utilization'] for device in utilization_info['gpu']]


def report_gpu_metric(value, type, instance_id, zone, project_id):
    series = monitoring_v3.types.TimeSeries()
    series.metric.type = 'custom.googleapis.com/{type}'.format(type=type)
    series.resource.type = 'gce_instance'
    series.resource.labels['instance_id'] = instance_id
    series.resource.labels['zone'] = zone
    series.resource.labels['project_id'] = project_id
    point = series.points.add()
    point.value.int64_value = value
    now = time.time()
    point.interval.end_time.seconds = int(now)
    point.interval.end_time.nanos = int(
        (now - point.interval.end_time.seconds) * 10**9)
    client.create_time_series(project_name, [series])

def main(argv):
    del argv

    logging.info(f'Entering monitoring loop with sampling interval: {FLAGS.interval}s')

    while True:
        print("Reporting metrics")
        metrics = get_gpu_metrics()
        for device_index in range(len(metrics)):
            print(f'GPU:{device_index}, Utilization:', metrics[device_index]['gpu_util'])
        time.sleep(FLAGS.interval)

if __name__ == '__main__':
    app.run(main)