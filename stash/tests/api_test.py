import os
import unittest
from .. import stash
from testutils import dict_differs_from_spec
import tempfile
import simplejson as json

class ApiTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, self.tmp_path = tempfile.mkstemp()
		sqlite_tmp_path = 'sqlite:///' + self.tmp_path

		stash.app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_tmp_path
		stash.app.config['TESTING'] = True

		self.app = stash.app.test_client()
		self.expected_results = {} 
		with stash.app.app_context():
			# Bootstrap models with new database
			from stash.core import db

			# Create tables
			db.create_all()

			# Manually read in data
			with open('data/db_items.json', 'r') as f:
				json_data = json.loads(f.read())
				for name, items in json_data.items():
					model_config = stash.app.config['API_MODELS'][name]
					MClass = model_config['model_class']
					for item in items:
						inst = MClass(**item)
						db.session.add(inst)
					self.expected_results[name] = {
						'num_results': len(items),
						'objects': items
					}
				db.session.commit() 

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(self.tmp_path)

	# given an endpoint url and a field to sort by, finds whether
	# the data from the api matches the test data
	def shared_endpoint_testing(self, url_endpoint, name, sort_by_field):
		res = self.app.get(url_endpoint)
		results = json.loads(res.data)
		assert 'objects' in results
		assert 'num_results' in results
		expected = self.expected_results[name]

		# sort by name so we can compare easily
		sort_fn = lambda x: x[sort_by_field]
		results['objects'] = sorted(results['objects'], key=sort_fn)
		expected['objects'] = sorted(expected['objects'], key=sort_fn)

		assert results['num_results'] == expected['num_results']
		for actual in results['objects']:
			assert not dict_differs_from_spec(expected, actual)

	def test_user_endpoint(self):
		self.shared_endpoint_testing('/api/v1/user', 'user', 'username')

	def test_tag_endpoint(self):
		self.shared_endpoint_testing('/api/v1/tag', 'tag', 'name')

	def test_images_endpoint(self):
		self.shared_endpoint_testing('/api/v1/image', 'image', 'name')

if __name__ == '__main__':
	unittest.main()
