import conf_html
from bs4 import BeautifulSoup
import re
import connectDB

def get_data(thtml):
    soup = BeautifulSoup(thtml,'html.parser')
    lsoup = soup.find_all('table', class_ = 'teams')
    one = []
    for item in lsoup:
        tmp = item.find_all('tr')
        team = []
        team.append(re.sub(r'.\d+.','',tmp[0].find_all('td')[0].text).strip().replace("'",'_'))
        team.append(tmp[0].find_all('td')[1].text)
        team.append(re.sub(r'.\d+.','',tmp[1].find_all('td')[0].text).strip().replace("'",'_'))
        team.append(tmp[1].find_all('td')[1].text)
        l = None
        for rt in item.find_all('a'):
            if rt.text == 'Final':
                l = 'https://www.sports-reference.com'+rt['href']
                break
        team.append(l)
        one.append(team)
    return one

#Структура целевой таблицы
# Create table llink(
# 	C1 varchar(MAX),
# 	S1 varchar(MAX),
# 	C2 varchar(MAX),
# 	S2 varchar(MAX),
# 	link varchar(MAX)
# )

def main():
    s = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month={month}&day={day}&year={year}'
    a = conf_html.generator_kw_dict(conf_html.nkw)
    a['year'] = 2020
    a['month'] = 12
    a['day'] = 13
    ghtml = conf_html.conf_html(s,a)
    DB = connectDB.WorkDB('RA19WIN10','NCAA_LL','sa','****')
    query = "Insert into NCAA_LL.dbo.llink Values('{0}','{1}','{2}','{3}','{4}')"
    while ghtml.is_next():
        print(ghtml.get_kw())
        for item in get_data(ghtml.get_html_text()):
            if len(item) == 0: continue
            #print(query.format(*item))
            DB.Commit_nr(query.format(*item))
        ghtml.next()
    
        


main()