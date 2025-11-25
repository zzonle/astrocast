from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Location


class LocationAPITest(APITestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='pass123')
		self.user2 = User.objects.create_user(username='user2', password='pass456')

		self.client = APIClient()
		self.client.force_authenticate(user=self.user1)

	def test_list_locations_empty(self):
		resp = self.client.get('/api/weather/locations/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data, [])

	def test_create_location(self):
		payload = {
			'name': 'Casa',
			'city': 'Santiago',
			'country': 'Chile',
			'latitude': -33.45,
			'longitude': -70.67,
		}
		resp = self.client.post('/api/weather/locations/', payload, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertIn('id', resp.data)
		self.assertEqual(Location.objects.filter(user=self.user1).count(), 1)

	def test_retrieve_update_delete_location_and_forbidden(self):
		# crear location para user2 (otro usuario)
		loc2 = Location.objects.create(user=self.user2, name='Plaza', city='Valpo', country='Chile', latitude=-33.05, longitude=-71.62)

		# tratar de recuperar la de user2 -> debe 404 porque el queryset filtra por usuario
		resp = self.client.get(f'/api/weather/locations/{loc2.id}/')
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

		# crear una location propia
		loc = Location.objects.create(user=self.user1, name='Trabajo', city='Santiago', country='Chile', latitude=-33.44, longitude=-70.65)

		# recuperar
		resp = self.client.get(f'/api/weather/locations/{loc.id}/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data['name'], 'Trabajo')

		# actualizar
		resp = self.client.patch(f'/api/weather/locations/{loc.id}/', {'name': 'Oficina'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		loc.refresh_from_db()
		self.assertEqual(loc.name, 'Oficina')

		# eliminar
		resp = self.client.delete(f'/api/weather/locations/{loc.id}/')
		self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Location.objects.filter(pk=loc.id).exists())