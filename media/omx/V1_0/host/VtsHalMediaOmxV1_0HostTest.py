#!/usr/bin/env python
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
import time

from vts.runners.host import asserts
from vts.runners.host import keys
from vts.runners.host import test_runner
from vts.testcases.template.hal_hidl_gtest import hal_hidl_gtest
import VtsHalMediaOmxV1_0TestCase as omx_test_case


class VtsHalMediaOmxV1_0Host(hal_hidl_gtest.HidlHalGTest):
    """Host test class to run the Media_Omx HAL."""

    AUDIO_ENC_TEST = "AudioEncHidlTest"
    AUDIO_DEC_TEST = "AudioDecHidlTest"
    VIDEO_ENC_TEST = "VideoEncHidlTest"
    VIDEO_DEC_TEST = "VideoDecHidlTest"

    # Components and Roles which will be skipped.
    blacklist_components = ["OMX.qcom.video.decoder.avc",
                            "OMX.qcom.video.encoder.avc.secure",
                            "OMX.qcom.video.decoder.avc.secure",
                            "OMX.qcom.video.decoder.mpeg4.secure",
                            "OMX.qcom.video.decoder.mpeg4",
                            "OMX.qcom.video.decoder.h263",
                            "OMX.qcom.video.decoder.hevc",
                            "OMX.qcom.video.decoder.mpeg2.secure",
                            "OMX.qcom.video.decoder.mpeg2",
                            "OMX.qcom.video.decoder.vp8",
                            "OMX.qcom.video.decoder.vp9",
                            "OMX.qcom.video.decoder.hevc.secure",
                            "OMX.qcom.video.decoder.vp9.secure",
                            "OMX.qcom.video.decoder.vp8.secure"]
    blacklist_roles = ["video_encoder.avc",
                       "video_decoder.avc",
                       "video_encoder.avc",
                       "video_decoder.mpeg4",
                       "video_decoder.vp8",
                       "video_decoder.h263",
                       "video_decoder.hevc",
                       "video_decoder.mpeg2",
                       "video_decoder.vp9"]

    def CreateTestCases(self):
        """Get all registered test components and create test case objects."""
        # Init the IOmx hal.
        self._dut.hal.InitHidlHal(
            target_type="media_omx",
            target_basepaths=self._dut.libPaths,
            target_version=1.0,
            target_package="android.hardware.media.omx",
            target_component_name="IOmx",
            bits=64 if self._dut.is64Bit else 32)

        # Call listNodes to get all registered components.
        self.vtypes = self._dut.hal.media_omx.GetHidlTypeInterface("types")
        status, nodeList = self._dut.hal.media_omx.listNodes()
        asserts.assertEqual(self.vtypes.Status.OK, status)

        self.components = {}
        for node in nodeList:
            self.components[node['mName']] = node['mRoles']

        super(VtsHalMediaOmxV1_0Host, self).CreateTestCases()

    # @Override
    def CreateTestCase(self, path, tag=''):
        """Create a list of VtsHalMediaOmxV1_0testCase objects.

        For each target side gtest test case, create a set of new test cases
        argumented with different component and role values.

        Args:
            path: string, absolute path of a gtest binary on device
            tag: string, a tag that will be appended to the end of test name

        Returns:
            A list of VtsHalMediaOmxV1_0TestCase objects
        """
        gtest_cases = super(VtsHalMediaOmxV1_0Host, self).CreateTestCase(path,
                                                                         tag)
        test_cases = []

        for gtest_case in gtest_cases:
            test_suite = gtest_case.GetFullName()
            for component, roles in self.components.iteritems():
                for role in roles:
                    if component in self.blacklist_components and role in self.blacklist_roles:
                        continue
                    if self.AUDIO_ENC_TEST in test_suite and not "audio_encoder" in role:
                        continue
                    if self.AUDIO_DEC_TEST in test_suite and not "audio_decoder" in role:
                        continue
                    if self.VIDEO_ENC_TEST in test_suite and not "video_encoder" in role:
                        continue
                    if self.VIDEO_DEC_TEST in test_suite and not "video_decoder" in role:
                        continue
                    test_name = component + '_' + role
                    # TODO (zhuoyao): get instance name using lshal.
                    instance_name = "default"
                    test_case = omx_test_case.VtsHalMediaOmxV1_0TestCase(
                        component, role, instance_name, test_suite, test_name,
                        path)
                    test_cases.append(test_case)
        logging.info("num of test_testcases: %s", len(test_cases))
        return test_cases


if __name__ == "__main__":
    test_runner.main()
