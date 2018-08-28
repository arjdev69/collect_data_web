from django.shortcuts import render

# Create your views here.

def data_view(request):
    data = ["bruno","bruno1","bruno2","bruno3"]
    return render(request, 'view_datas/view.html', {'datas': data})
