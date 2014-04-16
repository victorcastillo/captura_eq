
def documento(request):
	from .models import Documento
	documento = None
	if request.session.has_key('documento_id'):
		try:
			documento = Documento.objects.get(id=int(request.session['documento_id']))
		except:
			del request.session['documento_id']
			pass
	return {'documento': documento}