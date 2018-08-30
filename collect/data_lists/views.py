from django.shortcuts import render
from .forms import DataForm
from .crawler.web_crawler import *


# Create your views here.

def data_view(request):
  final_data = dict()
  if request.method == 'POST':
    data_form = DataForm(request.POST)
    if data_form.is_valid():
      teste = data_form.cleaned_data['processes']
      final_data = get_web_crawler()
      print("---- --- ",final_data)
  else:
    data_form = DataForm()  # An unbound form
  return render(request, 'view_datas/view.html', {'form': data_form, 'final_data':final_data})

def get_web_crawler():
  return crawler_concatenate_link("https://www.tjms.jus.br/cpopg5/search.do;jsessionid=F8E5227C1A100152C58411A02113AB4B.cpopg1?conversationId=&dadosConsulta.localPesquisa.cdLocal=1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado=", "&foroNumeroUnificado=0001&dadosConsulta.valorConsultaNuUnificado=", "&dadosConsulta.valorConsulta=&uuidCaptcha=sajcaptcha_d1c087a198884723ab35d670baaf13f4", "0821901-51.2018.8.12.0001")