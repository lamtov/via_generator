import numpy as np
import os
import difflib
cur_dir = os.getcwd()
via_dir = cur_dir+'/via_database'
database_dir = cur_dir+'/via_database/domain_database'
class Email():
    def __init__(self, *args, **kwargs):
        if kwargs.get('string_line'):
            self.string_line = kwargs.get('string_line')
            # print(string_line)
            self.name =self.string_line.split('@')[0]
            self.tail = self.string_line.split('@')[1]
            self.first_tail = self.tail.split('.')[0]
            self.second_tail = self.tail.split('.')[1]
        else:
            self.name = kwargs.get("name")
            self.tail =  kwargs.get("tail")
            self.first_tail = self.tail.split('.')[0]
            self.second_tail = self.tail.split('.')[1]
            self.string_line = self.name+"@"+self.tail


    def copy(self,name=None,tail=None,first_tail=None,second_tail=None):
        if name==None:
            name=self.name
        if tail == None:
            tail = self.tail
        if first_tail != None:
            tail = first_tail+'.'+tail.split('.')[1]
        if second_tail != None:
            tail = tail.split('.')[0]+'.'+second_tail
        return Email(name=name,tail=tail)

    def get_string_line(self):
        return self.string_line

class Via_obj():
    def __init__(self, string_line):
        self.string_line = string_line
        list_string=self.string_line.split('|')
        self.list_phones=[]
        self.public_emails=[]
        self.hidden_emails=[]
        self.list_predict=[]
        for string in list_string:
            string = string.replace('\n', "")
            if string[-1].isdigit():
                self.list_phones.append(string)
            else:
                # print('not string'+ string[-1])
                if '*' not in string:
                    # print(string)
                    self.public_emails.append(Email(string_line=string))
                else:
                    self.hidden_emails.append(Email(string_line=string))
    def print_via(self):
        rs=self.string_line.replace('\n','')
        for line in self.list_predict:
            rs=rs+'|'+line
        return rs



class FileVia():
    def __init__(self, database_txt):
        file1 = open(database_txt, encoding="utf8")
        Lines = file1.readlines()
        self.public_emails =set()
        self.public_tails=set()
        self.public_second_tails=set()
        self.list_Via=[]
        for line in Lines:
            via= Via_obj(line)
            self.list_Via.append(via)

            for mail in via.public_emails:

                self.public_emails.add(mail.string_line)
                self.public_tails.add(mail.tail)
                self.public_second_tails.add(mail.second_tail)
            for mail in via.hidden_emails:
                if '*' not in mail.second_tail:
                    self.public_second_tails.add(mail.second_tail)
        self.public_emails = sorted(self.public_emails)
        self.public_tails = sorted(self.public_tails)

        self.public_second_tails = sorted(self.public_second_tails)

    def save_to_file(self, data,name):
        output = open(via_dir + '/'+name+'.txt', 'w', encoding='utf-8')
        for line in data:
            line=line+'\n'
            output.writelines(line)
        output.close()

    def save(self):
        self.save_to_file(self.public_emails,'public_emails')
        self.save_to_file(self.public_tails, 'public_tails')
        self.save_to_file(self.public_second_tails, 'public_second_tails')


class Database():
    def __init__(self, database_txt):
        file1 = open(database_txt, encoding="utf8")
        Lines = file1.readlines()
        self.list_second_tail =set()
        self.list_tail= {}

        for line in Lines:
            line=line.replace('\n','')
            second_tail=line.split('.')[-1]

            first_tail = line[0:-1*(len(second_tail)+1)]
            if second_tail not in self.list_second_tail:
                self.list_second_tail.add(second_tail)
                self.list_tail[second_tail]=set()
            self.list_tail[second_tail].add(first_tail)

    def get_list_second_tail(self):
        return self.list_second_tail
    def get_list_first_tail(self,second_tail):
        return self.list_tail[second_tail]
    def get_list_domain(self,second_tail):
        list_domain=[]
        for tail in  self.list_tail[second_tail]:
            list_domain.append(tail+'.'+second_tail)
        return list_domain





# via_test=Via_obj('kerstinberndt@web.de|k***************4@t*******.de|***************4')
# print(via_test.public_emails)
# print(via_test.hidden_emails)
# print(via_test.list_phones)


#
def predic_second_tail(hidden_second_tail,database):
    try:
        list_public = database.get_list_second_tail()
        list_public_second_tail = []
        for tail in list_public:
            if len(tail)==len(hidden_second_tail):
                is_same=True
                for i in range(0, len(hidden_second_tail)):
                    if hidden_second_tail[i]!='*' and hidden_second_tail[i]!=tail[i]:
                        is_same=False
                if is_same:
                    list_public_second_tail.append(tail)
        return difflib.get_close_matches(hidden_second_tail,list_public_second_tail,n=3)
    except:
        return []

def predict_first_tail(hidden_first_tail,second_tail,database):
    try:
        list_public = database.get_list_first_tail(second_tail)
        list_public_first_tail = []
        for tail in list_public:
            if len(tail) == len(hidden_first_tail):
                is_same = True
                for i in range(0, len(hidden_first_tail)):
                    if hidden_first_tail[i] != '*' and hidden_first_tail[i] != tail[i]:
                        is_same = False
                if is_same:
                    list_public_first_tail.append(tail)
        return difflib.get_close_matches(hidden_first_tail, list_public_first_tail, n=5,cutoff=0)
    except:
        return []


def gen_from_char(x,size,first=False):
    try:
        list_out = []
        rs = ""
        for i in range(0, size):
            rs = rs + x
        list_out.append(rs)
        if first is False:
            if x.isdigit():
                rs = ""
                if int(x)-size+1 >0:
                    for i in range(0, size):
                        rs = str(int(x)-i)+rs
                    list_out.append(rs)
            else:
                rs = ""
                for i in range(0, size):
                    rs = str(chr(ord(x)-i)) + rs
                list_out.append(rs)
        else:
            if x.isdigit():
                rs = ""
                if int(x)+size-1 <10:
                    for i in range(0, size):
                        rs = rs+str(int(x)+i)
                    list_out.append(rs)
            else:
                rs = ""
                for i in range(0, size):
                    rs =rs + str(chr(ord(x)+i))
                list_out.append(rs)
        return list_out
    except:
        return []

def predict_name(hidden_name,list_public_name):
    char_1 = hidden_name[0]
    char_2 = hidden_name[-1]
    list_predict_name=[]
    for public_name in list_public_name:
        if public_name[0]==char_1:
            rs=""

            if len(public_name) == len(hidden_name):
                rs=rs+public_name[0:-1]
                for out in gen_from_char(char_2, len(hidden_name) - len(public_name) + 1):
                    list_predict_name.append(rs+out)
            elif len(public_name) < len(hidden_name):
                rs=rs+public_name
                for out in gen_from_char(char_2, len(hidden_name) - len(public_name) ):
                    list_predict_name.append(rs+out)
            else:
                list_predict_name.append(public_name[0:len(hidden_name)-1] + char_2)
        elif public_name[-1]==char_2:
            rs = ""
            if len(public_name) == len(hidden_name):
                rs = rs + public_name[1:]
                for out in gen_from_char(char_1, len(hidden_name) - len(public_name) + 1, first=True):
                    list_predict_name.append(out+rs  )
            elif len(public_name) < len(hidden_name):
                rs = rs + public_name
                for out in gen_from_char(char_1, len(hidden_name) - len(public_name) , first=True):
                    list_predict_name.append(out+rs  )
            else:
                list_predict_name.append(char_1+public_name[1:len(hidden_name)] )
        else:
            if len(public_name) <= len(hidden_name)-2:
                size_st = int((len(hidden_name)-len(public_name))/2)
                size_ed = len(hidden_name)-len(public_name)-size_st
                gen_st=gen_from_char(char_1,size_st, first=True)
                gen_ed=gen_from_char(char_2,size_ed)

                for st in gen_st:
                    for ed in gen_ed:
                        list_predict_name.append(st+public_name+ed)
        return list_predict_name




def predic(via,database):
    list_public_name=[]
    for mail in via.public_emails:
        list_public_name.append(mail.name)

    for mail in via.hidden_emails:
        list_name = predict_name(mail.name,list_public_name)
        list_second_tail=predic_second_tail(mail.second_tail,database)

        for second_tail in list_second_tail:
            list_first_tail = predict_first_tail(mail.first_tail,second_tail,database)
            for first_tail in list_first_tail:
                for name in list_name:
                    string_line =name+"@"+first_tail+'.'+second_tail
                    via.list_predict.append(string_line)


def excute_via(file,db,output_name):

    filevia1 = FileVia(  cur_dir+'/'+ file)
    filevia1.save()
    output = open(via_dir + '/' + 'output/' + file[:-4]+"_"+output_name, 'w', encoding='utf-8')
    for via in filevia1.list_Via[0:]:
        predic(via,db)
        line = via.print_via() + '\n'
        output.writelines(line)
    output.close()


if __name__ == "__main__":
    db_small = Database(database_dir+'/small_popular_domain_sort_size.txt')
    db_medium= Database(database_dir+'/medium_popular_domain_sort_size.txt')
    db_all = Database(database_dir+'/all_email_domain_sort_size.txt')
    # print(list(database.get_list_second_tail())[0:10])
    # print(list(database.get_list_first_tail('de')))
    # print(list(database.get_list_domain('de')))


    excute_via('Via.txt',db_small,'output_small.txt')
    excute_via('Via.txt', db_medium, 'output_medium.txt')
    excute_via('Via.txt', db_all, 'output_all.txt')