def dict_differs_from_spec(expected, actual):
	""" 
	Returns whether all props in "expected" are matching in "actual" 
	Note that "actual" could contain extra properties not in expected
	"""
	for k, v in enumerate(expected.items()):
		if not k in actual:
			return False
		if actual[k] != v:
			return False
	return True
