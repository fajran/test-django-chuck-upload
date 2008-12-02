
from django.http import HttpResponse

def request(req):
	return HttpResponse("""<html><body>
<form method="post" action="/upload/">
	<p>size: <input type="text" name="size"/></p>
	<p>sha1sum: <input type="text" name="sha1sum"/></p>
	<p>filename: <input type="text" name="filename"/></p>
	<p><input type="submit" value="submit"/></p>
</form>
</body></html>""")

def chunk(req, id):
	return HttpResponse("""<html><body>
<form method="post" action="/upload/%d/" enctype="multipart/form-data">
	<p>offset: <input type="text" name="offset"/></p>
	<p>length: <input type="text" name="length"/></p>
	<p>sha1sum: <input type="text" name="sha1sum"/></p>
	<p>file: <input type="file" name="data"/></p>
	<p><input type="submit" value="submit"/></p>
</form>
</body></html>""" % int(id))
