# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import print_function
from __future__ import division
from __future__ import print_function

import numpy as np
import paddle


class InputField(object):
    """
    A high-level API for handling inputs in PaddlePaddle.
    """

    def __init__(self, input_slots=[]):

        self.shapes = []
        self.dtypes = []
        self.names = []
        self.lod_levels = []

        self.input_slots = {}
        self.feed_list_str = []
        self.feed_list = []

        self.loader = None

        if input_slots:
            for input_slot in input_slots:
                self += input_slot

    def __add__(self, input_slot):

        if isinstance(input_slot, list) or isinstance(input_slot, tuple):
            name = input_slot[0]
            shape = input_slot[1]
            dtype = input_slot[2]
            lod_level = input_slot[3] if len(input_slot) == 4 else 0

        if isinstance(input_slot, dict):
            name = input_slot["name"]
            shape = input_slot["shape"]
            dtype = input_slot["dtype"]
            lod_level = input_slot[
                "lod_level"] if "lod_level" in input_slot else 0

        self.shapes.append(shape)
        self.dtypes.append(dtype)
        self.names.append(name)
        self.lod_levels.append(lod_level)

        self.feed_list_str.append(name)

        return self

    def __getattr__(self, name):

        if name not in self.input_slots:
            raise Warning("the attr %s has not been defined yet." % name)
            return None

        return self.input_slots[name]

    def build(self):

        for _name, _shape, _dtype, _lod_level in zip(
                self.names, self.shapes, self.dtypes, self.lod_levels):
            self.input_slots[_name] = paddle.static.data(
                name=_name, shape=_shape, dtype=_dtype, lod_level=_lod_level)

        for name in self.feed_list_str:
            self.feed_list.append(self.input_slots[name])
