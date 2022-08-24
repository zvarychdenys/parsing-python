import numpy as np
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
}

url = "https://signal.nfx.com/investors/garrett-camp"
req = requests.get(url,headers=headers)
src = req.text


soup = BeautifulSoup(src, 'html.parser')


person_name = soup.find('h1', class_ = 'f3 f1-ns mv1').text.split("(")[0]

info_person_dict = {}
info_person_dict['Name'] = person_name

number_invested_companies = soup.find_all("span", class_ = 'lh-solid')
for item in number_invested_companies[-3]:
    number_companies = int(item.text)
    if number_companies > 8:
        number_companies = 8
    
    info_person_dict['Investmets'] = number_companies

invested_companies = soup.find_all("td", class_ = 'with-coinvestors')
companies_info = []
for companies in invested_companies:
    companies_name = companies.text
    companies_info.append(companies_name)


companies_arrays = np.array_split(companies_info,number_companies) # companies_arrays - zawiera dane do firmy

companies_NAME = []
companies_STAGEDATEROUND_SIZE = []
companies_TOTAL_RAISED = []

for item in companies_arrays:
    companies_NAME.append(item[0])
    companies_STAGEDATEROUND_SIZE.append(item[1])
    companies_TOTAL_RAISED.append(item[2])


info_person_dict['Company'] = companies_NAME
info_person_dict['Stage Data ROUND SIZE'] = companies_STAGEDATEROUND_SIZE
info_person_dict['Total raised'] = companies_TOTAL_RAISED
 

with open('3_info.json','w') as file:
    json.dump(info_person_dict, file, indent=4)
