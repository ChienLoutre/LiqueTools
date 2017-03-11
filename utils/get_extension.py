def get_ext(obj):

	extractor = obj.split('.')
	ext = extractor[-1]
	extractor.pop(-1)
	obj = '.'.join(extractor)
	return obj, ext