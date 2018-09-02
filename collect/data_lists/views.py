from django.shortcuts import render
from .forms import DataForm
from .crawler.web_crawler import *


# Create your views here.

def data_view(request):
  final_data = dict()
  move = dict()
  if request.method == 'POST':
    data_form = DataForm(request.POST)
    if data_form.is_valid():
      number_processes = data_form.cleaned_data['processes']
      courts = data_form.cleaned_data['courts']
      if ((number_processes[0:5].isdigit()) and (len(number_processes)==25)):
        final_data, move = get_web_crawler(courts,number_processes)
        if final_data == "Não existem informações disponíveis para os parâmetros informados.":
          return render(request, 'view_datas/view.html', {'form': data_form, 'ErrorMain':"Não existem informações disponíveis para os parâmetros informados."})
      else:
        return render(request, 'view_datas/view.html', {'form': data_form, 'ErrorMain':"Por Favor digite o numero do processo corretamente. \n Ex: '0821901-51.2018.8.12.0001'"})
  else:
    data_form = DataForm()  # An unbound form
  return render(request, 'view_datas/view.html', {'form': data_form, 'final_data':final_data,'move':move})

def get_web_crawler(courts,number):
  if courts == "SP":
    return crawler_concatenate_link("https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&dadosConsulta.localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado=", "&foroNumeroUnificado="+number[-4:]+"&dadosConsulta.valorConsultaNuUnificado=", "&dadosConsulta.valorConsulta=&uuidCaptcha=", number)
  else:
    return crawler_concatenate_link("https://www.tjms.jus.br/cpopg5/search.do;jsessionid=F8E5227C1A100152C58411A02113AB4B.cpopg1?conversationId=&dadosConsulta.localPesquisa.cdLocal=1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado=", "&foroNumeroUnificado="+number[-4:]+"&dadosConsulta.valorConsultaNuUnificado=", "&dadosConsulta.valorConsulta=&uuidCaptcha=sajcaptcha_d1c087a198884723ab35d670baaf13f4", number)