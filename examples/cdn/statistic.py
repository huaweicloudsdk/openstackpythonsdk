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


def query_statistics(conn, domain_name):
    """Query statistic data about the given domain

    :param conn: an instance of :class:`~openstack.connection.Connection`
    :param domain_name: The name of the domain
    """
    print('Query the total network traffic: ')
    total_traffic = conn.query_network_traffic(domain_name=domain_name)
    print(total_traffic)

    # You can limit the query time range like this.
    print('Query the total network traffic in the last 1 hour: ')
    now = time.time()
    # Convert to milliseconds
    end_time = int(now * 1000)
    start_time = end_time - 3600000
    traffic_last_hour = conn.query_network_traffic(
        start_time=start_time, end_time=end_time, domain_name=domain_name)
    print(traffic_last_hour)

    # Query network traffic details
    print('Query network traffic details per hour: ')
    traffic_per_hour = conn.query_network_traffic_detail(interval=3600)
    print(traffic_per_hour)
