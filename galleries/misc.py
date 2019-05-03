import os

from loghomecrew import settings


def get_upload_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s%s.%s" % ('img', instance.pk, ext)

	return '/'.join(instance.location.state, instance.date_build, filename)