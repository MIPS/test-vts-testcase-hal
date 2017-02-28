#!/usr/bin/env python
#
# Copyright (C) 2016 The Android Open Source Project
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
#

import logging

from vts.runners.host import asserts
from vts.runners.host import base_test_with_webdb
from vts.runners.host import const
from vts.runners.host import keys
from vts.runners.host import test_runner
from vts.utils.python.controllers import android_device
from vts.utils.python.coverage import coverage_utils
from vts.utils.python.profiling import profiling_utils


class TvInputHidlTest(base_test_with_webdb.BaseTestWithWebDbClass):
    """Two hello world test cases which use the shell driver."""

    def setUpClass(self):
        """Creates a mirror and init tv input hal."""
        self.dut = self.registerController(android_device)[0]

        self.dut.shell.InvokeTerminal("one")
        self.dut.shell.one.Execute("setenforce 0")  # SELinux permissive mode

        if getattr(self, keys.ConfigKeys.IKEY_ENABLE_COVERAGE, False):
            coverage_utils.InitializeDeviceCoverage(self.dut)

        self.dut.hal.InitHidlHal(target_type="tv_input",
                                 target_basepaths=self.dut.libPaths,
                                 target_version=1.0,
                                 target_package="android.hardware.tv.input",
                                 target_component_name="ITvInput",
                                 bits=64 if self.dut.is64Bit else 32)

        self.dut.shell.InvokeTerminal("one")

    def setUpTest(self):
        """Setup function that will be called every time before executing each
        test case in the test class."""
        if self.enable_profiling:
            profiling_utils.EnableVTSProfiling(self.dut.shell.one)

    def tearDownTest(self):
        """TearDown function that will be called every time after executing each
        test case in the test class."""
        if self.enable_profiling:
            profiling_trace_path = getattr(
                self, self.VTS_PROFILING_TRACING_PATH, "")
            self.ProcessTraceDataForTestCase(self.dut, profiling_trace_path)
            profiling_utils.DisableVTSProfiling(self.dut.shell.one)

    def tearDownClass(self):
        """To be executed when all test cases are finished."""
        if getattr(self, keys.ConfigKeys.IKEY_ENABLE_COVERAGE, False):
            self.SetCoverageData(coverage_utils.GetGcdaDict(self.dut))

        if self.enable_profiling:
            self.ProcessAndUploadTraceData()

    def testGetStreamConfigurations(self):
        configs = self.dut.hal.tv_input.getStreamConfigurations(0)
        logging.info('return value of getStreamConfigurations(0): %s', configs)


if __name__ == "__main__":
    test_runner.main()