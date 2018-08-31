from bs4 import BeautifulSoup
import urllib3
from more_itertools import unique_everseen
import re

def get_crawler_processes(page_formated):
  #page_formated = get_url(link)
  div_datas = page_formated.find_all("div", {"class": ""})
  for table_data in div_datas:
    span_datas = table_data.find_all("table", {"class": "secaoFormBody"})
    for span_data in span_datas:
      span_data_values = span_data.find_all("span", {"class": ""})
      list_datas = verify_space(span_data_values)
  spanArea = get_value_tag(span_data,"span","labelClass",'Área: ')
  list_datas.append(spanArea)
  return list_datas

def get_crawler_parts_processes(page_formated):
  div_datas = page_formated.find_all("table", {"id": "tablePartesPrincipais"})
  for dat in div_datas:
    datas = dat.find_all("td", {"align": "left"})
  lista = []
  for ld in datas:
    lista.append(ld.text.strip())    
  word_list = remove_word(lista,['Advogada:','RepreLeg:'])
  datas = refactor_word(lista,word_list)
  return datas

def get_crawler_move(page_formated):
  #page_formated = get_url(link)
  div_datas = page_formated.find_all("div", {"class": ""})
  for table_data in div_datas:
    span_datas = table_data.find_all("table", {"class": "secaoFormBody"})
    '''for span_data in span_datas:
      span_data_values = span_data.find_all("span", {"class": ""})
      list_datas = verify_space(span_data_values)'''
  spanArea = get_value_tag(span_data,"span","labelClass",'Área: ')
  list_datas.append(spanArea)
  return list_datas

def refactor_word(list_word,list_main):
  word_not_space = []
  for i in range(len(list_main)):
    list_word[i] = list_main[i].replace(' ','').split()
  for li in list_word:
    for i in range(len(li)):
      word_not_space.append(re.sub(r"(\w)([A-Z])", r"\1 \2", li[i]))
  return word_not_space

def remove_word(word_list,words):
  for i in range(len(word_list)):
    word_list[i] = word_list[i].replace(words[i],'')
  return word_list

def get_url(urlSite):
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  http = urllib3.PoolManager()
  page_data = http.request('GET', urlSite)
  page_formated = BeautifulSoup(page_data.data, "lxml")
  return page_formated

def verify_space(data_value):
  list_datas = []
  for span_data_value in data_value:
    if(span_data_value.text[0:3].isspace() != True):
      list_datas.append(span_data_value.text.strip())
  list_datas = list(unique_everseen(list_datas))
  return list_datas

def get_crawler_list(url):
	page_formated = get_url(url)
	datas_processes = get_crawler_processes(page_formated)
	datas_parts = get_crawler_parts_processes(page_formated)
  datas_move = get_crawler_move(page_formated)
	datas = set_dict(datas_move)
	return datas

def crawler_concatenate_link(first_link, second_link, third_link, processes):
  tjms_link_full = first_link + processes[:-5] + second_link + processes + third_link
  return_list = get_crawler_list(tjms_link_full)
  return return_list

def set_dict(data_list):
  data_dict = dict(zip(['Classe','Assunto','Distribuicao','Descricao','Controle','Juiz','Valor da Acao','Área'], data_list))
  return data_dict

def get_value_tag(html, tag, value_class, specific_content):
  data_values = html.find(tag, {"class": value_class})
  data_values = data_values.parent.text.strip()
  data_values = data_values.replace(specific_content, '')
  return data_values

#def return_list_data():

#print(get_url("https://www.tjms.jus.br/cpopg5/show.do?processo.codigo=01001ZB2W0000&processo.foro=1&uuidCaptcha=sajcaptcha_d1c087a198884723ab35d670baaf13f4"))	

#print("+",

crawler_concatenate_link("https://www.tjms.jus.br/cpopg5/search.do;jsessionid=F8E5227C1A100152C58411A02113AB4B.cpopg1?conversationId=&dadosConsulta.localPesquisa.cdLocal=1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado=", "&foroNumeroUnificado=0001&dadosConsulta.valorConsultaNuUnificado=", "&dadosConsulta.valorConsulta=&uuidCaptcha=sajcaptcha_d1c087a198884723ab35d670baaf13f4", "0821901-51.2018.8.12.0001")