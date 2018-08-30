from bs4 import BeautifulSoup
import urllib3
import re


def crawler_data(link):
  page_formated = get_url(link)
  div_datas = page_formated.find_all("div", {"class": ""})
  for table_data in div_datas:
    span_datas = table_data.find_all("table", {"class": "secaoFormBody"})
    for span_data in span_datas:
      span_data_values = span_data.find_all("span", {"class": ""})
      list_datas = verify_space(span_data_values)
  return list_datas

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
  return list_datas

def remove_duplicate(duplicate):
  final_list = []
  for num in duplicate:
    if num not in final_list:
      final_list.append(num)
  return final_list

def get_crawler_list():
  datas = crawler_data('https://www.tjms.jus.br/cpopg5/show.do?processo.codigo=01001ZB2W0000&processo.foro=1&uuidCaptcha=sajcaptcha_d1c087a198884723ab35d670baaf13f4')
  data_dict = remove_duplicate(datas)
  return data_dict