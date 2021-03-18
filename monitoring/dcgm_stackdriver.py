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
import datetime
import dcgm_fields

from absl import app
from absl import flags
from absl import logging
from google.cloud import monitoring_v3

from DcgmReader import DcgmReader

FLAGS = flags.FLAGS
FIELD_GROUP_NAME = 'dcgm_stackdriver'

# DCGM fields to SD metrics mapping
DCGM_FIELDS = {
    # Equivalents of the basic metrics in nvidia-smi
    dcgm_fields.DCGM_FI_DEV_GPU_UTIL: # 203
        {
            'name': 'custom.googleapis.com/gce/gpu/utilization',
            'desc': 'GPU utilization',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64,
            'dcgm_units': '%',
            'value_converter': (lambda x: x) 
        },
    dcgm_fields.DCGM_FI_DEV_FB_USED: # 252
        {
            'name': 'custom.googleapis.com/gce/gpu/mem_used',
            'desc': 'GPU memory used',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'MBs',
            'value_converter': (lambda x: x)
        },
    dcgm_fields.DCGM_FI_DEV_POWER_USAGE: #155
        {
            'name': 'custom.googleapis.com/gce/gpu/power_usage',
            'desc': 'Power usage',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'Watts',
            'value_converter': (lambda x: int(x))
        },
    # Profiling metrics recommended by NVidia
    dcgm_fields.DCGM_FI_PROF_GR_ENGINE_ACTIVE: # 1001
        {
            'name': 'custom.googleapis.com/gce/gpu/gr_engine_active',
            'desc': 'Ratio of time the graphics engine is active',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'ratio',
            'value_converter': (lambda x: int(100 * x))
        },
    dcgm_fields.DCGM_FI_PROF_SM_ACTIVE: # 1002 
        {
            'name': 'custom.googleapis.com/gce/gpu/sm_active',
            'desc': 'Ratio of cycles an SM has at least 1 warp assigned',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'ratio',
            'value_converter': (lambda x: int(100 * x))
        },
    dcgm_fields.DCGM_FI_PROF_SM_OCCUPANCY: # 1003
        {
            'name': 'custom.googleapis.com/gce/gpu/sm_occupancy',
            'desc': 'Ratio of number of warps resident on an SM',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'ratio',
            'value_converter': (lambda x: int(100 * x))            
        },
    dcgm_fields.DCGM_FI_PROF_DRAM_ACTIVE: # 1005
        {
            'name': 'custom.googleapis.com/gce/gpu/memory_active',
            'desc': 'Ratio of cycles the device memory inteface is active sending or receiving data',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'ratio',
            'value_converter': (lambda x: int(100 * x))
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_TENSOR_ACTIVE: # 1004 
        {
            'name': 'custom.googleapis.com/gce/gpu/tensor_active',
            'desc': 'Ratio of cycles the tensor cores are active',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64,  
            'dcgm_units': 'ratio',
            'value_converter': (lambda x: int(100 * x))
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_FP32_ACTIVE: # 1007
        {
            'name': 'custom.googleapis.com/gce/gpu/fp32_active',
            'desc': 'Ratio of cycles the FP32 cores are active',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'ratio',
            'value_converter': (lambda x: int(100 * x))
        },
    dcgm_fields.DCGM_FI_PROF_PCIE_TX_BYTES: # 1011
        {
            'name': 'custom.googleapis.com/gce/gpu/pcie_tx_throughput',
            'desc': 'PCIE transmit througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'Bytes per second',
            'value_converter': (lambda x: x) 
        },
    dcgm_fields.DCGM_FI_PROF_PCIE_RX_BYTES:
        {
            'name': 'custom.googleapis.com/gce/gpu/pcie_rx_throughput',
            'desc': 'PCIE receive througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'Bytes per second',
            'value_converter': (lambda x: x) 
        },
    dcgm_fields.DCGM_FI_PROF_NVLINK_TX_BYTES:
        {
            'name': 'custom.googleapis.com/gce/gpu/nvlink_tx_throughput',
            'desc': 'NVLink transmit througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'Bytes per second',
            'value_converter': (lambda x: x) 
        },
    dcgm_fields.DCGM_FI_PROF_NVLINK_RX_BYTES:
        {
            'name': 'custom.googleapis.com/gce/gpu/nvlink_rx_throughput',
            'desc': 'NVLink receive througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
            'dcgm_units': 'Bytes per second',
            'value_converter': (lambda x: x) 
        },
    # Future optional metrics. This metrics cannot be retrieved
    # together with the core metrics without a perf/accuracy penalty.
    # They could be used as drill down metrics
    # dcgm_fields.DCGM_FI_DEV_MEM_COPY_UTIL:
    # dcgm_fields.DCGM_FI_PROF_PIPE_FP64_ACTIVE:
    # dcgm_fields.DCGM_FI_PROF_PIPE_FP16_ACTIVE:
}


class DcgmStackdriver(DcgmReader):
    """
    Custom DCGM reader that pushes DCGM metrics to GCP Cloud Monitoring
    """
 
    def __init__(self, update_frequency, fields_to_watch, project_id):
       
        DcgmReader.__init__(self, fieldIds=fields_to_watch.keys(), 
                            fieldGroupName=FIELD_GROUP_NAME, 
                            updateFrequency=update_frequency * 1000 * 1000)
        
        self._fields_to_watch = fields_to_watch
        self._project_id = project_id
        self._resource_type = 'gce_instance'
        self._zone = 'us-west1-b'
        self._project_id = 'jk-mlops-dev'
        self._instance_id = '284365999706661199'

        self._client =  monitoring_v3.MetricServiceClient()
        self._project_name = self._client.project_path(self._project_id)
        
        self._create_sd_metric_descriptors()
        self._counter = 0
    
    def _create_sd_metric_descriptors(self):
        """
        Creates SD metric descriptors for the watched DCGM fields.
        """
        project_name = self._client.project_path(self._project_id) 
        for key, item in self._fields_to_watch.items():
            descriptor = monitoring_v3.types.MetricDescriptor()
            descriptor.type = item['name']
            descriptor.metric_kind = item['metric_kind'] 
            descriptor.value_type =  item['value_type']
            descriptor.description = item['desc']
            descriptor = self._client.create_metric_descriptor(project_name, descriptor)

    def _construct_sd_series(self, gpu_number, field_id, field_time_series):
        """Constructs SD time series from the DCGM field time_series."""

        series = None
        if field_id in self._fields_to_watch.keys():
            series = monitoring_v3.types.TimeSeries()
            series.metric.type = self._fields_to_watch[field_id]['name']
            series.metric.labels['gpu_number'] = str(gpu_number)
            series.resource.type = self._resource_type 
            series.resource.labels['instance_id'] = self._instance_id
            series.resource.labels['zone'] = self._zone
            series.resource.labels['project_id'] = self._project_id

            field_value = self._fields_to_watch[field_id]['value_converter'](field_time_series[-1].value)
            field_timestamp = field_time_series[-1].ts 
            seconds = field_timestamp // 10**6
            nanos = (field_timestamp % 10**6) * 10**3

            point = series.points.add()
            point.value.int64_value = field_value
            point.interval.end_time.seconds = seconds
            point.interval.end_time.nanos = nanos
            print(series)

        return series


    def _create_time_series(self, fvs):
        """
        Calls SD to create time series based on the latest values
        of DCGM watched fields/
        """

            #for gpuId in fvs.keys():
        #    gpuFv = fvs[gpuId]
        #    print(gpuFv)
        #    print('*****************')
        #gpuFv = fvs[0]
        #for field_id, value in fvs[0].items():
        #    print(field_id, self.m_fieldIdToInfo[field_id].tag, value[-1].value)
        #field = fvs[0][1002][-1] 
        #if self.previous_ts == field.ts:
        #    print("Duplicate detected") 
        #self.previous_ts = field.ts
        #print(self.m_fieldIdToInfo[1002].tag, field.ts, field.value)
        #

        
        time_series = []
        #for gpu in fvs:
        for gpu in [0]:
            for field_id, field_time_series in fvs[gpu].items():
                series = self._construct_sd_series(gpu, field_id, field_time_series)
                if series:
                    time_series.append(series)


        return
        

        series = monitoring_v3.types.TimeSeries()
        series.metric.type = 'custom.googleapis.com/gce/gpu/sm_active'
        series.resource.type = self._resource_type 
        series.resource.labels['instance_id'] = self._instance_id
        series.resource.labels['zone'] = self._zone
        series.resource.labels['project_id'] = self._project_id



        time_series = [series]


        print('**********')
        print(point)
        self._client.create_time_series(
            name=project_name, 
            time_series=time_series)


    def CustomDataHandler(self, fvs):
        """
        Writes reported field values to Cloud Monitoring.
        """

        self._counter += 1 
        if self._counter > 1:
            time_series = self._create_time_series(fvs)
    
    
    
    def LogInfo(self, msg):
        logging.info(msg)  # pylint: disable=no-member

    def LogError(self, msg):
        logging.info(msg)  # pylint: disable=no-member


def main(argv):
    del argv
    
    logging.info("main()")
    logging.info("Project ID:" + FLAGS.project_id)

    logging.info('Entering monitoring loop with update interval: ' + str(FLAGS.update_interval))
    
    with DcgmStackdriver(fields_to_watch=DCGM_FIELDS, 
                         update_frequency=FLAGS.update_interval,
                         project_id=FLAGS.project_id) as dcgm_reader:
        
        nexttime = time.time()
        try:
            # Sleep for one interval to allow the DCGM watches to catch up
            while True:
            #while False:
                dcgm_reader.Process()
                nexttime += FLAGS.update_interval
                sleep_time = nexttime - time.time() 
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except KeyboardInterrupt:
            logging.info("Caught CTRL-C. Exiting ...")

# Command line parameters
flags.DEFINE_integer('update_interval', 5, 'Metrics update frequency - seconds', 
                     lower_bound=5)
flags.DEFINE_string('project_id', None, 'GCP Project ID')
flags.mark_flag_as_required('project_id')

if __name__ == '__main__':
    app.run(main)
