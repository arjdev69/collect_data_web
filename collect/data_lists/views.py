from django.shortcuts import render
from .forms import DataForm
from .crawler.web_crawler import *


# Create your views here.

def data_view(request):
  if request.method == 'POST':
    data_form = DataForm(request.POST)
    if data_form.is_valid():
      teste = data_form.cleaned_data['processes']
      it = get_crawler_list()
      print("---- --- ",it)
  else:
    data_form = DataForm()  # An unbound form
  return render(request, 'view_datas/view.html', {'datas': data_form})

