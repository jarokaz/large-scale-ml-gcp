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
import dcgm_fields

from absl import app
from absl import flags
#from absl import logging
import logging

from DcgmReader import DcgmReader

from google.cloud import monitoring_v3


FLAGS = flags.FLAGS



# DCGM fields to SD metrics mapping
DCGM_FIELDS = {
    # Equivalents of the basic metrics in nvidia-smi
    dcgm_fields.DCGM_FI_DEV_GPU_UTIL:
        {
            'name': 'gce/gpu/utilization',
            'desc': 'GPU utilization',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_DEV_FB_USED:
        {
            'name': 'gce/gpu/mem_used',
            'desc': 'GPU memory used',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_DEV_POWER_USAGE:
        {
            'name': 'gce/gpu/power_usage',
            'desc': 'Power usage',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    # Profiling metrics recommended by NVidia
    dcgm_fields.DCGM_FI_PROF_GR_ENGINE_ACTIVE:
        {
            'name': 'gce/gpu/gr_engine_active',
            'desc': 'Ratio of time the graphics engine is active',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_PROF_SM_ACTIVE: 
        {
            'name': 'gce/gpu/sm_active',
            'desc': 'Ratio of cycles an SM has at least 1 warp assigned',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_PROF_SM_OCCUPANCY: 
        {
            'name': 'gce/gpu/sm_occupancy',
            'desc': 'Ratio of number of warps resident on an SM',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_PROF_DRAM_ACTIVE:
        {
            'name': 'gce/gpu/memory_active',
            'desc': 'Ratio of cycles the device memory inteface is active sending or receiving data',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64,  
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_TENSOR_ACTIVE: 
        {
            'name': 'gce/gpu/tensor_active',
            'desc': 'Ratio of cycles the tensor cores are active',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64,  
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_FP32_ACTIVE:
        {
            'name': 'gce/gpu/fp32_active',
            'desc': 'Ratio of cycles the FP32 cores are active',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64,  
        },
    dcgm_fields.DCGM_FI_PROF_PCIE_TX_BYTES:
        {
            'name': 'gce/gpu/pcie_tx_throughput',
            'desc': 'PCIE transmit througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_PROF_PCIE_RX_BYTES:
        {
            'name': 'gce/gpu/pcie_rx_throughput',
            'desc': 'PCIE receive througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_PROF_NVLINK_TX_BYTES:
        {
            'name': 'gce/gpu/nvlink_tx_throughput',
            'desc': 'NVLink transmit througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    dcgm_fields.DCGM_FI_PROF_NVLINK_RX_BYTES:
        {
            'name': 'gce/gpu/nvlink_rx_throughput',
            'desc': 'NVLink receive througput',
            'metric_kind': monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
            'value_type': monitoring_v3.enums.MetricDescriptor.ValueType.INT64, 
        },
    # Future optional metrics. This metrics cannot be retrieved
    # together with the core metrics without a perf/accuracy penalty.
    # They could be used as drill down metrics
    # dcgm_fields.DCGM_FI_DEV_MEM_COPY_UTIL:
    # dcgm_fields.DCGM_FI_PROF_PIPE_FP64_ACTIVE:
    # dcgm_fields.DCGM_FI_PROF_PIPE_FP16_ACTIVE:
}



FIELD_GROUP_NAME = 'dcgm_stackdriver'

class DcgmStackdriver(DcgmReader):
    """
    Custom DCGM reader that pushes DCGM metrics to GCP Cloud Monitoring
    """
 
    def __init__(self, update_frequency, fields_to_watch):
       
        DcgmReader.__init__(self, fieldIds=fields_to_watch.keys(), 
                            fieldGroupName=FIELD_GROUP_NAME, 
                            updateFrequency=update_frequency * 1000 * 1000)
        
        self._fields_to_watch = fields_to_watch
        
        # If the identical metrics descriptors already exist the following
        # call will have no effect
        self._create_sd_metric_descriptors()


        self._counter = 0
    
    def _create_sd_metric_descriptors(self):
        """
        Creates SD metric descriptors for the watched DCGM fields.
        """
        
        for key, item in self._fields_to_watch.items():
            print(key, item['name'])

    def _create_time_series(self, fvs):
        """
        Calls SD to create time series based on the latest values
        of DCGM watched fields/
        """

        print('In _create_time_series')



    def CustomDataHandler(self, fvs):
        """
        Writes reported field values to Cloud Monitoring.
        """

        time_series = self._create_time_series(fvs)
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
                         update_frequency=FLAGS.update_interval) as dcgm_reader:
        
        nexttime = time.time()
        try:
            while True:
                dcgm_reader.Process()
                nexttime += FLAGS.update_interval
                sleep_time = nexttime - time.time() 
                if sleep_time > 0:
                    print(sleep_time)
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
