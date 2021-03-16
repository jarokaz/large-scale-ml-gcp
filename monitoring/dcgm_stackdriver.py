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

flags.DEFINE_integer('sampling_interval', 2, 'Sampling interval for collecting metrics - seconds', 
                     lower_bound=1)
flags.DEFINE_integer('update_frequency', 1000, 'DCGM update frequency - miliseconds seconds', 
                     lower_bound=1)
flags.DEFINE_integer('reporting_interval', 30, 'Reporting interval to Cloud Monitoring - seconds', 
                     lower_bound=10)
flags.DEFINE_string('project_id', None, 'GCP Project ID')
flags.mark_flag_as_required('project_id')

# Mapping DCGM fields to OC metrics
FIELDS_TO_SD = {
    dcgm_fields.DCGM_FI_DEV_POWER_USAGE:
        {
            'name': 'power_usage',
            'desc': 'power usage',
            'metric_kind': 'Watts',
            'buckets': [], 
        },
    dcgm_fields.DCGM_FI_DEV_GPU_UTIL:
        {
            'name': 'gpu_utilization',
            'desc': 'GPU utilization',
            'units': '%',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101],
        },
    dcgm_fields.DCGM_FI_DEV_MEM_COPY_UTIL:
        {
            'name': 'mem_cpu_utilization',
            'desc': 'memory copy utilization',
            'units': '%',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101],
        },
    dcgm_fields.DCGM_FI_PROF_DRAM_ACTIVE:
        {
            'name': 'memory_active',
            'desc': 'ratio of cycles the device memory inteface is active sending or receiving data',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101],
        },
    dcgm_fields.DCGM_FI_DEV_FB_TOTAL:
        {
            'name': 'fb_total',
            'desc': 'Total framebuffer memory',
            'units': 'MBs',
        },
    dcgm_fields.DCGM_FI_DEV_FB_FREE:
        {
            'name': 'fb_free',
            'desc': 'Free framebuffer memory',
            'units': 'MBs',
        },
    dcgm_fields.DCGM_FI_DEV_FB_USED:
        {
            'name': 'fb_used',
            'desc': 'Used framebuffer memory',
            'units': 'MBs',
        },
    dcgm_fields.DCGM_FI_PROF_GR_ENGINE_ACTIVE:
        {
            'name': 'gr_engine_active',
            'desc': 'ratio of time the graphics engine is active',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_SM_ACTIVE: # 1
        {
            'name': 'sm_active',
            'desc': 'ratio of cycles an SM has at least 1 warp assigned',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_SM_OCCUPANCY: # 1
        {
            'name': 'sm_occupancy',
            'desc': 'ratio of number of warps resident on an SM',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_TENSOR_ACTIVE: # 2
        {
            'name': 'tensor_active',
            'desc': 'ratio of cycles the tensor cores are active',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_FP64_ACTIVE:
        {
            'name': 'fp64_active',
            'desc': 'ratio of cycles the FP64 cores are active',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_FP32_ACTIVE:
        {
            'name': 'fp32_active',
            'desc': 'ratio of cycles the FP32 cores are active',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_PIPE_FP16_ACTIVE:
        {
            'name': 'fp16_active',
            'desc': 'ratio of cycles the FP16 cores are active',
            'units': 'ratio',
            'buckets': [11, 21, 31, 41, 51, 61, 71, 81, 91, 101], 
        },
    dcgm_fields.DCGM_FI_PROF_PCIE_TX_BYTES:
        {
            'name': 'pcie_tx_throughput',
            'desc': 'PCIE transmit througput',
            'units': 'bytes per second',
            'buckets': [], 
        },
    dcgm_fields.DCGM_FI_PROF_PCIE_RX_BYTES:
        {
            'name': 'pcie_rx_throughput',
            'desc': 'PCIE receive througput',
            'units': 'bytes per second',
            'buckets': [], 
        },
    dcgm_fields.DCGM_FI_PROF_NVLINK_TX_BYTES:
        {
            'name': 'nvlink_tx_throughput',
            'desc': 'NVLink transmit througput',
            'units': 'bytes per second',
            'buckets': [], 
        },
    dcgm_fields.DCGM_FI_PROF_NVLINK_RX_BYTES:
        {
            'name': 'nvlink_rx_throughput',
            'desc': 'NVLink receive througput',
            'units': 'bytes per second',
            'buckets': [], 
        },
}



FIELD_GROUP_NAME = 'dcgm_stackdriver'

class DcgmStackdriver(DcgmReader):
    """
    Custom DCGM reader that pushes DCGM metrics to GCP Cloud Monitoring
    """
    def __init__(self, update_frequency, field_ids):
        DcgmReader.__init__(self, fieldIds=field_ids, 
                            fieldGroupName=FIELD_GROUP_NAME, 
                            updateFrequency=update_frequency * 1000 * 1000)

        self.previous_ts = 0.0


    def _define_oc_metrics():
        """
        Creates and registers Open Census metrics.
        """



    def CustomDataHandler(self, fvs):
        """
        Writes reported field values to Cloud Monitoring.
        """
        #for gpuId in fvs.keys():
        #    gpuFv = fvs[gpuId]
        #    print(gpuFv)
        #    print('*****************')
        gpuFv = fvs[0]
        #for field_id, value in fvs[0].items():
        #    print(field_id, self.m_fieldIdToInfo[field_id].tag, value[-1].value)
        field = fvs[0][1002][-1] 
        if self.previous_ts == field.ts:
            print("Duplicate detected") 
        self.previous_ts = field.ts
        #print(self.m_fieldIdToInfo[1002].tag, field.ts, field.value) 
    
    def LogInfo(self, msg):
        logging.info(msg)  # pylint: disable=no-member

    def LogError(self, msg):
        logging.info(msg)  # pylint: disable=no-member


def main(argv):
    del argv
    
    logging.info("main()")
    logging.info("Project ID:" + FLAGS.project_id)

    logging.info('Entering monitoring loop with sampling interval: ' + str(FLAGS.sampling_interval))
    
    #tmap = tags.tag_map.TagMap()
    #tmap.insert(key_device, tags.tag_value.TagValue("0"))


    return
    
    with DcgmStackdriver() as dcgm_reader:
        try:
            while True:
                #metrics = get_gpu_metrics()
                #for device_index in range(len(metrics)):
                #    mmap = stats.stats.stats_recorder.new_measurement_map()
                #    
                #    mmap.measure_int_put(gpu_utilization_ms, metrics[device_index]['utilization']['gpu_util'])
                #    mmap.measure_int_put(gpu_memory_utilization_ms, metrics[device_index]['utilization']['memory_util'])
                #    power_percentage = metrics[device_index]['power_readings']['power_draw'] / metrics[device_index]['power_readings']['power_limit']
                #    #logging.info(round(power_percentage,2))
                #    mmap.measure_int_put(gpu_power_utilization_ms, round(power_percentage,2))
                #    
                #    tmap.update(key_device, tags.tag_value.TagValue(str(device_index)))
                #    mmap.record(tmap)
                    #logging.info(mmap)
                    #logging.info(tmap)
                
                time.sleep(FLAGS.sampling_interval)
                dcgm_reader.Process()
        except KeyboardInterrupt:
            print("Caught CTRL-C. Exiting ...")


if __name__ == '__main__':
    app.run(main)
