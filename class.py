import requests
import re,os
import shutil
from bs4 import BeautifulSoup
import hashlib
import time

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

def isUpdate(html):
    print(html)
    m = hashlib.md5(html)
    # m.update(html)
    md5 = m.hexdigest()

    old_md5 = ''
    if os.path.exists('old_md5'):
        with open('old_md5', 'r') as f:
            old_md5 = f.read()
    with open('old_md5' ,'w') as f:
        f.write(md5)
    print(md5)
    print(old_md5)
    if md5 != old_md5:
        return True
    else:
        return False

def getdata(url, index,courses):
    html = requests.get(url)
    html.encoding = 'utf-8'
    sp = BeautifulSoup(html.text,'lxml')

    table = sp.select('table')
    # print(table[0])
    trs = table[0].select('tr')
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
            courses[index].append(tmp)

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
            courses[index].append(tmp)
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
            courses[index].append(tmp)

def crawler():
    global courses
    courses = {}
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
        shutil.copyfile('courses.json','./courses_data/'+str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')
        # shutil.copyfile('courses.json','./courses_data/'+str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')

    # move file(code_table.json) before store data to code_table.json
    # if os.path.exists('code_table.json'):
        # shutil.copyfile('code_table.json','./code_table_data/'+str(time.strftime('%Y_%m_%d',time.localtime())) + '.json')

# create the dir for sroring data
if not os.path.isdir("code_table_data"):
    os.mkdir("code_table_data")

if not os.path.isdir("courses_data"):
    os.mkdir("courses_data")

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
    print(courses)
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
while True:
    print('\n----------------------')
    print('1. 查找課程by課名')
    print('2. 查找課程by老師')
    print('3. 查找課程by課程代碼')
    print('0. 離開')
    print('----------------------')
    ch = input("選項: ")
    if ch == '1':
        name = input('請輸入課程名稱: ')
        find_course_by_class_name(name.strip())
    elif ch == '2':
        name = input('請輸入老師名稱: ')
        find_course_by_teacher_name(name.strip())
    elif ch == '3':
        name = input('請輸入課程代碼: ')
        find_course_by_class_id(name.strip())
    elif ch == '0':
        break
    else :
        print('Please input the correctly option')
        input('press any key to countinue')
#input()
