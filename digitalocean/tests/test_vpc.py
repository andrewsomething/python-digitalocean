import json
import unittest
import responses
import digitalocean

from .BaseTest import BaseTest


class TestVPC(BaseTest):

    def setUp(self):
        super(TestVPC, self).setUp()
        self.vpc_id = '953d698c-dg84-11e8-80bc-3cfdfeaae000'
        self.vpc = digitalocean.VPC(id=self.vpc_id, token=self.token)

    @responses.activate
    def test_load(self):
        data = self.load_from_file('vpcs/single.json')
        url = self.base_url + 'vpcs/' + self.vpc_id

        responses.add(responses.GET,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.vpc.load()

        self.assert_get_url_equal(responses.calls[0].request.url, url)
        self.assertEqual(self.vpc.id, self.vpc_id)
        self.assertEqual(self.vpc.name, 'default-nyc3')
        self.assertEqual(self.vpc.region, 'nyc3')
        self.assertEqual(self.vpc.created_at, '2019-02-19T18:48:45Z')
        self.assertEqual(self.vpc.default, True)

    @responses.activate
    def test_create(self):
        data = self.load_from_file('vpcs/single.json')
        url = self.base_url + 'vpcs'

        responses.add(responses.POST,
                      url,
                      body=data,
                      status=201,
                      content_type='application/json')

        vpc = digitalocean.VPC(name='default-nyc3',
                               region='nyc3',
                               token=self.token).create()

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(vpc.id, '953d698c-dg84-11e8-80bc-3cfdfeaae000')
        self.assertEqual(vpc.name, 'default-nyc3')
        self.assertEqual(vpc.created_at, '2019-02-19T18:48:45Z')

    @responses.activate
    def test_rename(self):
        data = self.load_from_file('vpcs/single.json')
        url = self.base_url + 'vpcs/' + self.vpc_id
        responses.add(responses.PATCH,
                      url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.vpc.rename('default-nyc3')

        self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(self.vpc.id, '953d698c-dg84-11e8-80bc-3cfdfeaae000')
        self.assertEqual(self.vpc.name, 'default-nyc3')
        self.assertEqual(self.vpc.created_at, '2019-02-19T18:48:45Z')

    @responses.activate
    def test_destroy(self):
        url = self.base_url + 'vpcs/' + self.vpc_id
        responses.add(responses.DELETE,
                      url,
                      status=204,
                      content_type='application/json')

        self.vpc.destroy()

        self.assertEqual(responses.calls[0].request.url, url)


if __name__ == '__main__':
    unittest.main()
