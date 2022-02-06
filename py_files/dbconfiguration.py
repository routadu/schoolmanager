import mysql.connector as sql
import time
import os
from kivy.storage.jsonstore import JsonStore

section_container=['a','b','c','d','e','f','g','h','i']

def secfetch(x):
    d={'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9'}
    return d[x]


def config(user_name,password,highest_class,highest_sec):


    global section_container

    a=sql.connect(host="localhost",username="root",passwd=password)
    cur=a.cursor()
    cur.execute("create database {}".format(user_name))
    a.commit()
    time.sleep(1)
    cur.execute("use {}".format(user_name))
    cur.execute("create table library_user_database (name varchar(200), id bigint(13), book_id varchar(11), issue_date varchar(200), return_date varchar(200))")
    cur.execute("create table library_book_database (book_name varchar(200), book_id varchar(11), qty int(4))")
    
    cur.execute("create table id_contact (id bigint(13), email_id varchar(100), ph_no bigint(10), aadhar_num bigint(12))")
    cur.execute("create table teachers ( t_id bigint(13), name varchar(200), age int(3), gender varchar(20), ph_no bigint(10), dob varchar(20), email_id varchar(200), aadhar_num bigint(12), qualification varchar(100), t_subject varchar(100), class_teacher varchar(100), t_class varchar(100), salary bigint(10), doj varchar(20))")
    cur.execute("insert into teachers value (1000000000000,'dummy',50,'dummy',4354554454,'34-34-34','dummy@duymmy.com',654456654456,'dummy','dummy','dummy','dummy',56445,'dummy')")
    a.commit()
    classes=int(highest_class)
    highest_section=highest_sec.lower()

    local_storage_class = JsonStore("../App/Data/School/school.json")
    
    for i in range(1,classes+1):
        bfr=section_container.index(highest_section)
        for j in range(bfr+1):
            section=str(section_container[j])
            if i<10:
                class_sec='9'+str(i)+section
            else:
                class_sec=str(i)+section
            class_sec_num=class_sec[0:2]+secfetch(section)+'000000000'
            class_sec_num=int(class_sec_num)
            
            if os.path.exists("./App/Data/Student/{}".format(class_sec))==True:
                print("passing directory {}".format(class_sec))
            else:
                os.makedirs("./App/Data/Student/{}".format(class_sec))
                print("creating directory {}".format(class_sec))

            cur.execute("create table {} ( student_id bigint(12), name varchar(200), age int(3), gender varchar(20), aadhar_num bigint(12), ph_no bigint(10), dob varchar(20), class_sec varchar(10), shift varchar(20), email_id varchar(100), f_name varchar(200), m_name varchar(200), attendance varchar(10) DEFAULT '0/210', roll_no int(4))".format(class_sec))
            cur.execute("insert into {} values ({},'dummy',99,'dummy',345435345345,4545454545,'dummy','dummy','dummy','dummy','dummy','dummy','dummy',0)".format(class_sec,class_sec_num))
            a.commit()
            time.sleep(1)

    return "Success"

    
    
    

    
