from bs4 import BeautifulSoup
import urllib3
from more_itertools import unique_everseen
from collections import OrderedDict
from selenium import webdriver

def get_content_html(page_formated,tag,class_tag,value_class):
  div_datas = page_formated.find_all(tag, {class_tag: value_class})
  get_error = page_formated.find("td", {"id": "mensagemRetorno"})
  if get_error:
    div_datas = False
  return div_datas

def get_crawler_processes(page_formated,courts):
  div_datas = get_content_html(page_formated,"table","class","secaoFormBody")
  if div_datas:
    for table_data in div_datas:
      span_data_values = table_data.find_all("span", {"class": ""})
      list_datas = verify_space(span_data_values)
    spanArea = get_value_tag(table_data,"span","labelClass",'Área: ')
    list_datas.append(spanArea)
    key_list = define_key_list(div_datas,"Descricao: ",courts)
    key_list.append("Area:")
    return list_datas,key_list
  else:
    return False,False

def get_crawler_parts_processes(page_formated):
  div_datas = get_content_html(page_formated,"table","id","tablePartesPrincipais")
  if div_datas:
    datas = get_content_list(div_datas,"td","align","left")
    lista = []
    for ld in datas:
      lista.append(ld.text.strip())
    datas = get_content_list(div_datas,"td","align","right")
    key_list = set_key_list(datas,"span","class","mensagemExibindo","parts")
    return lista,key_list
  else:
    return False,False

def get_crawler_move(page_formated):
  div_datas = get_content_html(page_formated,"tbody","id","tabelaUltimasMovimentacoes")
  if div_datas:
    move_describe = []; move_date = []; move_list = dict()
    td_datas = get_content_list(div_datas,"td")
    move_date,move_describe = add_date_move_list(td_datas,move_date,move_describe)
    move_list = zip(move_date,move_describe)
    return move_list
  else:
    return False,False

def add_date_move_list(td_datas,move_date,move_describe):
  for i in range(len(td_datas)):
    if(td_datas[i].text.isspace() != True):
      if td_datas[i].text.strip()[0].isdigit():
        move_date.append(td_datas[i].text.strip())
      else:
        move_describe.append(td_datas[i].text.strip())
  return move_date,move_describe

def get_url(urlSite):
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  http = urllib3.PoolManager()
  try:
    page_data = http.request('GET', urlSite)
    page_formated = BeautifulSoup(page_data.data, "lxml")
    return page_formated
  except:
    print("Error URL")

def verify_space(data_value):
  list_datas = []
  for span_data_value in data_value:
    if(span_data_value.text.isspace() != True):
      list_datas.append(span_data_value.text.strip())
  list_datas = list(unique_everseen(list_datas))
  return list_datas

def get_crawler_list(courts,url):
	page_formated = get_url(url)
	datas_processes,keys_processes = get_crawler_processes(page_formated,courts)
	datas_parts,keys_parts = get_crawler_parts_processes(page_formated)
	datas_move = get_crawler_move(page_formated)
	if (datas_processes and datas_parts and datas_move):
		datas = set_dict([keys_processes,keys_parts],[datas_processes,datas_parts])
		return datas, datas_move
	else:
		return "Não existem informações disponíveis para os parâmetros informados.",""

def crawler_concatenate_link(courts,first_link, second_link, third_link, processes):
  processes = str(processes)
  tjms_link_full = first_link + processes[:-5] + second_link + processes + third_link
  return_list = get_crawler_list(courts,tjms_link_full)
  return return_list

def set_dict(keys,data_list):
  data_processes, alls_keys = put_key(keys)
  for i in range(len(alls_keys)):
    data_processes[alls_keys[i]] = dict(zip(data_processes[alls_keys[i]], data_list[i]))
  return data_processes

def put_key(keys):
  data_processes = OrderedDict()
  data_processes['Dados do Processo']  = keys[0]
  data_processes['Partes do Processo'] = keys[1]#['Autora','Réu']

  keys = ['Dados do Processo','Partes do Processo']
  return data_processes,keys

def get_value_tag(html, tag, value_class, specific_content):
  data_values = html.find(tag, {"class": value_class})
  data_values = data_values.parent.text.strip()
  data_values = data_values.replace(specific_content, '')
  return data_values

def get_content_list(div_datas,tag, tag_class="False", value_class="False"):
  for table_data in div_datas:
    if ((tag_class != "False") and (value_class != "False")):
      td_datas = table_data.find_all(tag, {tag_class: value_class})
    else:
      td_datas = table_data.find_all(tag)
  return td_datas

def define_key_list(div_datas,key_name,courts):
  key_list = set_key_list(div_datas,"label","class","labelClass","datas")
  if courts == "SP":
    key_list[4:5] = [key_list[4],key_name]
  else:
    key_list[3:4] = [key_list[4],key_name]
  return key_list

def set_key_list(div_datas,tag,class_tag,value_class,type_processes):
  if type_processes == "parts":
    datas = div_datas
  else:
    datas = get_content_list(div_datas,tag,class_tag,value_class)

  for i in range(len(datas)):
    datas[i] = datas[i].text.strip()
  return datas