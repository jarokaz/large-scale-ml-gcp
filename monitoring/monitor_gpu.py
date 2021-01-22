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

from opencensus.ext.stackdriver import stats_exporter
from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view
from opencensus import tags

from pynvml import smi


FLAGS = flags.FLAGS

flags.DEFINE_integer('sampling_interval', 5, 'Sampling interval for collecting metrics - seconds', 
                     lower_bound=1)
flags.DEFINE_integer('reporting_interval', 30, 'Reporting interval to Cloud Monitoring - seconds', 
                     lower_bound=10)
flags.DEFINE_string('project_id', None, 'GCP Project ID')
flags.mark_flag_as_required('project_id')


def get_gpu_metrics():
    """
    Retrieves GPU and GPU memory utilization for all attached devices.
    """

    nvsmi = smi.nvidia_smi.getInstance()
    utilization_info = nvsmi.DeviceQuery(
        [smi.NVSMI_UTILIZATION_GPU, smi.NVSMI_UTILIZATION_MEM])
    return [device['utilization'] for device in utilization_info['gpu']]


def main(argv):
    del argv

    # Define OpenCensus measures
    gpu_utilization_ms = measure.MeasureInt(
        'gpu_utilization',
        'GPU utilization',
        '%'
    )
    gpu_memory_utilization_ms = measure.MeasureInt(
        'gpu_memory_utilization',
        'GPU memory utilization',
        '%'
    )
    
    # Define OpenCensus views
    key_device = tags.tag_key.TagKey("device")
    
    gpu_utilization_view = view.View(
        'gce/gpu/utilization_distribution',
        'The distribution of gpu utilization',
        [key_device],
        gpu_utilization_ms,
        aggregation.DistributionAggregation(
            [10, 20, 30, 40, 50, 60, 70, 80, 90]
        )
    )
    gpu_memory_utilization_view = view.View(
        'gce/gpu/memory_utilization_distribution',
        'The distribution of gpu memory utilization',
        [key_device],
        gpu_memory_utilization_ms,
        aggregation.DistributionAggregation(
            [10, 20, 30, 40, 50, 60, 70, 80, 90]
        )
    )
    stats.stats.view_manager.register_view(gpu_utilization_view)
    stats.stats.view_manager.register_view(gpu_memory_utilization_view)
    
    # Create Cloud Monitoring stats exporter
    exporter_options = stats_exporter.Options(project_id=FLAGS.project_id,
                                              default_monitoring_labels={})
    exporter = stats_exporter.new_stats_exporter(options=exporter_options,
                                                 interval=FLAGS.reporting_interval)
    
    # Register exporter to the view manager.
    stats.stats.view_manager.register_exporter(exporter)
    
    logging.info(f'Entering monitoring loop with sampling interval: {FLAGS.sampling_interval}s')

    
    tmap = tags.tag_map.TagMap()
    tmap.insert(key_device, tags.tag_value.TagValue("0"))
    while True:
        metrics = get_gpu_metrics()
        for device_index in range(len(metrics)):
            mmap = stats.stats.stats_recorder.new_measurement_map()
            mmap.measure_int_put(gpu_utilization_ms, metrics[device_index]['gpu_util'])
            mmap.measure_int_put(gpu_memory_utilization_ms, metrics[device_index]['memory_util'])
            tmap.update(key_device, tags.tag_value.TagValue(str(device_index)))
            mmap.record(tmap)
            
        time.sleep(FLAGS.sampling_interval)

if __name__ == '__main__':
    app.run(main)