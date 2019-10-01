# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from .basecase import BaseTestCase
from .cassconnect import testrun_cqlsh
from .ansi_colors import ColoredText
import sys

class TestCqlshRestrictedQueries(BaseTestCase):

    def test_restricted_query_blocked(self):
        envs = [
            {}, # Test with no env vars set
            {'CQLSH_RESTRICTED_TABLES': 'dc_blob_store_group'}
        ]
        table_names = ['dc_blob_store_group']
        for env in envs:
            with testrun_cqlsh(tty=True, env=env) as c:
                for table in table_names:
                    restricted_query_templates = [
                        'insert into {0} (id) values ("g");',
                        'update {0} set id = "g";',
                        'delete from {0};',
                        'consistency all; delete from {0};'
                    ]
                    allowed_query_templates = [
                        'select * from {0};'
                    ]
                    restricted_queries = [
                        t.format(table) for t in restricted_query_templates]
                    allowed_queries = [
                        t.format(table) for t in allowed_query_templates]

                expected_error_msg = 'Mutations on {0} are not allowed'.format(table)
                for query_list, is_restricted in [(restricted_queries, True), (allowed_queries, False)]:
                    for query in query_list:
                        output = c.cmd_and_response(query).lstrip("\r\n")
                        c_output = ColoredText(output)
                        if is_restricted:
                            self.assertTrue(
                                expected_error_msg in c_output.plain(),
                                'Restricted query {0} was not blocked'.format(query)
                            )
                        else:
                            self.assertTrue(
                                expected_error_msg not in c_output.plain(),
                                'Non-restricted query {0} was blocked'.format(query)
                            )

