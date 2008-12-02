from django.http import HttpResponse
from django import forms

import hashlib

from upload.settings import UPLOAD_DIR, UPLOAD_TMPDIR
import os

db = {
	'next_id': 1,
	'data': {}
}

class UploadRequestForm(forms.Form):
	filename = forms.CharField()
	size = forms.IntegerField()
	sha1sum = forms.CharField()

class UploadHandlerForm(forms.Form):
	offset = forms.IntegerField()
	length = forms.IntegerField()
	sha1sum = forms.CharField()
	data = forms.FileField()

def upload_request(request):
	global db
	print "=== request"
	print db

	form = UploadRequestForm(request.POST)
	if form.is_valid():
		id = db['next_id']
		db['next_id'] += 1

		dir = os.path.join(UPLOAD_DIR, str(id))
		file = os.path.join(dir, form.cleaned_data['filename'])
		tmpdir = os.path.join(UPLOAD_TMPDIR, str(id))

		os.mkdir(dir)
		os.mkdir(tmpdir)

		data = {
			'size': form.cleaned_data['size'],
			'sha1sum': form.cleaned_data['sha1sum'],
			'filename': form.cleaned_data['filename'],
			'dir': dir,
			'file': file,
			'tmpdir': tmpdir,
			'uploaded': 0,
		}

		db['data'][id] = data

		response = HttpResponse("request ok. id=%d" % id)
		response['Content-Location'] = '/upload/%d/' % id

		return response

	else:

		return HttpResponse("invalid request")

def upload_chunk(request, id):
	global db
	print "=== chunk"
	print db

	id = int(id)

	data = db['data'].get(id, None)
	if data:
		
		form = UploadHandlerForm(request.POST, request.FILES)
		if form.is_valid():
			info = save_file(data, request.FILES['data'])

			offset = form.cleaned_data['offset']
			length = form.cleaned_data['length']
			sha1sum = form.cleaned_data['sha1sum']

			if length == info['size'] and sha1sum == info['sha1sum'] and data['uploaded'] == offset:
				append_file(data, info)

				if data['uploaded'] == data['size']:
					sha1sum = hashlib.sha1(open(data['file'], 'rb').read()).hexdigest()
					if sha1sum == data['sha1sum']:
						return HttpResponse("upload complete. checksum match")
					else:
						return HttpResponse("upload complete. checksum mismatch")

				else:
					return HttpResponse("OK")

			else:
				if length != info['size']:
					return HttpResponse("invalid chunk: size mismatch")
				elif sha1sum != info['sha1sum']:
					return HttpResponse("invalid chunk: checksum mismatch")
				else:
					return HttpResponse("invalid chunk: unexpected offset")

		else:
			return HttpResponse("invalid form")
	
	else:
		return HttpResponse("invalid id")

def save_file(data, file):
	fname = os.path.join(data['tmpdir'], "tmp")
	f = open(fname, "w")

	for chunk in file.chunks():
		f.write(chunk)
	
	f.close()

	info = {}
	info['file'] = fname
	info['size'] = os.path.getsize(fname)
	info['sha1sum'] = hashlib.sha1(open(fname, 'rb').read()).hexdigest()

	return info

def append_file(data, info):
	fd = open(data['file'], "a+")
	fc = open(info['file'], "r")

	fd.write(fc.read())

	fc.close()
	fd.close()

	data['uploaded'] += info['size']

