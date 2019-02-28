# encoding=utf-8

import hashlib
import requests
import re,os
import shutil
from bs4 import BeautifulSoup
import time
from db import create_conn

md5 = hashlib.md5()
courses = {}
code_table = {}
translate = {
    'grade':'年級',
    'class_id':'編號' ,
    'class_num':'班號' ,
    'class_name':'科目名稱' ,
    'teacher':'任課教授' ,
    'credit':'學分' ,
    'category':'選必' ,
    'time':'上課時間' ,
    'location':'上課地點' ,
    'limit_people':'限制人數' ,
    'outline':'課程大綱' ,
    'note':'備註' ,
    'direction':'向度',
    'field' : '領域'
}

def isUpdate(index,html):
    # print(html)
    m = hashlib.md5(html)
    # m.update(html)
    md5 = m.hexdigest()
    sql = "SELECT `hash_value` FROM `course_hash` WHERE `department_name` = '{}'"
    cursor.execute(sql.format(index))
    row = cursor.fetchone()
    # print(row[0])
    # for key,value in enumerate(hash_value):
        # print(key,value)
    # hash_value = row[0]
    if row == None:
        sql = "INSERT INTO `course_hash` (`department_name`,`hash_value`,`modify_date`) VALUES ('{}','{}',CURDATE())"
        # sql = "INSERT INTO `course_hash` (`department_name`,`hash_value`) VALUES ({},{})"
        # print(sql.format(str(index),str(md5)))
        cursor.execute(sql.format(index,md5))
        conn.commit()
        return True

    hash_value = row[0]

    if row[0] != md5:
        sql = "UPDATE `course_hash` SET `hash_value` = '{}',`modify_date` = CURDATE() WhERE `department_name` = '{}'"
        cursor.execute(sql.format(md5,index))
        conn.commit()
        return True
    elif row[0] == md5:
        print(index + " is not need to update")
        return False
    else:
        exit("Have some errors judge the date whether update")


def getdata(url, index,courses):
    # print(courses)
    html = requests.get(url)
    html.encoding = 'utf-8'
    if isUpdate(index,html.text.encode("utf-8")) == False:
        return
    sp = BeautifulSoup(html.text,'lxml')
    table = sp.select('table')
    trs = table[0].select('tr')
    course = []
    # print(index[-1]=='6')
    if index == 'I001':
        for tr in trs[1:]:
            tds = tr.select('td')
            tmp = {
                    # 'field': tds[0].text,
                    'direction': tds[1].text,
                    'class_id': tds[2].text,
                    'class_num': tds[3].text,
                    'class_name': tds[4].text,
                    'teacher': tds[5].text,
                    'credit': tds[7].text,
                    'category': tds[8].text,
                    'time': tds[9].text,
                    'location': tds[10].text,
                    'limit_people': tds[11].text,
                    'outline': tds[12].select('a')[0].get('href'),
                    'note': tds[13].text,
                   }

            course.append(tmp)

    elif (index[-1] == '6' and index != '7306') or index == '4508':
        for tr in trs[1:]:
            tds = tr.select('td')
            tmp = { 'grade': tds[0].text,
                    'class_id': tds[1].text,
                    'class_num': tds[2].text,
                    'class_name': tds[3].text,
                    'teacher': tds[4].text,
                    'credit': tds[6].text,
                    'category': tds[7].text,
                    'time': tds[8].text,
                    'location': tds[9].text,
                    'limit_people': tds[10].text,
                    'outline': tds[12].select('a')[0].get('href'),
                    'note': tds[13].text,
                    # 'direction':''
                    }
            course.append(tmp)

    else:
        for tr in trs[1:]:
            tds = tr.select('td')
            # print(tds[11].select('a')[0].get('href'), end='\n-----------------\n')
            tmp = {'grade': tds[0].text,
                   'class_id': tds[1].text,
                   'class_num': tds[2].text,
                   'class_name': tds[3].text,
                   'teacher': tds[4].text,
                   'credit': tds[6].text,
                   'category': tds[7].text,
                   'time': tds[8].text,
                   'location': tds[9].text,
                   'limit_people': tds[10].text,
                   'outline': tds[11].select('a')[0].get('href'),
                   'note': tds[12].text,
                #    'direction': ''
                   }
            course.append(tmp)

    courses[index] = tmp

    fname = "./courses_data/"+index+".json"
    dname = './old_courses_data/'+ index + '/'

    if not os.path.isdir(dname):
        os.mkdir(dname)
    if os.path.exists(fname):
        shutil.copyfile(fname, dname + index + '_' + str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')
    with open(fname,'w',encoding='utf-8') as f:
        import json
        json.dump(course,f);

def crawler():
    global courses
    # courses = {}
    url = 'https://kiki.ccu.edu.tw/~ccmisp06/Course/'
    html = requests.get(url)
    # print(html.text)
    html.encoding = 'utf-8'
    # if isUpdate(html.text.encode('utf-8-sig')) == False :
    #     return False
    sp = BeautifulSoup(html.text,'lxml')

    table = sp.select('table')
    trs = table[1].select('tr')
    tds = trs[1].select('td')
    for td in tds[0:-1]:
        links = td.select('a')
        for link in links:
            href = link.get('href')
            text = link.text
            # get the table of departments code
            code_table[text] = href[0:4]
            code_table[href[0:4]] = text

            # print(text)
            print(href)
            if not href[0:4] in courses:
                courses[href[0:4]]=[]
            getdata(os.path.join(url, href), href[0:4], courses)
        print('--------------------------------------')
    return True
    # print(courses)

def print_course(id,course):
    print('\n-----------------------------------')
    print('系所: '+code_table[id])
    for key,value in course.items():
        print(translate[key]+': '+value)
def find_course_by_class_name(name):
    # print(courses)
    for id, department in courses.items():
        for course in department:
            if course['class_name'].find(name) != -1:
                print_course(id,course)
                input()
def find_course_by_teacher_name(name):
    # print(courses)
    for id, department in courses.items():
        for course in department:
            if course['teacher'].find(name) != -1:
                print_course(id,course)
                input()
def find_course_by_class_id(id):
    # print(courses)
    for id, department in courses.items():
        for course in department:
            if course['class_id'] == id:
                print_course(id,course)
                input()

def moveOldFile():
    # move file(courses.data) before store data to courses.data
    if os.path.exists('courses.json'):
        if not os.path.isdir("./old_courses_data/fullcourse"):
            os.mkdir("./old_courses_data/fullcourse")
        shutil.copyfile('courses.json','./old_courses_data/fullcourse/'+str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')
        # shutil.copyfile('courses.json','./courses_data/'+str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')

    # move file(code_table.json) before store data to code_table.json
    if os.path.exists('code_table.json'):
        shutil.copyfile('code_table.json','./code_table_data/'+str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')

# create a connection
conn = create_conn()
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS `course_hash` (department_id INTEGER(99) PRIMARY KEY NOT NULL AUTO_INCREMENT,hash_value VARCHAR(255) NOT NULL,department_name VARCHAR(255) NOT NULL,modify_date DATE NOT NULL) CHARACTER SET = utf8 COLLATE = utf8_unicode_ci')
conn.commit()
# conn.close()

# exit()
# create the dir for sroring data
if not os.path.isdir("code_table_data"):
    os.mkdir("code_table_data")

if not os.path.isdir("courses_data"):
    os.mkdir("courses_data")

if not os.path.isdir("old_courses_data"):
    os.mkdir("old_courses_data")

# if exists the old file we can use them.
if os.path.exists('courses.json'):
    with open('courses.json', "r", encoding='utf-8') as f:
        import json
        courses = json.load(f)
if os.path.exists('code_table.json'):
    with open('code_table.json', "r", encoding='utf-8') as f:
        import json
        code_table = json.load(f)
if crawler() == True:
    print("Finish crawler")
    # print(courses)
    moveOldFile()
else:
    print("The website is not update")
#print(code_table)
# print(courses)
#print(code_table)

# save the file after crawler
with open('courses.json','w',encoding='utf-8') as f:
    import json
    json.dump(courses,f);
with open('code_table.json', 'w', encoding='utf-8') as f:
    import json
    json.dump(code_table, f)

# cmdline search
# while True:
#     print('\n----------------------')
#     print('1. 查找課程by課名')
#     print('2. 查找課程by老師')
#     print('3. 查找課程by課程代碼')
#     print('0. 離開')
#     print('----------------------')
#     ch = input("選項: ")
#     if ch == '1':
#         name = input('請輸入課程名稱: ')
#         find_course_by_class_name(name.strip())
#     elif ch == '2':
#         name = input('請輸入老師名稱: ')
#         find_course_by_teacher_name(name.strip())
#     elif ch == '3':
#         name = input('請輸入課程代碼: ')
#         find_course_by_class_id(name.strip())
#     elif ch == '0':
#         break
#     else :
#         print('Please input the correctly option')
#         input('press any key to countinue')
#input()
# close db
conn.close()
