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

"""A command line utility that creates custom Cloud Monitoring metrics
for tracking GPU and GPU memory utilization."""

from google.cloud import monitoring_v3

from absl import app
from absl import flags
from absl import logging

GPU_UTILIZATION_METRIC_NAME = 'gce/gpu/utilization'
GPU_UTILIZATION_METRIC_DESC = 'GPU utilization'
GPU_MEMORY_UTILIZATION_METRIC_NAME = 'gce/gpu/memory_utilization'
GPU_MEMORY_UTILIZATION_METRIC_DESC = 'GPU memory utilization'

FLAGS = flags.FLAGS

flags.DEFINE_string('project_id', None, 'GCP Project ID') 
flags.mark_flag_as_required('project_id')


GPU_UTILIZATION_METRIC_NAME = 'gce/gpu/utilization'                            
GPU_MEMORY_UTILIZATION_METRIC_NAME = 'gce/gpu/memory_utilization'

def main(argv):
    del argv
    
    client = monitoring_v3.MetricServiceClient()

    parent = 'projects/{}/metricDescriptors/custom.googleapis.com'.format(FLAGS.project_id)
    gpu_util_metric_name = '{}/{}'.format(parent, GPU_UTILIZATION_METRIC_NAME)
    gpu_memory_metric_name = '{}/{}'.format(parent, GPU_MEMORY_UTILIZATION_METRIC_NAME)

    client.delete_metric_descriptor(name=gpu_util_metric_name)
    client.delete_metric_descriptor(name=gpu_memory_metric_name)

if __name__ == '__main__':
    app.run(main)