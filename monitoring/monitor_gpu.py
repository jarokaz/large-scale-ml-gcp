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

FLAGS = flags.FLAGS

flags.DEFINE_integer('interval', 10, 'Sampling interval for collecting metrics', 
                     lower_bound=10)


def main(argv):
    del argv

    logging.info(f'Entering monitoring loop with sampling interval: {FLAGS.interval}s')

    while True:
        print("Reporting metric")
        time.sleep(FLAGS.interval)

if __name__ == '__main__':
    app.run(main)