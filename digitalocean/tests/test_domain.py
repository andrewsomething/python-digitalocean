import json
import unittest

import responses

import digitalocean
from .BaseTest import BaseTest


class TestDomain(BaseTest):

    def setUp(self):
        super(TestDomain, self).setUp()
        self.domain = digitalocean.Domain(name='example.com', token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('domains/single.json')

        url = self.base_url + "domains/example.com"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        domain = digitalocean.Domain(name='example.com', token=self.token)
        domain.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(domain.name, "example.com")
        self.assertEqual(domain.ttl, 1800)

    @responses.activate
    def test_destroy(self):
        url = self.base_url + "domains/example.com"
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        self.domain.destroy()

        self.assertEqual(responses.calls[0].request.url, url)

    @responses.activate
    def test_create_new_domain_record(self):
        data = self.load_from_file('domains/create_record.json')

        url = self.base_url + "domains/example.com/records"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        response = self.domain.create_new_domain_record(
            type="CNAME", name="www", data="@")

        self.assert_url_query_equal(
            responses.calls[0].request.url,
            self.base_url + "domains/example.com/records")
        self.assertEqual(json.loads(responses.calls[0].request.body),
                         {"type": "CNAME", "data": "@", "name": "www"})
        self.assertEqual(response['domain_record']['type'], "CNAME")
        self.assertEqual(response['domain_record']['name'], "www")
        self.assertEqual(response['domain_record']['data'], "@")

    @responses.activate
    def test_create(self):
        data = self.load_from_file('domains/create.json')

        url = self.base_url + "domains"
        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        domain = digitalocean.Domain(name="example.com",
                                     ip_address="1.1.1.1",
                                     token=self.token).create()

        self.assert_url_query_equal(
            responses.calls[0].request.url, self.base_url + "domains")
        self.assertEqual(json.loads(responses.calls[0].request.body),
                         {'ip_address': '1.1.1.1', 'name': 'example.com'})
        self.assertEqual(domain['domain']['name'], "example.com")
        self.assertEqual(domain['domain']['ttl'], 1800)

    @responses.activate
    def test_get_records(self):
        data = self.load_from_file('domains/records.json')

        url = self.base_url + "domains/example.com/records/"
        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        records = self.domain.get_records()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(len(records), 5)
        self.assertEqual(records[0].type, "A")
        self.assertEqual(records[0].name, "@")
        self.assertEqual(records[4].type, "CNAME")
        self.assertEqual(records[4].name, "example")

if __name__ == '__main__':
    unittest.main()
