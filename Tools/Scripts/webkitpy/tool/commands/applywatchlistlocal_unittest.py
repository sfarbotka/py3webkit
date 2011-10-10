# Copyright (c) 2011 Google Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from webkitpy.tool.commands.commandtest import CommandsTest
from webkitpy.tool.commands.applywatchlistlocal import ApplyWatchListLocal


class ApplyWatchListLocalTest(CommandsTest):
    def test_args_parsing(self):
        expected_stderr = 'MockWatchList: determine_cc_and_messages\n'
        self.assert_execute_outputs(ApplyWatchListLocal(), [''], expected_stderr=expected_stderr)

    def test_args_parsing_with_bug(self):
        expected_stderr = """MockWatchList: determine_cc_and_messages
MOCK bug comment: bug_id=50002, cc=set(['levin@chromium.org', 'abarth@webkit.org'])
--- Begin comment ---
Message1.

Message2.
--- End comment ---\n\n"""
        self.assert_execute_outputs(ApplyWatchListLocal(), ['50002'], expected_stderr=expected_stderr)

    def test_args_parsing_with_two_bugs(self):
        self._assertRaisesRegexp('Too many arguments given: 1234 5678', self.assert_execute_outputs, ApplyWatchListLocal(), ['1234', '5678'])
