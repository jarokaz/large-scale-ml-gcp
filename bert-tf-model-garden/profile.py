# Lint as: python3
# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Starts a profiler run."""

import tensorflow as tf

from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS

def main(_):
    tf.profiler.experimental.client.trace(
        f'grpc://localhost:{FLAGS.profiler_port}',
        FLAGS.tb_log_dir,
        FLAGS.duration
    )
    logging.info(
        f'Profiling completed. Duration: {FLAGS.duration}ms. Logs in: {FLAGS.tb_log_dir}')

flags.DEFINE_integer(
    'profiler_port',
    default=6009,
    help='The port for the profiler server.')

flags.DEFINE_integer(
    'duration',
    default=2000,
    help='The duration of a profiler run.')

flags.DEFINE_string(
    'tb_log_dir',
    default=None,
    help='The location for the profiler logs.')
flags.mark_flag_as_required('tb_log_dir')

if __name__ == '__main__':
  app.run(main)
