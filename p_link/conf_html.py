from requests import get

class plist(object):#класс для контроля диапазона ключевых слов(хранит в себе приоритет ключевого слова и диапазон в котором ключевое слово может принимать значение)

    def __init__(self,priority,val,per = False, chi = 1, ring = True):
        if type(priority) is not int or priority < 0: raise Exception('ERROR_TYPE(PLIST):prioriyety is not INT or <0')
        self._p = priority #приоритет ключевого слова принемает int >= 0
        if type(val) is not list: raise Exception('ERROR_TYPE(PLIST):value is not LIST')
        if len(val) == 0: raise Exception('ERROR_DATA(PLIST):value is empty')
        self._v = val #диапазон который может принемать ключ( это либо набор значений в виде списка, либо числа от a до b[a,b])
        self._index = self._v[0] #текущее значение ключевого слова
        if type(per) is not bool: raise Exception('ERROR_TYPE(PLIST):per is not BOOL')
        if not per and len(val) != 2: raise Exception('ERROR_DATA(PLIST):type not per and count vel not two')
        elif not per and val[0]>=val[1]: raise Exception('ERROR_DATA(PLIST):bad interval')
        self._t = per #ключевое слово перебирается из списка или изменяется в диапазоне
        if type(chi) is not int: raise Exception('ERROR_TYPE(PLIST):chi is not INT')
        self._i = chi #если перебирается в допозоне на сколько плюсовать
        if type(ring) is not bool: raise Exception('ERROR_TYPE(PLIST):ring is not BOOL')
        self._r = ring #закольцован ли список
        self._next = True #возможно ли выполнить опирацию next
        self.__is_next() 

    def set_val(self,val=None,n_val=None): #задание определенного значения из диапазона(если значение вне диапазона ошибка)
        if val is not None and n_val is None:
            if self._t and val in self._v: self._index=val
            elif not self._t and val >= self._v[0] and val <= self._v[1]: self._index=val
            else: raise Exception('ERROR_DATA(PLIST_SET_VAL):val is not list_val')
            self.__is_next()
        elif n_val is not None and val is None:
            if type(n_val) is not int or not self._t or len(self._v)<= n_val:
                raise Exception('ERROR_DATA_OR_TYPE(PLIST_SET_VAL):n_val is not type INT or type not per or count list val <= n_val')
            self._index = self._v[n_val]
            self.__is_next()
        else: raise Exception('ERROR_TYPE(PLIST_SET_VAL):val and n_val is NONE or not NONE')

    def __is_next(self): #задает значение вниутренней переменной next
        if self._next:
            if self._t:
                if self._v.index(self._index)+1 == len(self._v):
                    self._next = False
            elif self._index+self._i > self._v[1]:
                self._next = False

    def next_val(self): #передвижение указателя на след. элимент если невозможно вернет False
        if not self._next: return False
        if self._t:
            i = self._v.index(self._index)+1
            self._index = self._v[i]
            self.__is_next()
            return True
        i = self._index+self._i
        self._index = i
        self.__is_next()
        return True

    def next_val_ring(self):#Передвижение указателя в начало
        if not self._next and not self._r: return False
        if not self._r: return self.next_val()
        self._index = self._v[0]
        self._next = True
        self.__is_next()
        return True

    #функции полученя показателей
    def get_prioritety(self): return self._p

    def get_val(self): return self._index

    def __repr__(self): return str(self._index)

    def __str__(self): return str(self._index)

    def get_list_val(self): return self._v

    def is_per(self): return self._t

    def is_ring(self): return self._r

    def is_next(self): return self._next

    def set_list_val(self,val,per = False):#присвоение нового диапазона
        if type(val) is not list: raise Exception('ERROR_TYPE(PLIST_SET_LIST_VAL):value is not LIST')
        if val.count() == 0: raise Exception('ERROR_DATA(PLIST_SET_LIST_VAL):value is empty')
        if type(per) is not bool: raise Exception('ERROR_TYPE(PLIST_SET_LIST_VAL):per is not BOOL')
        if not per and len(val) != 2: raise Exception('ERROR_DATA(PLIST_SET_LIST_VAL):type not per and count vel not two')
        elif not per and val[0]>=val[1]: raise Exception('ERROR_DATA(PLIST):bad interval')
        self._v = val
        self._index = self._v[0]
        self._t = per
        self._next = True
    
    def set_ring(self,ring):#изменеие кольцевого статуса 
        if type(ring) is not bool: raise Exception('ERROR_TYPE(PLIST_SET_RING):ring is not BOOL')
        self._r = ring

    def set_upper(self,chi):#измение значения увелечения
        if type(chi) is not int: raise Exception('ERROR_TYPE(PLIST_SET_UPPER):chi is not INT')
        self._i = chi

class kw_status(object):#класс хранящий список ключевых слов и позволяющий переходить к следующе комбинации ключевых слов

    def __init__(self):
        self._kw = {}
        self._p = []

    def __setitem__(self,key,value): #Задание начальных значений или ручной ввод значений ключевых слов
        if type(key) is not str: raise Exception('ERROR_TYPE(KW_STATUS_[]):key is not STR')
        if key not in self._kw.keys():raise Exception('ERROR_DATA(KW_STATUS_[]):key dont found')
        self._kw[key].set_val(value)

    def __getitem__(self,key): #получение тек знач по ключевому слову
        if type(key) is not str: raise Exception('ERROR_TYPE(KW_STATUS_[]):key is not STR')
        if key not in self._kw.keys():raise Exception('ERROR_DATA(KW_STATUS_[]):key dont found')
        return self._kw[key]

    def __sort__(self):#сортировка по приоритету для операции next
        tmp = {}
        for i in self._kw.keys():
            tmp[self._kw[i].get_prioritety()]=i
        self._p = []
        for i in sorted(tmp.keys()):
            self._p.append(tmp[i])

    def add(self,kword,pl):#добавление пары ключ:диапазонбпроиритет
        if type(kword) is not str: raise Exception('ERROR_TYPE(KW_STATUS_ADD):kword is not STR')
        if type(pl) is not plist: raise Exception('ERROR_TYPE(KW_STATUS_ADD):pl is not PLIST')
        if kword in self._kw.keys(): raise Exception('ERROR_DATA(KW_STATUS_ADD):kword not uniq')
        for i in self._kw.keys():
            if pl.get_prioritety() == self._kw[i].get_prioritety(): raise Exception('ERROR_DATA(KW_STATUS_ADD):kword with tek. prioritety exist')
        self._kw[kword]=pl
        self.__sort__()

    def del_kw(self,kw):#удаление ключевого слова
        if type(kw) is not str: raise Exception('ERROR_TYPE(KW_STATUS_DEL_KW):kw is not STR')
        if kw not in self._kw.keys(): raise Exception('ERROR_DATA(KW_STATUS_DEL_KW):kword dont found')
        self._kw.pop(kw)
    
    def __null_ring__(self,i):#вспомогательная функция для next(вызывает обнуления у ключевых слов с приоритетом i+)
        for j in range(i,len(self._p)):
            self._kw[self._p[j]].next_val_ring()

    def __next_prior__(self,i):#вспомогательная функция для next(смещает значения в диапазону у следующего по приоритету ключевого слова)
        if i == 0: return False
        if not self._kw[self._p[i-1]].is_next():
            self.__null_ring__(i)
            return self.__next_prior__(i-1)
        self._kw[self._p[i-1]].next_val()
        self.__null_ring__(i)
        return True

    def next(self):#смещает значение в диапазоне ключевых слов
        i = len(self._p)-1
        if self._kw[self._p[i]].is_next():
            return self._kw[self._p[i]].next_val()
        return self.__next_prior__(i)

    def get_kw(self):#возращает ключевой словарь вида {ключ:тек_знач_ключа}
        tmp = {}
        for i in self._kw.keys():
            tmp[i]=self._kw[i]
        return tmp

class conf_html(object):#класс для получения html получает шаблон ссылки и класс перебора состояний ключевых слов

    def __init__(self,shablon,kwparams):
        if type(shablon) is not str: raise Exception('ERROR_TYPE(CONF_HTML):shablon not STR')
        if type(kwparams) is not kw_status: raise Exception('ERROR_TYPE(CONF_HTML):kwparams not kw_status')
        self._s = shablon #шаблон
        self._kw = kwparams #класс ключевых слов
        self.html = None #суда будет писвтся html
        self._next = True #статус можно ли получить следующую страницу
        self._htmls = 0 #статус get запроса
    
    def __repr__(self): #получает html если удается получить
        if not self._next: #смысл проверки что не удалось получить следующую комбинацию ключевых слов и страницу можно не запрашивать
            self._htmls = 0
            return 'ERROR_next'
        try:
            self.html = get(url = self._s.format(**self._kw.get_kw()))
        except:
            return 'ERROR_get'
        self._htmls = self.html.status_code
        if self._htmls != 200: return 'ERROR_status'
        return str(self.html.text)
    
    def __str__(self):
        return self.__repr__()

    def next(self):#получение следующей комбинации ключевых слов
        self._next = self._kw.next()
        return self._next
    
    def is_next(self): return self._next

    def is_status(self):
        if self._htmls != 200: return False
        return True

    def set_kw(self,kw):# назначение новых ключевых слов
        if type(kw) is not kw_status: raise Exception('ERROR_TYPE(CONF_HTML_SET_KW):kw not kw_status')
        self._kw = kw
        self.html = None
        self._next = True
        self._htmls = True

    def get_kw(self): return self._kw.get_kw()
    
def generator_kw_dict(kw_s):#Гениратор для класа поддержки ключевых слов
    if type(kw_s) is not dict: raise Exception('ERROR_TYPE(GKD):kw_s is not DICT')
    for item in kw_s.keys():
        if type(item) is not str: raise Exception('ERROR_DATA(GKD):kw is not STR')
        if type(kw_s[item]) is not list: raise Exception('ERROR_DATA(GKD):kw_s is two el. not list')
        if len(kw_s[item]) != 2: raise Exception('ERROR_DATA(GKD):kw_s el is not two')
        if type(kw_s[item][0]) is not int or kw_s[item][0] < 0: raise Exception('ERROR_DATA(GKD):kw_s one el. is not INT or < 0')
        if type(kw_s[item][1]) is not list: raise Exception('ERROR_DATA(GKD):kw_s is two el. is not list')
    tmp_kw = kw_status()
    for item in kw_s.keys():
        tmp_kw.add(item,plist(kw_s[item][0],kw_s[item][1]))
    return tmp_kw
#Шаблон для гениратора
nkw = {
    'year':[0,[2010,2020]],
    'month':[1,[1,12]],
    'day':[2,[1,31]]
}





def main():
    s = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month={month}&day={day}&year={year}'
    # a = kw_status()
    # a.add('month',plist(2,[1,12]))
    # a.add('year',plist(1,[2010,2020]))
    # a.add('day',plist(3,[1,31]))
    a = generator_kw_dict(nkw)
    a['month'] = 11
    a['day'] = 8
    a['year'] = 2020
    
    h = conf_html(s,a)

    while h.is_next():
        # with open('output.txt','w',encoding='UTF-8') as k:
        #     k.write(str(h))
        print(h.is_status())
        print(h.get_kw())
        h.next()

    
    


if __name__ == '__main__':
    main()