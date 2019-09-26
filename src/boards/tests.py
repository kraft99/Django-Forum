from django.urls import reverse,resolve
from django.test import TestCase

from .views import board_index,board_topics
from .models import Board


# class HomeTests(TestCase):
# 	"""
# 	Test - Board Home View
# 	"""
# 	def test_home_view_status_code(self):
# 		"""
# 		Test - Home Page Status Code
# 		"""
# 		url = reverse('boards')
# 		response = self.client.get(url)
# 		self.assertEquals(response.status_code,200) #200 == 200 (success ) or 403 != 200 (Failure or Error)


# 	def test_home_url_resolve_board_index_view(self):
# 		"""
# 		Test - check view of home route
# 		ie. url = 'http://127.0.0.1:8000/boards/' return by board_index view ?
# 		"""
# 		view = resolve('boards')
# 		self.assertEquals(view.func,board_index)



class BoardTopic(TestCase):
		"""
		Test - BoardTopic View
		"""
		def setUp(self):
			Board.objects.create(name="Forum",description="Jxt a Forum")


		def test_board_topic_view_success_statuc_code(self):
			# Test - Success code 200 of Board Topic
			url = reverse('board_topics',kwargs={'pk':'fd4c2d60-3868-4501-a30e-89d2bcae431f'})
			response = self.client.get(url)
			self.assertEquals(response.status_code,200)


		def test_board_view_not_found_status_code(self):
			# Test - NotFound Error Checking for pk(beyond pk's in DB)
			url = reverse('board_topics',kwargs={'pk':'fd4c2d60-3868-4501-a30e-89d2bcae431f-wuywu'})#pk:267
			response = self.client.get(url)
			self.assertEquals(response.status_code,404)


	    def test_board_topics_url_resolves_board_topics_view(self):
	    	# Test - check view or controller of board detail route
	        view = resolve('/boards/fd4c2d60-3868-4501-a30e-89d2bcae431f')
	        self.assertEquals(view.func, board_topics) 