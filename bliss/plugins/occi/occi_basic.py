
import httplib
import time


class PyssfDummy(object):
    '''
    A simple OCCI interface for bliss.
    '''

    _url = '127.0.0.1:8888'

    def manager_create_compute(self, manager_obj, compute_desc):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Content-Type': 'text/occi'}

        # kinds & mixins
        heads['Category'] = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#"'

        # TODO: evaluate os/resource templates
        # heads['Category'] = heads['Category'] + 'term;scheme="http://example.com"'

        # extract data from compute description
        if hasattr(compute_desc, 'slots'):
            heads['X-OCCI-Attribute'] = 'occi.compute.cores=' + str(compute_desc.slots)
        # TODO: implement more...

        # TODO: evaluate os/resource templates

        # do request
        conn.request('POST', '/compute/', headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 201:
            raise AttributeError(response.status, response.reason)
        else:
            uri = response.getheader('Location', None)

        # close & return
        conn.close()
        return uri

    def manager_create_storage(self, manager_obj, storage_desc):
        # TODO
        pass

    def manager_list_compute_resources(self, manager_obj):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/occi'}

        # do request
        # TODO: get location from QI.
        conn.request('GET', '/compute/', headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            uris = response.getheader('X-OCCI-Location', None)

        # close & return
        conn.close()
        return [x.strip() for x in uris.split(',')]

    def manager_list_storage_resources(self, manager_obj):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/occi',
                 'Content-Type': 'text/occi'}

        heads['Category'] = 'storage;scheme="http://schemas.ogf.org/occi/infrastructure#"'

        # do request
        # TODO: do it with a filter here :-D
        conn.request('GET', '/', headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            uris = response.getheader('X-OCCI-Location', None)

        # close & return
        conn.close()
        if uris is not None:
            return [x.strip() for x in uris.split(',')]
        else:
            return []

    def manager_list_compute_templates(self, manager_obj):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/plain'}

        # do request
        conn.request('GET', '/-/', headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            data = response.read()

        # close & return
        conn.close()
        tmpl = []
        if data is not None:
            for item in data.split('\n'):
                if item.find('rel="http://schemas.ogf.org/occi/infrastructure#resource tpl"') != -1:
                    tmpl.append(item)
                #
            return tmpl
        else:
            return None

    def manager_list_storage_templates(self, manager_obj):
        # TODO: see above
        # http://schemas.ogf.org/occi/infrastructure#os tpl
        pass

    def manager_get_template_details(self, manager_obj, t_id):
        # TODO: see above
        pass

    def manager_get_compute(self, manager_obj, compute_id):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/plain'}

        # do request
        # XXX: do it with a filter here :-D
        conn.request('GET', compute_id, headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            uris = response.read()

        conn.close()
        return uris

    def manager_get_storage(self, manager_obj, storage_id):
        # TODO: see get compute
        pass

    def manager_destroy_compute(self, manager_obj, compute_id, drain):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # do request
        # XXX: do it with a filter here :-D
        conn.request('DELETE', compute_id)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)

    def manager_destroy_storage(self, manager_obj, storage_id, drain):
        # TODO: see above...
        pass

    ######## Method templates for saga.resource.Compute functionality 
    ##
    def compute_resource_get_state(self, res_obj):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/occi'}

        # do request
        # TODO: Get id from res_obj
        conn.request('GET', res_obj, headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            data = response.getheader('X-OCCI-Attribute')

        conn.close()

        # parse data
        attributes = [x.strip() for x in data.split(',')]
        for item in attributes:
            name = item.split('=')[0]
            if name == 'occi.compute.state':
                return item.split('=')[1].strip('"')
        return 'N/A'

    def compute_resource_get_state_detail(self, res_obj):
        # TODO: not sure what to do here...
        pass

    def compute_resource_get_job_service(self, res_obj):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/occi'}

        # do request
        # TODO: Get id from res_obj
        conn.request('GET', res_obj, headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            attr = response.getheaders()

        conn.close()
        # parse data
        if attr.get_header('Category').find('http://example.com/bes-endpoint#bes') != -1:
            attributes = [x.strip() for x in attr.get_header('X-OCCI-Attribute').split(',')]
            for item in attributes:
                name = item.split('=')[0]
                if name == 'bes.endpoint':
                    return item.split('=')[1].strip('"')
        else:
            return None

    def compute_resource_get_id(self, res_obj):
        # TODO: id is is res_obj...
        pass

    def compute_resource_get_manager(self, res_obj):
        # TODO: not sure what to do here...
        return self._url

    def compute_resource_get_description(self, res_obj):
        # attributes abhohlen...

        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # basic header
        heads = {'Accept': 'text/occi'}

        # do request
        # TODO: Get id from res_obj
        conn.request('GET', res_obj, headers=heads)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)
        else:
            data = response.getheader('X-OCCI-Attribute')

        conn.close()

        # parse data
        attributes = [x.strip() for x in data.split(',')]
        return attributes

    def compute_resource_destroy(self, res_obj, drain):
        # open conn.
        conn = httplib.HTTPConnection(self._url)

        # do request
        # TODO: get compute ide from res_obj.
        conn.request('DELETE', res_obj)
        response = conn.getresponse()

        # some err handling...
        if response.status != 200:
            raise AttributeError(response.status, response.reason)

    def compute_resource_wait(self, res_obj, filter):
        for i in range(0, 15):
            time.sleep(1)
            if self.compute_resource_get_state(res_obj) == filter:
                return
            else:
                continue

    ######## Method templates for saga.resource.Storage functionality 
    ##
    def storage_resource_get_state(self, res_obj):
        # TODO: see above
        pass

    def storage_resource_get_state_detail(self, res_obj):
        # TODO: see above
        pass

    def storage_resource_get_id(self, res_obj):
        # TODO: see above
        pass

    def storage_resource_get_manager(self, res_obj):
        # TODO: see above
        pass

    def storage_resource_get_description(self, res_obj):
        # TODO: see above
        pass

    def storage_resource_destroy(self, res_obj, drain):
        # TODO: see above
        pass

    def storage_resource_wait(self, res_obj, filter):
        # TODO: see above
        pass

