from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from api.views import NetworkList, NetworkDetail, RouterList, RouterDetail

# from rest_framework.authtoken.models import Token # util doar pentru autentificarea standard cu token(nu JWT)
from rest_framework import status
from rest_framework.test import APITestCase


class UrlsTests(SimpleTestCase):
    """
    Testare legatura url - view
    """
    # reverse reutrneaza url din urls.py in functie de atributul name din path. Ex rezultat: ('/api/networks/').
    # resolve returns an object that describes the matching view for a given url
    def test_networks_url_is_resolved(self):
        url = reverse('networks')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func.view_class, NetworkList)

    def test_network_url_is_resolved(self):
        url = reverse('network', args=[1])
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func.view_class, NetworkDetail)

    def test_routers_url_is_resolved(self):
        url = reverse('routers')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func.view_class, RouterList)

    def test_router_url_is_resolved(self):
        url = reverse('router', args=[1])
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func.view_class, RouterDetail)


class NetworkListTest(APITestCase):
    """
    Testare NetworkList View
    """
    token_url = reverse('token_obtain_pair')
    networks_url = reverse('networks')
    routers_url = reverse('routers')

    # Se creaza automat un database pentru test. Nu este folosit db de development
    def setUp(self):
        self.user = User.objects.create_user(username='user_one', password='pass')
        token_response = self.client.post(path=self.token_url,
                                          data={'username': 'user_one', 'password': 'pass'})
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        router_data = {
            'name': 'RTR_TEST_001',
            'management_ip': '10.0.0.5',
            'os_type': 'Linux',
        }
        network_data = {
            'name': 'TestNetwork_00',
            'vlan_tag': '50',
            'network_address': '192.168.0.0/16',
            'router': '1'
        }
        # Scriem in db un router necesar pentru teste (nu se poate crea o retea fara a o asigna unui router)
        self.client.post(path=self.routers_url, data=router_data, format='json')
        self.client.post(path=self.networks_url, data=network_data, format='json')

    def test_network_get_list_success(self):
        response = self.client.get(self.networks_url)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assertEqual nu functioneaza aplicat pe intreg raspunsul pentru ca raspunsul include un model nested al
        # routerului. Deci un ordered dict intr-un ordered dict.
        self.assertEqual(response.data[0]['name'], 'TestNetwork_00')

    def test_networks_list_get_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.networks_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_network_post_invalid_input(self):
        data = {
            'name': 'TestNetwork_01',
            'vlan_tag': 'vlan tag invalid',
            'network_address': '172.16.0.0/12',
            'router': '1'
        }
        response = self.client.post(path=self.networks_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_network_post_success(self):
        data = {
            'name': 'TestNetwork_01',
            'vlan_tag': '2000',
            'network_address': '172.16.0.0/12',
            'router': '1'
        }
        response = self.client.post(path=self.networks_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 2, 'name': 'TestNetwork_01', 'vlan_tag': '2000',
                                         'network_address': '172.16.0.0/12', 'router': 1,
                                         'description': None})


class NetworkDetailTest(APITestCase):
    """
    Testare NetworkDetail View
    """
    token_url = reverse('token_obtain_pair')
    routers_url = reverse('routers')
    networks_url = reverse('networks')
    network_url = reverse('network', args=[1])

    def setUp(self):

        self.user = User.objects.create_user(username='user_one', password='pass')
        token_response = self.client.post(path=self.token_url,
                                          data={'username': 'user_one', 'password': 'pass'})
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        router_data = {
            'name': 'RTR_TEST_001',
            'management_ip': '10.0.0.5',
            'os_type': 'Linux',
        }

        network_data = {
            'name': 'TestNetwork',
            'vlan_tag': '100',
            'network_address': '172.16.0.0/12',
            'router': '1',
        }
        self.client.post(path=self.routers_url, data=router_data, format='json')
        self.client.post(path=self.networks_url, data=network_data, format='json')

    def test_network_get_success(self):
        response = self.client.get(self.network_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vlan_tag'], '100')

    def test_network_put_success(self):
        new_network_data = {
            'name': 'TestNetwork',
            'vlan_tag': '105',
            'network_address': '172.16.0.0/12',
            'router': '1',
        }
        response = self.client.put(path=self.network_url, data=new_network_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'TestNetwork', 'vlan_tag': '105',
                                         'network_address': '172.16.0.0/12', 'router': 1,
                                         'description': None})

    def test_network_put_invalid_input(self):
        new_network_data = {
            'name': 'TestNetwork',
            'vlan_tag': '105',
            'network_address': 'ip retea invalid',
            'router': '1',
        }
        response = self.client.put(path=self.network_url, data=new_network_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_network_delete_success(self):
        response = self.client.delete(path=self.network_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RouterListTest(APITestCase):
    """
    Testare RouterList View
    """

    token_url = reverse('token_obtain_pair')
    routers_url = reverse('routers')

    def setUp(self):

        self.user = User.objects.create_user(username='user_one', password='pass')
        token_response = self.client.post(path=self.token_url,
                                          data={'username': 'user_one', 'password': 'pass'})
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        router_data = {
            'name': 'RTR_TEST_001',
            'management_ip': '10.0.0.100',
            'os_type': 'Linux',
        }
        self.client.post(path=self.routers_url, data=router_data, format='json')

    def test_router_post_invalid_input(self):
        invalid_router_data = {
            'name': 'RTR_TEST_002',
            'management_ip': '10.0.0.5',
            'os_type': 'valoare invalida',
        }
        response = self.client.post(path=self.routers_url, data=invalid_router_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_router_post_success(self):
        router_data = {
            'name': 'RTR_TEST_002',
            'management_ip': '10.10.10.10',
            'os_type': 'Linux',
        }
        response = self.client.post(path=self.routers_url, data=router_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 2, 'name': 'RTR_TEST_002', 'management_ip': '10.10.10.10',
                                         'os_type': 'Linux', 'description': None})

    def test_router_get_list_success(self):
        response = self.client.get(path=self.routers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]),  {
            'id': 1,
            'name': 'RTR_TEST_001',
            'management_ip': '10.0.0.100',
            'os_type': 'Linux',
            'networks': [],
            'description': None
        })


class RouterDetailTest(APITestCase):
    """
    Testare RouterList View
    """

    token_url = reverse('token_obtain_pair')
    routers_url = reverse('routers')
    router_url = reverse('router', args=[1])

    def setUp(self):
        # In cazul folosirii autentificarii cu token standard(nu cu JWT):
        # self.user = User.objects.create_user(username='admin', password='pass')
        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.user = User.objects.create_user(username='user_one', password='pass')
        token_response = self.client.post(path=self.token_url,
                                          data={'username': 'user_one', 'password': 'pass'})
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        router_data = {
            'name': 'RTR_TEST_001',
            'management_ip': '10.0.0.100',
            'os_type': 'Linux',
        }
        self.client.post(path=self.routers_url, data=router_data, format='json')

    def test_router_get_success(self):
        response = self.client.get(path=self.router_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'RTR_TEST_001', 'management_ip': '10.0.0.100',
                                         'os_type': 'Linux', 'description': None, 'networks': []})

    def test_router_put_invalid_input(self):
        router_invalid_data = {
            'name': 'RTR_TEST_001',
            'management_ip': 'ip invalid',
            'os_type': 'Linux',
        }
        response = self.client.put(path=self.router_url, data=router_invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_router_put_success(self):
        router_invalid_data = {
            'name': 'RTR_TEST_001',
            'management_ip': '10.5.5.5',
            'os_type': 'Linux',
            'description': 'a network device'
        }
        response = self.client.put(path=self.router_url, data=router_invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'RTR_TEST_001', 'management_ip': '10.5.5.5',
                                         'os_type': 'Linux', 'description': 'a network device'})
