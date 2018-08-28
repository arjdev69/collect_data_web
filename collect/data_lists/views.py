from django.shortcuts import render
from .forms import DataForm


# Create your views here.

def data_view(request):
    data_form = DataForm()
    print(data_form)
    return render(request, 'view_datas/view.html', {'datas': data_form})
