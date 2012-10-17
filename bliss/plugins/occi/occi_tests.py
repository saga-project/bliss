from bliss.plugins.occi import occi_basic
import unittest
from bliss.saga.resource import ComputeDescription


class OcciTest(unittest.TestCase):

    occi = occi_basic.PyssfDummy()

    def test_manager_create_compute(self):
        desc = ComputeDescription()
        desc.slots = 2
        uri = self.occi.manager_create_compute(None, desc)
        self.assertTrue(uri.find('/compute/') != -1)

    def test_manager_list_compute_resoucrs(self):
        uri = self.occi.manager_create_compute(None, None)
        uris = self.occi.manager_list_compute_resources(None)
        self.assertTrue(len(uris) >= 1)
        self.assertTrue(uri in uris)

    def test_manager_list_compute_templates(self):
        data = self.occi.manager_list_compute_templates(None)

    def test_manager_list_storage_resources(self):
        # TODO come up with more useful test...
        uris = self.occi.manager_list_storage_resources(None)

    def test_manager_get_compute(self):
        uri = self.occi.manager_create_compute(None, None)
        uri = uri[len(self.occi._url) + 7:]
        self.occi.manager_get_compute(None, uri)

    def test_compute_resource_get_state(self):
        uri = self.occi.manager_create_compute(None, None)
        uri = uri[len(self.occi._url) + 7:]
        self.occi.compute_resource_get_state(uri)

    def test_compute_resource_get_description(self):
        uri = self.occi.manager_create_compute(None, None)
        uri = uri[len(self.occi._url) + 7:]
        self.occi.compute_resource_get_description(uri)

    def test_compute_resource_destroy(self):
        uri = self.occi.manager_create_compute(None, None)
        uri = uri[len(self.occi._url) + 7:]
        self.occi.compute_resource_destroy(uri, None)
