# Copyright 2017 HuaWei Tld
# Copyright 2017 OpenStack.org
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import print_function
import time


# NOTE(samsong8610): The CDN endpoints are not in the service catalogs, so we
# must override it by setting the environment variable before connecting.
#
# import os
# os.environ['OS_CDN_ENDPOINT_OVERRIDE'] = 'https://cdn.myhwclouds.com/v1.0'


def list_logs(conn, domain_name):
    """List the logs about the given domain

    :param conn: an instance of :class:`~openstack.connection.Connection`
    :param domain_name: The name of the domain
    """
    today = int(time.time() * 1000)
    print('List the logs: ')
    for log in conn.logs(conn, domain_name=domain_name, query_date=today):
        print(log)
