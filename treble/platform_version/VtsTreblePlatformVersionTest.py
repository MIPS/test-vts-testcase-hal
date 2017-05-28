#!/usr/bin/env python3.4
#
# Copyright (C) 2017 The Android Open Source Project
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
from vts.runners.host import base_test
from vts.runners.host import const
from vts.runners.host import test_runner
from vts.utils.python.controllers import android_device

ANDROID_O_API_VERSION = 26

class VtsTreblePlatformVersionTest(base_test.BaseTestClass):
    """VTS should run on devices launched with O or later."""

    def setUpClass(self):
        self.dut = self.registerController(android_device)[0]
        self.dut.shell.InvokeTerminal("VtsTreblePlatformVersionTest")

    def getProp(self, prop):
        """Helper to retrieve a property from device."""

        results = self.dut.shell.VtsTreblePlatformVersionTest.Execute(
            "getprop " + prop)
        asserts.assertEqual(results[const.EXIT_CODE][0], 0,
            "getprop must succeed")

        result = results[const.STDOUT][0].strip()

        logging.info("getprop {}={}".format(prop, result))

        return result

    def testPlatformVersion(self):
        """Test that device launched with O or later."""

        try:
            firstApiLevel = int(self.getProp("ro.product.first_api_level"))
            asserts.assertTrue(firstApiLevel >= ANDROID_O_API_VERSION,
                "VTS can only be run for new launches in O or above")
        except ValueError:
            asserts.fail("Unexpected value returned from getprop")

    def testTrebleEnabled(self):
        """Test that device has Treble enabled."""

        trebleIsEnabledStr = self.getProp("ro.treble.enabled")
        asserts.assertEqual(trebleIsEnabledStr, "true",
            "VTS can only be run for Treble enabled devices")

    def testVndkVersion(self):
        """Test that VNDK version is specified."""
        vndkVersion = self.getProp("ro.vendor.vndk.version")
        asserts.assertLess(0, len(vndkVersion),
            "VNDK version is not defined")

if __name__ == "__main__":
    test_runner.main()
