from django.shortcuts import render
from tripapp.models import Result
from tripapp.API.test_API import *


# Create your views here.
def group(request):
    global test_api
    # name = request.GET['name']
    # 如果是用POST的方式進來這個function
    if request.method == 'POST' and request.POST:
	# 如果是POST，就再產生一個變數接request.POST的東西，並將之與form.py裡面的格式結合
        keyword = request.POST.get("Search")
        result = test_api.call_search_API(keyword)
        if result == []:
            return render(request, 'back.html', locals())
        else:
            Days = range(len(result[0]))
            print(result)
            #print(keyword)
	    #search=Result.objects.create(Search=keyword)
	    #Result.objects.all()

            return render(request, 'show.html', locals())

test_api = API()
