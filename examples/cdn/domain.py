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


def list_domains(conn):
    print('List all domains: ')
    for domain in conn.cdn.domains():
        print(domain)

    # You can list domains by page.
    print('List 3rd and 4th domains: ')
    for domain in conn.cdn.domains(page_size=2, page_number=2):
        print(domain)

    # Also support filtering by some attributes
    print('List all domains in "online" status: ')
    for domain in conn.cdn.domains(domain_status='online'):
        print(domain)


def domain_creation(conn):
    print('Create a new acceleration domain name: ')
    attrs = {
        'domain_name': 'cdn.example.com',
        'business_type': 'web',
        'sources': [
            {
                'ip_or_domain': '1.2.3.4',
                'origin_type': 'ipaddr',
                'active_standby': 1         # 1 means this source is active
            }
        ]
    }
    domain = conn.cdn.create_domain(**attrs)
    print(domain)

    print('Get the domain details: ')
    domain = conn.cdn.get_domain(domain.id)

    print('Set domain\'s origin source hosts: ')
    source = {
        'ip_or_domain': 'cdnsrc1.example.com',
        'origin_type': 'domain',
        'active_standby': 1
    }
    domain = conn.cdn.set_domain_sources(domain, source)

    print('Set domain\'s origin host name: ')
    origin_host = {
        'origin_host_type': 'customize',
        'customize_domain': 'cdn.example.com'
    }
    domain = conn.cdn.set_domain_origin_host(domain, **origin_host)

    print('Get the updated origin host name: ')
    updated_origin = conn.cdn.get_domain_origin_host(domain)
    print(updated_origin)

    print('Set domain referer policies: ')
    referer = {
        'referer_type': 2,
        'referer_list': 'site.example.com;www.example.com',
        'include_empty': True
    }
    domain = conn.cdn.set_domain_referer(domain, referer)

    print('Get the updated referer policies: ')
    updated_referer = conn.cdn.get_domain_referer(domain)
    print(updated_referer)

    print('Set domain cache rules: ')
    print('Caching all content for 30 days.')
    cache_config = {
        'ignore_url_parameter': True,
        'rules': [
            {
                'rule_type': 0,
                'content': None,
                'ttl': 30,
                'ttl_type': 4,
                'priority': 1
            }
        ]
    }
    domain = conn.cdn.set_domain_cache_rules(domain, cache_config)

    print('Get the updated cache rules: ')
    updated_cache = conn.cdn.get_domain_cache_rules(domain)
    print(updated_cache)

    print('Set domain https configuration: ')
    cert_content = open('your-cert-file').read()
    key_content = open('your-private-rsa-key-file').read()
    https = {
        'cert_name': 'test_cert',
        'https_status': 2,
        'certificate': cert_content,
        'private_key': key_content
    }
    domain = conn.cdn.set_domain_https(domain, https)

    print('Get the updated https configuration: ')
    updated_https = conn.cdn.get_domain_https(domain)
    print(updated_https)

    print('Delete the domain: ')
    # Disable the domain before deleting
    conn.cdn.disable_domain()
    cnt = 30
    print('Waiting for domain disabled', end='')
    while cnt:
        print('.', end='')
        domain = conn.cdn.get_domain()
        if domain.domain_status == 'offline':
            break
        else:
            time.sleep(1)

    if cnt:
        conn.cdn.delete_domain(domain)
    else:
        print('Disable domain timeout')
