from django.shortcuts import render
from tripapp.models import Result

# Create your views here.
def index(request):

	# print(locals())
	return render(request, 'index.html', locals())