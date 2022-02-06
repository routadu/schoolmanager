# Importing required modules

from functools import partial
import time
from datetime import datetime,timedelta
import os
import shutil
import pickle

import plyer
import mysql.connector as sql
import matplotlib.pyplot as plt

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import Screen,ScreenManager,SlideTransition,RiseInTransition,NoTransition,FallOutTransition,FadeTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color,Rectangle,Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.config import  Config
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.properties import ListProperty,ObjectProperty,StringProperty

from py_files import dbconfiguration
from py_files import score_analyzer
from py_files import push_notification_email as mail_service


def win_notification(app_name="Task Manager",message="",duration=3):
    plyer.notification.notify(title="{}".format(app_name), message="{}".format(message))

    
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# global container variables

FetchStudentDetails_fetch_details=['']

FetchStudentDetails_fetch_details_cont=0

FetchClassWise_submit=['']

FetchClassWise_submit_cont=0

AddStudent_runcycle=0

mail_service_username=''

mail_service_password=''

school_name='Kendriya Vidyalaya Andrews Ganj'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





kv_file = '''    

<EllipseButtonType1@Button>:

    background_color:(0,0,0,0)
    background_normal:""
    
    canvas.before:
        Color:
            rgba:app.fnt_fg_color
        Ellipse:
            size:self.size
            pos:self.pos

<RoundedButtonType1@Button>:

    background_color:(0,0,0,0)
    background_normal:""
    
    canvas.before:
        Color:
            rgba:app.fnt_fg_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius: [21]

<RoundedButtonType2Left@Button>:

    background_color:(0,0,0,0)
    background_normal:""
    
    canvas.before:
        Color:
            rgba:app.fnt_fg_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius: [21,2,2,21]

<RoundedButtonType2Centre@Button>:

    background_color:(0,0,0,0)
    background_normal:""
    
    canvas.before:
        Color:
            rgba:app.fnt_fg_color
        Rectangle:
            size:self.size
            pos:self.pos

<RoundedButtonType2Right@Button>:

    background_color:(0,0,0,0)
    background_normal:""
    
    canvas.before:
        Color:
            rgba:app.fnt_fg_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius: [2,21,21,2]

<WelcomePage>:

    GridLayout:
 
        size:root.size
        cols:1

        canvas.before:
            Color:
                rgba:app.fnt_fg_color
            Rectangle:
                size:self.size
                pos:self.pos
        
        Label:
            bold:True
            text: "WELCOME"
            font_size: 40




<popup_exit>:

    id:main_win
    title:'Exit'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(450,450)

    exit_btn:exit_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'


    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    BoxLayout:
        orientation:'vertical'
        padding:[self.size[0]/3,10]
        Label:
            size_hint_y:0.30
        Label:
            size_hint_y:0.25
            text:'Are you sure to exit the application ?'
            font_size:20
            color:(0,0,0,1)
    
        Label:
            size_hint_y:0.30

        BoxLayout:
            padding:[20,0]
            size_hint_y:0.15
            
            RoundedButtonType1:
                id:exit_btn
                text:'Exit'
                bold:True
                on_release:root.closeapp()



<LoginPage>:

    orientation:'vertical'
    id:main_win
    username:uname
    passwd:password
    btn:button_login
    btn_signup:button_signup
    exit_btn:exit_button
    space_x:self.size[0]/3

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    BoxLayout:

        orientation:'horizontal'
        size_hint_y:None
        height:80

        canvas.before:
            Color:
                rgba:app.fnt_fg_color
            Rectangle:
                size:self.size
                pos:self.pos

        Label:
            size_hint_x:0.2

        Label:
            text:"Sign In"
            font_size:25
            bold:True
            size_hint_x:0.6
        
        Label:
            size_hint_x:0.195

        Button:
            id:exit_button
            text:"Exit"
            bold:True
            background_color:app.fnt_fg_color
            background_normal:''
            size_hint_x:0.05

    Label:
        size_hint_y:None
        height:245
        
    BoxLayout:
        padding:main_win.space_x,10
        orientation:"vertical"
        spacing:10
        size_hint_y:None
        height:130


        TextInput:
            id:uname
            hint_text:"Enter Username"
            size_hint_y:None
            height:45
            multiline:False
            write_tab:False
            
        TextInput:
            id:password
            hint_text:"Enter Password"
            size_hint_y:None
            height:45
            password:True
            multiline:False
            write_tab:False
        

    Label:
        size_hint_y:None
        height:55
        
    BoxLayout:
        padding:[main_win.space_x,0]
        size_hint_y:None
        height:45

        Label:
            size_hint_x:0.05
            
        RoundedButtonType2Left:

            id:button_login
            text:"Login"
            size_hint_x:0.3

        Label:
            size_hint_x:None
            width:5
            
        RoundedButtonType2Right:

            id:button_signup
            text:"Sign Up"
            size_hint_x:0.3

        Label:
            size_hint_x:0.05

        
    Label:
        id:blank2
        size_hint_y:None
        height:310


<SignUpPage>:
    id:main_win
    orientation:'vertical'
    space_x:self.size[0]/3
    cont:continu

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x,10
        spacing:10

        Label:
            id:conti
            text:"Account Created Successfully"
            font_size:27
            bold:True
            color:app.fnt_fg_color
        
        Button:
            padding:[main_win.space_x+60,0]
            id:continu
            text:"Continue"
            bold:True
            font_size:25
            size_hint_y:0
            height:46
            background_color:app.fnt_fg_color
            background_normal:''

        Label:
            id:blnk
            size_hint_y:None
            height:200


<DatabaseConfigurationPage>:

    orientation:'vertical'
    space_x:self.size[0]/3
    id:main_win
    spacing:20

    highest_class:highest_class
    highest_section:highest_section

    submit_btn:submit_btn

    bxlayout:bxlayout

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    BoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        spacing:5
        height:80

        canvas.before:
            Color:
                rgba:app.fnt_fg_color
            Rectangle:
                size:self.size
                pos:self.pos

        Label:
            
            text:'Database Configuration'
            font_size:30
            bold:True

    Label:
        size_hint_y:None
        height:130
    
    BoxLayout:

        orientation:'vertical'
        padding:[main_win.space_x-20,0]

        GridLayout:

            cols:2
            size_hint_y:None
            height:240
            spacing:[15,25]

            Label:

                text:"Highest Class"
                size_hint_y:None
                height:40
                color:(0,0,0,1)

            TextInput:

                id:highest_class
                hint_text:"( In double digits )"
                size_hint_y:None
                height:40
            
            Label:
            
                text:"Highest Section"
                size_hint_y:None
                height:40
                color:(0,0,0,1)

            TextInput:

                id:highest_section
                hint_text:"Max is ( I )"
                size_hint_y:None
                height:40
    
    BoxLayout:

        id:bxlayout
        orientation:'vertical'
        padding:[main_win.space_x+120,0]

        RoundedButtonType1:

            id:submit_btn
            text:'Submit'
            size_hint_y:None
            height:40
            
    Label:
        size_hint_y:None
        height:60

<AfterLogin>:
    orientation:'vertical'
    id:main_win
    login_stat:loginstat
    btn:button
    space_x:self.size[0]/3

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x,10
        size_hint_y:None
        height:60
        
        Label:
            id:loginstat
            bold:True
            font_size:35
            color:app.fnt_fg_color

    Label:
        size_hint_y:None
        height:350
    
    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x+100,10
        size_hint_y:None
        height:70
        
        RoundedButtonType1:

            id:button
            text:"Continue"
            bold:True
            font_size:26   
        
    Label:
        id:blank34
        size_hint_y:None
        height:150


<AppInterfaceNavBar>:

    home_btn:home_btn
    back_btn:back_btn
    logout_btn:logout_btn
    setting_btn:setting_btn
    
    orientation:'horizontal'
    size_hint_y:None
    spacing:5
    height:50
    canvas.before:
        Color:
            rgba:app.fnt_fg_color
        Rectangle:
            size:self.size
            pos:self.pos

    Button:
        text:"<"
        id:back_btn
        font_size:22
        size_hint_x:0.0285
        background_color:app.fnt_fg_color
        background_normal:''
        on_release:app.back()

    Button:
        text:"Home"
        id:home_btn
        background_color:app.fnt_fg_color
        background_normal:''
        size_hint_x:0.1
        on_release:app.home()

    Button:
        text:"Settings"
        id:setting_btn
        background_color:app.fnt_fg_color
        background_normal:''
        size_hint_x:0.1
        on_release:app.settings()
    
    Label:
        id:blank
        size_hint_x:0.6715
    
    Button:
        text:"Logout"
        id:logout_btn
        background_color:app.fnt_fg_color
        background_normal:''
        size_hint_x:0.1
        on_release:app.logout()


<HomePage>:

    orientation:'vertical'
    id:main_win

    student_btn:student_btn
    teacher_btn:teacher_btn
    employee_btn:employee_btn
    othersection_btn:othersection_btn
    adminsection_btn:adminsection_btn


    space_x:self.size[0]/3

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos


    Label:
        size_hint_y:None
        height:200

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x+110,10
        spacing:46

        
        RoundedButtonType1:
            id:student_btn
            text:"Student's Section"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:teacher_btn
            text:"Teacher's Section"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        RoundedButtonType1:
            id:employee_btn
            text:"Employee's Section"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:othersection_btn
            text:"Others Section"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        RoundedButtonType1:
            id:adminsection_btn
            text:"Admin Section"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        Label:
            size_hint_y:None
            height:150


<StudentSection>:
    orientation:'vertical'
    space_x:self.size[0]/3
    id:main_win
    spacing:20

    fetch_std_btn:fetch_std
    fetch_class_btn:fetch_class
    add_student_btn:add_std
    remove_student_btn:remove_std
    
    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos


    Label:
        size_hint_y:None
        height:185

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x+110,10
        spacing:46

        
        RoundedButtonType1:
            id:fetch_std
            text:"Fetch Student Details"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:fetch_class
            text:"Fetch Classwise Records"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        RoundedButtonType1:
            id:add_std
            text:"Add Student(s)"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:remove_std
            text:"Remove Student(s)"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        Label:
            size_hint_y:None
            height:165

<popup_updatestudentperformance>:
    
    id:main_win
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(600,600)

    gdlayout:gdlayout

    update_btn:update_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:
        orientation:'vertical'

        BoxLayout:
            size_hint_y:0.1

        BoxLayout:

            size_hint_y:0.7

            ScrollView:

                size:self.size
                id:main_box
                do_scroll_x: False
                do_scroll_y: True
                size_hint_y:None
                height:430
                bar_width:5
                bar_color:(247/255, 202/255, 24/255, 1)
                bar_inactive_color:[136/255,136/255,136/255,1]

                GridLayout:
                
                    size_hint_y:None
                    height:1600
                    id:gdlayout
                    cols:2
                    size_hint_y:None
                    spacing:[10,10]
                    padding:[0,0,20,0]

        Label:
            size_hint_y:0.1

        BoxLayout:
            
            padding:[100,0]
            size_hint_y:0.1

            RoundedButtonType1:
                text:"Update"
                id:update_btn
                size_hint_x:None
                width:110
            
            Label:
                size_hint_x:None
                width:150

            RoundedButtonType1:
                text:"Cancel"
                id:cancel_btn
                size_hint_x:None
                width:110

            Label:
                size_hint_x:None
                width:30

<FetchStudentDetails>:
    orientation:'vertical'
    spacing:20
    
    id:main_win
    space_x:self.size[0]/3

    student_id:std_id
    submit_btn:submit_button

    form_name:form_name
    form_class:form_class
    form_rollno:form_rollno
    form_stdid:form_stdid
    form_fname:form_fname
    form_mname:form_mname
    form_attendance:form_attendance
    form_phno:form_phno
    form_age_gender:form_age_gender
    form_aadhar_num:form_aadhar_num
    form_dob:form_dob
    form_email:form_email

    image_gdlayout:image_gdlayout

    gdlayout:gdlayout
    scrollview:scrollview
    bxlayout3:bxlayout3
    bxlayout4:bxlayout4
    bxlayout5:bxlayout5

    subject_label:subject_label
    performance_suggestion_box:performance_suggestion_box

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:50
    
    BoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        height:30
        spacing:20

        Label:
            size_hint_x:0.1
            text:'Enter Student ID:'
            color:(0,0,0,1)
        
        TextInput:
            id:std_id
            size_hint_x:0.7
            hint_text:'Enter 12 digit Student ID'
            input_filter: lambda text, from_undo: text[:12 - len(self.text)]
            write_tab:False
            multiline:False
        
        Label:
            size_hint_x:0.1
        
        RoundedButtonType1:
            size_hint_x:0.06
            text:'Submit'
            id:submit_button

        Label:
            size_hint_x:0.04
    
    Label:
        size_hint_y:0.08
    
    ScrollView:
        id:scrollview
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y:None
        height:700
        bar_width:10
        bar_color:app.fnt_fg_color
        bar_inactive_color:[136/255,136/255,136/255,1]

        GridLayout:
            id:gdlayout
            spacex:self.size[0]/3
            size_hint_y:None
            height:self.minimum_height
            cols:1

            Label:
                size_hint_y:None
                height:20

            BoxLayout:
        
                size_hint_y:None
                height:240

                GridLayout:
                    size_hint_x:0.6
                    cols:2
                    spacing:[0,30]
                    Label:
                        text:'Name'
                        font_size:20
                        color:(0,0,0,1)
                
                    Label:
                        font_size:20
                        id:form_name
                        color:(0,0,0,1)
                    
                    Label:
                        text:"Class"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_class
                        font_size:20
                        color:(0,0,0,1)
                    
                    Label:
                        text:"Roll Number"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_rollno
                        font_size:20
                        color:(0,0,0,1)
                        

                    Label:
                        text:"Student ID"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_stdid
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        text:"Aadhar Number"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_aadhar_num
                        color:(0,0,0,1)
                        font_size:20
                    
                Label:
                    size_hint_x:0.2

                GridLayout:
                    size_hint_x:0.2
                    cols:1
                    id:image_gdlayout
            Label:
                size_hint_y:None
                height:25


            BoxLayout:
                
                size_hint_y:None
                height:280

                GridLayout:

                    size_hint_x:0.6
                    cols:2
                    spacing:[0,30]

                    Label:
                        text:"Phone Number"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_phno
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        text:"Age & Gender"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_age_gender
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        text:"Date of Birth"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_dob
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        text:"Email ID"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_email
                        color:(0,0,0,1)
                        font_size:20


                    Label:
                        text:"Father's Name"
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        id:form_fname
                        font_size:20
                        color:(0,0,0,1)

                    Label:
                        text:"Mother's Name"
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        id:form_mname
                        font_size:20
                        color:(0,0,0,1)
                        
                    
                    Label:
                        text:"Attendance"
                        color:(0,0,0,1)
                        font_size:20
                
                    Label:
                        id:form_attendance
                        font_size:20
                        color:(0,0,0,1)


                Label:
                    size_hint_x:0.2
                    
                    
                BoxLayout:
                    size_hint_x:0.2
                    orientation:'vertical'

                    Label:
                        id:form_attendace_suggestion
                        color:(0,0,0,1)

            Label:
                size_hint_y:None
                height:130
            
            BoxLayout:
                id:bxlayout3
                size_hint_y:None
                height:40
                padding:[self.size[0]/3+120,0]

            Label:
                size_hint_y:None
                height:100
            
            BoxLayout:

                size_hint_y:None
                height:600
                orientation:'vertical'
                id:bxlayout4
                size_hint_y:None

            Label:
                size_hint_y:None
                height:40

            
            Label:
                text_size:self.size
                halign:'center'
                valign:'middle'
                id:subject_label
                color:(0,0,0,1)
                size_hint_y:None
                font_size:25
                height:35

            Label:
                size_hint_y:None
                height:20
                
            Label:
                text_size:self.size
                halign:'center'
                valign:'middle'
                id:performance_suggestion_box
                size_hint_y:None
                height:100
                font_size:18
                strip:True
                color:(0,0,0,1)

            Label:
                size_hint_y:None
                height:40

            BoxLayout:

                id:bxlayout5
                padding:[main_win.space_x+150,0]
                size_hint_y:None
                height:40

            Label:
                size_hint_y:None
                height:170


<FetchClassWise>:
    id:main_win
    orientation:'vertical'
    space_x:self.size[0]/3
    spacing:20

    enter_class_txt:enter_class
    enter_section_txt:enter_section

    gdlayout:gdlayout

    submit_btn:submit

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:50
    
    BoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        height:30
        spacing:15

        Label:
            size_hint_x:0.075
            text:'Enter Class'
            color:0,0,0,1

        TextInput:
            id:enter_class
            size_hint_x:0.55
            background_color:(218/255, 223/255, 225/255, 1)
            background_normal:''
            multiline:False
            write_tab:False

        Label:
            size_hint_x:0.075
            text:'Enter Section'
            color:0,0,0,1
        
        TextInput:
            id:enter_section
            size_hint_x:0.22
            background_color:(218/255, 223/255, 225/255, 1)
            background_normal:''
            multiline:False
            write_tab:False
        
        Label:
            size_hint_x:0.02
        
        RoundedButtonType1:
            id:submit
            text:"Submit"
            size_hint_x:0.05

        Label:
            size_hint_x:0.01

    GridLayout:
        size_hint_y:0.08
        cols:3

        Label:
            text:''
            size_hint_x:0.4

        Label:
            text:''
            size_hint_x:0.4

        BoxLayout:
            size_hint_x:0.1
        
        Label:
            size_hint_x:0.1


    GridLayout:
        cols:6
        size_hint_y:0.1
        padding:[5,5]

        Label:
            text:'Student ID'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
            
        Label:
            text:'Name'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
            
        Label:
            text:'Class and Section'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
            
        Label:
            text:'Roll No.'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True

        Label:
            text:'Phone Number'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True

        Label:
            text:'Attendance'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True



    ScrollView:
        size:self.size
        id:main_box
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y:0.692
        bar_width:10
        bar_color:app.fnt_fg_color
        bar_inactive_color:[136/255,136/255,136/255,1]
        padding:[10,0]

        GridLayout:
            id:gdlayout
            cols:6
            size_hint_y:None
            padding:[5,5]


<attendance_popup>:

    id:popup_attendance
    title:'Attendance'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(400,400)

    attendance_label:attendance_label
    student_label:student_label

    add_btn:add_btn
    back_btn:back_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'
        
        Label:
            size_hint_y:0.03

        Label:
            size_hint_y:0.2
            id:student_label
            bold:True
            color:(0,0,0,1)
    
        Label:
            size_hint_y:0.17

        Label:
            size_hint_y:0.2
            id:attendance_label
            bold:True
            color:(0,0,0,1)

        Label:
            size_hint_y:0.25

        BoxLayout:
           
            id:bxlayout
            size_hint_y:0.15
            
            Label:
                size_hint_x:None
                width:40

            RoundedButtonType1:
                size_hint_x:None
                width:120
                id:add_btn
                text:'Add'
                bold:True
                on_press:root.add()

            Label:
                size_hint_x:None
                width:60

            RoundedButtonType1:
                id:back_btn
                size_hint_x:None
                width:120
                text:'Back'
                bold:True
                on_release:root.cancel()

            Label:
                size_hint_x:None
                width:50
            


<popup_exit_without_saving_AddStudent>:
    id:popup_window
    title:'Exit'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(400,400)

    ex_btn:ex_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:
        orientation:'vertical'
        Label:
            size_hint_y:0.25
        Label:
            size_hint_y:0.25
            text:'Are you sure to exit without saving ?'
            bold:True
            color:(0,0,0,1)
    
        Label:
            size_hint_y:0.3

        BoxLayout:
            width:500
            id:bxlayout
            size_hint_y:0.20

            Label:
                width:25
                
            RoundedButtonType1:
                width:180
                text:'Cancel'
                id:cancel_btn
                bold:True
                on_release:popup_window.dismiss()

            Label:
                width:50

            RoundedButtonType1:
                width:120
                id:ex_btn
                text:'Exit'
                bold:True
            
            Label:
                width:25
                


<AddStudent>:
    id:add_student
    orientation:'vertical'
    space_x:self.size[0]/3
    spacing:20

    gdlayout:gdlayout

    submit_btn:submit_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos
            
        
    Label:
        size_hint_y:None
        height:85
    
    BoxLayout:

        GridLayout:
            id:gdlayout
            size_hint_x:0.7
            cols:2
            spacing:10
            
        GridLayout:

            size_hint_x:0.3
            cols:1

            BoxLayout:
                size_hint_y:0.4
                orientation:'horizontal'

                Label:
                    size_hint_x:0.3
                
                BoxLayout:

                    size_hint_x:0.4
                    id:image_gdlayout

                Label:
                    size_hint_x:0.3
            
            Label:
                size_hint_y:0.3
            
            Label:
                size_hint_y:0.3


    Label:
        size_hint_y:None
        height:35

    BoxLayout:

        id:btn_bxlayout
        size_hint_y:None
        height:60
        padding:[self.size[0]/3+100,10]

        RoundedButtonType1:
            id:submit_btn
            text:'Submit'


    Label:
        size_hint_y:None
        height:35



<RemoveStudent>:
    id:main_win_remove_student
    orientation:'vertical'
    space_x:self.size[0]/3
    spacing:20
    
    std_id:std_id
    submit_btn:submit_btn
    delete_btn:delete_btn

    form_name:form_name
    form_class:form_class
    form_rollno:form_rollno
    form_stdid:form_stdid
    form_img:form_img
    form_fname:form_fname
    form_mname:form_mname
    form_attendance:form_attendance
    form_phno:form_phno


    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:50 
    
    BoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        height:30
        spacing:20

        Label:
            size_hint_x:0.1
            text:'Enter Student ID:'
            color:(0,0,0,1)
        
        TextInput:
            id:std_id
            size_hint_x:0.7
            hint_text:'Enter 12 digit Student ID'
            input_filter: lambda text, from_undo: text[:12 - len(self.text)]
            write_tab:False
            multiline:False
        
        Label:
            size_hint_x:0.1
        
        RoundedButtonType1:
            size_hint_x:0.06
            text:'Submit'
            id:submit_btn

        Label:
            size_hint_x:0.04
    
    Label:
        size_hint_y:0.08
    
    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y:0.8
        bar_width:10
        bar_color:app.fnt_fg_color
        bar_inactive_color:[136/255,136/255,136/255,1]

        GridLayout:
            spacex:self.size[0]/3
            id:gdlayout
            size_hint_y:None
            height:self.minimum_height
            cols:1

            Label:
                size_hint_y:None
                height:20

            BoxLayout:
                id:bxlayout1
                size_hint_y:None
                height:240

                GridLayout:
                    size_hint_x:0.6
                    cols:2
                    spacing:[0,30]
                    Label:
                        text:'Name'
                        font_size:20
                        color:(0,0,0,1)
                
                    Label:
                        font_size:20
                        id:form_name
                        color:(0,0,0,1)
                    
                    Label:
                        text:"Class"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_class
                        font_size:20
                        color:(0,0,0,1)
                    
                    Label:
                        text:"Roll Number"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_rollno
                        font_size:20
                        color:(0,0,0,1)
                        

                    Label:
                        text:"Student ID"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_stdid
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        text:"Phone Number"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_phno
                        color:(0,0,0,1)
                        font_size:20
                    
                Label:
                    size_hint_x:0.2

                GridLayout:
                    size_hint_x:0.2
                    cols:1
                    id:form_img
            Label:
                size_hint_y:None
                height:25


            BoxLayout:
                id:bxlayout2
                size_hint_y:None
                height:120

                GridLayout:

                    size_hint_x:0.6
                    cols:2
                    spacing:[0,30]

                    Label:
                        text:"Father's Name"
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        id:form_fname
                        font_size:20
                        color:(0,0,0,1)

                    Label:
                        text:"Mother's Name"
                        color:(0,0,0,1)
                        font_size:20

                    Label:
                        id:form_mname
                        font_size:20
                        color:(0,0,0,1)
                        
                    
                    Label:
                        text:"Attendance"
                        color:(0,0,0,1)
                        font_size:20
                
                    Label:
                        id:form_attendance
                        font_size:20
                        color:(0,0,0,1)
                
                Label:
                    size_hint_x:0.4

            Label:
                size_hint_y:None
                height:70

            BoxLayout:

                id:btn_bxlayout
                size_hint_y:None
                height:60
                padding:[self.size[0]/3+120,10]

                RoundedButtonType1:
                    id:delete_btn
                    text:'Delete Records'


            Label:
                size_hint_y:None
                height:20


<TeacherSection>:
    orientation:'vertical'
    space_x:self.size[0]/3
    id:main_win
    spacing:20

    fetch_teacherlist_btn:fetch_teacherlist
    add_teacher_btn:add_teacher
    remove_teacher_btn:remove_teacher
    
    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos


    Label:
        size_hint_y:None
        height:120

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x+110,10
        spacing:46

        
        RoundedButtonType1:
            id:fetch_teacherlist
            text:"View Teacher List"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:add_teacher
            text:"Add Teacher(s)"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        

        RoundedButtonType1:
            id:remove_teacher
            text:"Remove Teacher(s)"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        Label:
            size_hint_y:None
            height:230



<FetchTeacherList>:
    id:main_win
    orientation:'vertical'
    space_x:self.size[0]/3
    spacing:20

    main_box:main_box
    
    gdlayout1:gdlayout1

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:70

    
    GridLayout:
        cols:8
        size_hint_y:0.1
        padding:[5,5]

        Label:
            text:'Teacher ID'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
            
        Label:
            text:'Name'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
            
            
        Label:
            text:'Age'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True

        Label:
            text:'Phone Number'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
        
        Label:
            text:'Email ID'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
        
        Label:
            text:'Subject'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
        
        Label:
            text:'Class Teacher'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True
        
        Label:
            text:'Salary'
            size_hint_y:None
            height:60
            color:[0,0,0,1]
            bold:True

    ScrollView:

        id:main_box
        size:self.size
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y:0.692
        bar_width:10
        bar_color:app.fnt_fg_color
        bar_inactive_color:[136/255,136/255,136/255,1]
        padding:[10,0]

        GridLayout:
            id:gdlayout1
            cols:8
            size_hint_y:None
            padding:[5,5]




<AddTeacher>:
    id:main_win_add_teacher
    orientation:'vertical'
    space_x:self.size[0]/3
    spacing:20

    gdlayout:gdlayout

    submit_btn:submit_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

        
    Label:
        size_hint_y:None
        height:100
    
    BoxLayout:

        GridLayout:

            id:gdlayout
            size_hint_x:0.6
            cols:2
            spacing:10
            
        GridLayout:

            size_hint_x:0.4
            cols:1
    Label:
        size_hint_y:None
        height:50

    BoxLayout:

        id:btn_bxlayout
        size_hint_y:None
        height:60
        padding:[self.size[0]/3+140,0]

        RoundedButtonType1:
            id:submit_btn
            size_hint_y:None
            height:45
            text:'Submit'


    Label:
        size_hint_y:None
        height:40


<RemoveTeacher>:
    id:main_win_remove_teacher
    orientation:'vertical'
    space_x:self.size[0]/3
    spacing:20

    t_id_textinput:t_id_textinput
    t_id:t_id
    name:name
    gender:gender
    age:age
    ph_no:ph_no
    dob:dob
    email_id:email_id
    aadhar_num:aadhar_num
    qualification:qualification
    t_subject:t_subject
    class_teacher:class_teacher
    t_class:t_class
    salary:salary

    submit_btn:submit_btn
    delete_btn:delete_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:50
        
    BoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        height:30
        spacing:20

        Label:
            size_hint_x:0.1
            text:'Enter Teacher ID:'
            color:(0,0,0,1)
        
        TextInput:
            id:t_id_textinput
            size_hint_x:0.7
            hint_text:'Enter 13 digit Teacher ID'
            input_filter: lambda text, from_undo: text[:13 - len(self.text)]
            write_tab:False
            multiline:False
        
        Label:
            size_hint_x:0.1
        
        RoundedButtonType1:
            size_hint_x:0.06
            text:'Submit'
            id:submit_btn

        Label:
            size_hint_x:0.04  
    
    Label:
        size_hint_y:None
        height:70
    
    BoxLayout:

        GridLayout:

            size_hint_x:0.6
            cols:2
            spacing:20

            Label:
                text:'Teacher ID'
                color:[0,0,0,1]
                bold:True

            Label:
                id:t_id
                color:[0,0,0,1]

            Label:
                text:'Name'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:name
                color:[0,0,0,1]

            Label:
                text:'Age'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:age
                color:[0,0,0,1]
            
            Label:
                text:'Gender'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:gender
                color:[0,0,0,1]
            
            Label:
                text:'Phone Number'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:ph_no
                color:[0,0,0,1]
            
            Label:
                text:'Date Of Birth'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:dob
                color:[0,0,0,1]

            Label:
                text:'Email ID'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:email_id
                color:[0,0,0,1]
            
            Label:
                text:'Aadhar Number'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:aadhar_num
                color:[0,0,0,1]
            
            Label:
                text:'Qualification'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:qualification
                color:[0,0,0,1]
            
            Label:
                text:'Teaching Subject'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:t_subject
                color:[0,0,0,1]
            
            Label:
                text:'Class Teacher'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:class_teacher
                color:[0,0,0,1]
            
            Label:
                text:'Teaching Classes'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:t_class
                color:[0,0,0,1]
            
            Label:
                text:'Salary'
                color:[0,0,0,1]
                bold:True
            
            Label:
                id:salary
                color:[0,0,0,1]
            
        GridLayout:

            size_hint_x:0.4
            cols:1
    Label:
        size_hint_y:None
        height:70

    BoxLayout:

        id:btn_bxlayout
        size_hint_y:None
        height:60
        padding:[self.size[0]/3+120,10]

        RoundedButtonType1:
            id:delete_btn
            text:'Delete Records'


    Label:
        size_hint_y:None
        height:20


<OtherSection>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3
    spacing:20

    main_members_btn:main_members_btn
    push_notification_btn:push_notification_btn
    library_btn:library_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    
    Label:
        size_hint_y:None
        height:120

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x+110,10
        spacing:46

        
        RoundedButtonType1:
            id:main_members_btn
            text:"Main Members"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:push_notification_btn
            text:"Push Notfication"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        

        RoundedButtonType1:
            id:library_btn
            text:"Library"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        Label:
            size_hint_y:None
            height:230 


<MainMembers>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    school_label:school_label
    principal_label:principal_label
    vice_principal_label:vice_principal_label


    edit_btn:edit_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:80


    Label:
        id:school_label
        color:(0,0,0,1)
        font_size:40
        size_hint_y:None
        height:100

    Label:
        size_hint_y:None
        height:35

    Label:

        text:'MAIN MEMBERS'
        color:(0,0,0,1)
        font_size:25
        size_hint_y:None
        height:50
            
    Label:
        size_hint_y:None
        height:60


    ScrollView:

        size:self.size
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y:0.892
        bar_width:12
        bar_color:app.fnt_fg_color
        bar_inactive_color:[136/255,136/255,136/255,1]
        padding:[10,0]


        BoxLayout:
                
            orientation:'vertical'

            GridLayout:

                cols:2
                spacing:(0,50)

                Label:
                    text:'Principal'
                    color:(0,0,0,1)
                    font_size:20
                    size_hint_y:None
                    height:40
                
                Label:
                    id:principal_label
                    color:(0,0,0,1)
                    font_size:20
                    size_hint_y:None
                    height:40
                
                Label:
                    text:'Vice Principal'
                    color:(0,0,0,1)
                    font_size:20
                    size_hint_y:None
                    height:40

                Label:
                    id:vice_principal_label
                    color:(0,0,0,1)
                    font_size:20
                    size_hint_y:None
                    height:40

            Label:
                size_hint_y:None
                height:50

            BoxLayout:
                
                padding:[main_win.space_x+140,0]
                size_hint_y:None
                height:35

                RoundedButtonType1:
                    text:"Edit"
                    id:edit_btn
                
            Label:
                size_hint_y:None
                height:40



<PushNotification>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3
    spacing:20

    notif_all_btn:notif_all_btn
    notif_indv_btn:notif_indv_btn
    notif_grp_btn:notif_grp_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    
    Label:
        size_hint_y:None
        height:120

    BoxLayout:
        orientation:'vertical'
        padding:main_win.space_x+110,10
        spacing:46

        
        RoundedButtonType1:
            id:notif_indv_btn
            text:"Individual"
            size_hint_y:None
            height:46
            bold:True
            font_size:25

        RoundedButtonType1:
            id:notif_grp_btn
            text:"Group"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        

        RoundedButtonType1:
            id:notif_all_btn
            text:"All Members"
            size_hint_y:None
            height:46
            bold:True
            font_size:25
        
        Label:
            size_hint_y:None
            height:230
    


<PushNotificationIndividual>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    submit_btn:submit_btn

    gdlayout1:gdlayout1

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos
    
    Label:
        size_hint_y:None
        height:334

    BoxLayout:

        size_hint_y:None
        height:140

        Label:
            size_hint_x:0.20

        GridLayout:

            size_hint_x:0.5
            cols:2
            id:gdlayout1
            spacing:[0,20]

        Label:
            
            size_hint_x:0.3
    
    Label:
        size_hint_y:None
        height:130

    BoxLayout:

        size_hint_y:None
        height:40
        padding:[main_win.space_x+140,0]

        RoundedButtonType1:
            text:'Submit'
            id:submit_btn

    Label:
        size_hint_y:None
        height:220



<PushNotificationGroup>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    submit_btn:submit_btn

    gdlayout1:gdlayout1
    

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:334

    BoxLayout:

        size_hint_y:None
        height:140

        Label:
            size_hint_x:0.20

        GridLayout:

            size_hint_x:0.5
            cols:2
            id:gdlayout1
            spacing:[0,20]

        Label:
            
            size_hint_x:0.3
    
    Label:
        size_hint_y:None
        height:130

    BoxLayout:

        size_hint_y:None
        height:40
        padding:[main_win.space_x+140,0]

        RoundedButtonType1:
            text:'Submit'
            id:submit_btn

    Label:
        size_hint_y:None
        height:220
    


<PushNotificationAll>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    submit_btn:submit_btn

    gdlayout1:gdlayout1

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    
    Label:
        size_hint_y:None
        height:381

    BoxLayout:

        size_hint_y:None
        height:103

        Label:
            size_hint_x:0.20

        GridLayout:

            size_hint_x:0.5
            cols:2
            id:gdlayout1
            spacing:[0,20]

        Label:
            
            size_hint_x:0.3
    
    Label:
        size_hint_y:None
        height:110

    BoxLayout:

        size_hint_y:None
        height:40
        padding:[main_win.space_x+140,0]

        RoundedButtonType1:
            text:'Submit'
            id:submit_btn

    Label:
        size_hint_y:None
        height:230


<popup_book_manager_add>:

    title:'Add Book'
    title_color:[1,1,1,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(500,400)

    book_id:book_id
    book_name:book_name
    quantity:quantity

    submit_btn:submit_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'

        Label:
            size_hint_y:None
            height:45
        
        GridLayout:

            cols:2
            padding:[20,0,20,0]
            spacing:[20,30]

            Label:
                size_hint_y:None
                height:40
                text:'Book Name'
                color:(0,0,0,1)

            TextInput:
                size_hint_y:None
                height:40
                id:book_name

            Label:
                size_hint_y:None
                height:40
                text:'Book ID'
                color:(0,0,0,1)
            
            TextInput:
                size_hint_y:None
                height:40
                id:book_id
            
            Label:
                size_hint_y:None
                height:40
                text:'Quantity'
                color:(0,0,0,1)
            
            TextInput:
                size_hint_y:None
                height:50
                hint_text:"( prefix with '+' to add to current stock)"
                id:quantity
        
        Label:
            size_hint_y:None
            height:45
        
        BoxLayout:
           
            id:bxlayout
            size_hint_y:None
            height:60
            
            Label:
                size_hint_x:None
                width:65

            RoundedButtonType1:
                size_hint_x:None
                width:120
                id:submit_btn
                text:'Submit'
                bold:True
                on_press:root.submit()

            Label:
                size_hint_x:None
                width:110

            RoundedButtonType1:
                id:cancel_btn
                size_hint_x:None
                width:120
                text:'Cancel'
                bold:True
                on_release:root.cancel()

            Label:
                size_hint_x:None
                width:75


<popup_book_manager_remove>:

    title:'Remove Book'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(500,400)

    book_id:book_id
    quantity:quantity

    submit_btn:submit_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'

        Label:
            size_hint_y:None
            height:80
        
        GridLayout:

            cols:2
            padding:[20,0,20,0]
            spacing:[20,30]

            Label:
                size_hint_y:None
                height:40
                text:'Book ID'
                color:(0,0,0,1)
            
            TextInput:
                size_hint_y:None
                height:40
                id:book_id
            
            Label:
                size_hint_y:None
                height:40
                text:'Quantity'
                color:(0,0,0,1)
            
            TextInput:
                size_hint_y:None
                height:50
                hint_text:"( leave it empty to remove complete stock )"
                id:quantity
        
        Label:
            size_hint_y:None
            height:80
        
        BoxLayout:
           
            id:bxlayout
            size_hint_y:None
            height:60
            
            Label:
                size_hint_x:None
                width:65

            RoundedButtonType1:
                size_hint_x:None
                width:120
                id:submit_btn
                text:'Submit'
                bold:True
                on_press:root.submit()

            Label:
                size_hint_x:None
                width:110

            RoundedButtonType1:
                id:cancel_btn
                size_hint_x:None
                width:120
                text:'Cancel'
                bold:True
                on_release:root.cancel()

            Label:
                size_hint_x:None
                width:75

<popup_book_manager_view>:

    title:'Available Books'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(600,500)

    gdlayout:gdlayout
    
    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:
        orientation:"vertical"
        padding:[20,0]
            
        GridLayout:
            cols:3
            spacing:[20,0]
            size_hint_y:None
            height:50

            Label:
                size_hint_x:0.2
                text:"Book ID"
                font_size:19
                color:(0,0,0,1)

            Label:
                size_hint_x:0.6
                text:"Book Name"
                font_size:19
                color:(0,0,0,1)

            Label:
                size_hint_x:0.2
                text:"Quantity"
                font_size:19
                color:(0,0,0,1)

        Label:
            size_hint_y:None
            height:20

        ScrollView:
            size_hint_y:None
            height:340
            bar_width:8
            bar_color:app.fnt_fg_color
            bar_inactive_color:[136/255,136/255,136/255,1]
            
            GridLayout:
                cols:3
                id:gdlayout
                spacing:[10,10]
                minimum_height:360
            
            

<popup_book_manager_option>:

    title:'Options'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(550,390)

    add_btn:add_btn
    remove_btn:remove_btn
    view_btn:view_btn
    
    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'

        Label:
            size_hint_y:0.4
        
        Label:
            size_hint_y:0.025

        BoxLayout:
           
            id:bxlayout
            size_hint_y:None
            height:50
            
            Label:
                size_hint_x:None
                width:40

            RoundedButtonType1:
                size_hint_x:None
                width:100
                id:add_btn
                text:'Add Book'
                bold:True
                on_press:root.add()

            Label:
                size_hint_x:None
                width:60

            RoundedButtonType1:
                size_hint_x:None
                width:110
                id:remove_btn
                text:'Remove Book'
                bold:True
                on_release:root.remove()

            Label:
                size_hint_x:None
                width:60

            RoundedButtonType1:
                size_hint_x:None
                width:100
                id:view_btn
                text:'View Books'
                bold:True
                on_release:root.view()

            Label:
                size_hint_x:None
                width:40

        Label:
            size_hint_y:0.4

<popup_book_issue>:

    title:'Issue Book'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(400,400)

    book_id:book_id
    return_date:return_date

    submit_btn:submit_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'

        Label:
            size_hint_y:None
            height:80
        
        GridLayout:

            cols:2
            padding:[20,0,20,0]
            spacing:[20,30]

            Label:
                size_hint_y:None
                height:40
                text:'Book ID'
                color:(0,0,0,1)

            TextInput:
                size_hint_y:None
                height:40
                id:book_id

            Label:
                size_hint_y:None
                height:40
                text:'Return Date'
                color:(0,0,0,1)
            
            TextInput:
                size_hint_y:None
                height:40
                id:return_date
                hint_text:"dd-mm-yyyy"
        
        Label:
            size_hint_y:None
            height:80
        
        BoxLayout:
           
            id:bxlayout
            size_hint_y:None
            height:60
            
            Label:
                size_hint_x:None
                width:40

            RoundedButtonType1:
                size_hint_x:None
                width:120
                id:submit_btn
                text:'Submit'
                bold:True
                on_press:root.submit()

            Label:
                size_hint_x:None
                width:60

            RoundedButtonType1:
                id:cancel_btn
                size_hint_x:None
                width:120
                text:'Cancel'
                bold:True
                on_release:root.cancel()

            Label:
                size_hint_x:None
                width:50

<popup_book_return>:


    title:'Return Book'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(400,400)

    confirm_btn:confirm_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'

        Label:
            size_hint_y:None
            height:80

        Label:
            size_hint_y:None
            height:260
            text:"Confirm return of current issued book ?"
            font_size:20
            color:(0,0,0,1)
        
        BoxLayout:
           
            id:bxlayout
            size_hint_y:None
            height:60
            
            Label:
                size_hint_x:None
                width:40

            RoundedButtonType1:
                size_hint_x:None
                width:120
                id:confirm_btn
                text:'Confirm'
                bold:True
                on_press:root.confirm()

            Label:
                size_hint_x:None
                width:60

            RoundedButtonType1:
                id:cancel_btn
                size_hint_x:None
                width:120
                text:'Cancel'
                bold:True
                on_release:root.cancel()

            Label:
                size_hint_x:None
                width:50


<LibraryPage>:

    orientation:'vertical'
    spacing:20
    
    id:main_win
    space_x:self.size[0]/3

    book_manager_btn:book_manager_btn

    borrower_id:borrower_id
    submit_btn:submit_button

    gdlayout:gdlayout
    scrollview:scrollview
    
    form_name:form_name
    form_phno:form_phno
    form_email:form_email
    form_borrowerid:form_borrowerid

    book_name:book_name
    book_id:book_id
    issue_date:issue_date
    return_date:return_date

    issue_btn:issue_btn
    return_btn:return_btn
    reminder_btn:reminder_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos

    Label:
        size_hint_y:None
        height:15
    
    BoxLayout:
        orientation:'horizontal'
        size_hint_y:None
        height:30
        spacing:15

        Label:
            size_hint_x:0.1
            text:'Enter your ID:'
            color:(0,0,0,1)
        
        TextInput:
            id:borrower_id
            size_hint_x:0.7
            hint_text:'Enter 12/13 digit ID'
            input_filter: lambda text, from_undo: text[:13 - len(self.text)]
            write_tab:False
            multiline:False
        
        Label:
            size_hint_x:0.1
        
        RoundedButtonType1:
            size_hint_x:0.06
            text:'Submit'
            id:submit_button

        Label:
            size_hint_x:0.04
    
    Label:
        size_hint_y:0.08


    ScrollView:
        id:scrollview
        do_scroll_x: False
        do_scroll_y: True
        size_hint_y:None
        height:680
        bar_width:10
        bar_color:app.fnt_fg_color
        bar_inactive_color:[136/255,136/255,136/255,1]

        GridLayout:

            id:gdlayout
            spacex:self.size[0]/3
            size_hint_y:None
            height:self.minimum_height
            cols:1

            Label:
                size_hint_y:None
                height:20

            BoxLayout:
        
                size_hint_y:None
                height:200

                GridLayout:

                    cols:2
                    spacing:[0,30]

                    Label:
                        text:'Name'
                        font_size:20
                        color:(0,0,0,1)
                
                    Label:
                        font_size:20
                        id:form_name
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'
                    
                    Label:
                        text:"ID"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_borrowerid
                        color:(0,0,0,1)
                        font_size:20
                        text_size:self.size
                        halign:'left'
                        valign:'middle'

                    Label:
                        text:"Phone Number"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_phno
                        font_size:20
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'
                    
                    Label:
                        text:"Email ID"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:form_email
                        font_size:20
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'

            Label:
                size_hint_y:None
                height:80

            Label:
                
                text:"Book Details"
                color:(0,0,0,1)
                size_hint_y:None
                height:40
                font_size:30

            Label:
                size_hint_y:None
                height:80

            BoxLayout:

                size_hint_y:None
                height:200

                GridLayout:

                    cols:2
                    spacing:[0,30]

                    Label:
                        text:"Book Name"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:book_name
                        font_size:20
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'
                    
                    Label:
                        text:"Book ID"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:book_id
                        font_size:20
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'
                    
                    Label:
                        text:"Issue Date"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:issue_date
                        font_size:20
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'
                    
                    Label:
                        text:"Return Date"
                        color:(0,0,0,1)
                        font_size:20
                    
                    Label:
                        id:return_date
                        font_size:20
                        color:(0,0,0,1)
                        text_size:self.size
                        halign:'left'
                        valign:'middle'
                        

            Label:

                size_hint_y:None
                height:90        

            BoxLayout:
                
                size_hint_y:None
                height:40
                padding:[100,0]

                Label:
                    size_hint_x:None
                    width:0.2

                BoxLayout:
                    
                    size_hint_x:0.6

                    Label:
                        size_hint_x:None
                        width:150

                    RoundedButtonType2Left:
                        text:"Issue Book"
                        id:issue_btn
                
                    Label:
                        size_hint_x:None
                        width:180

                    RoundedButtonType2Centre:
                        text:"Return Book"
                        id:return_btn
                
                    Label:
                        size_hint_x:None
                        width:180

                    RoundedButtonType2Right:
                        text:"Send Reminder"
                        id:reminder_btn

                    Label:
                        size_hint_x:None
                        width:150

                Label:
                    size_hint_x:None
                    width:0.2

            Label:
                size_hint_y:None
                height:100

            BoxLayout:
                padding:[685,0,585,0]
                size_hint_y:None
                height:45

                RoundedButtonType1:
                    id:book_manager_btn
                    text:"Book Manager"
                    size_hint_x:None
                    width:150

            Label:
                size_hint_y:None
                height:100   

<SettingsPage>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    changetheme_btn:changetheme_btn
    mailacc_btn:mailacc_btn

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos


    Label:
        size_hint_y:None
        height:391

    BoxLayout:
        size_hint_y:None
        height:120
        padding:[main_win.space_x+110,0]
        spacing:50
        orientation:'vertical'

        RoundedButtonType1:
            text:'Change Theme'
            font_size:25
            bold:True
            id:changetheme_btn
            size_hint_y:None
            height:60
        
        RoundedButtonType1:
            text:'Mail Account'
            font_size:25
            bold:True
            id:mailacc_btn
            size_hint_y:None
            height:60


    Label:
        size_hint_y:None
        height:353


<ChangeTheme>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    fg_color_bxlayout:fg_color_bxlayout
    txt_color_bxlayout:txt_color_bxlayout

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos
    
    Label:
        size_hint_y:None
        height:340
    
    BoxLayout:

        size_hint_y:None
        spacing:20
        height:200

        BoxLayout:
            id:fg_color_bxlayout
            orientation:'vertical'
            spacing:30
            size_hint_y:None
            height:200

            Label:
                text:'Foreground Color'
                size_hint_y:None
                height:30
                color:(0,0,0,1)
                bold:True

        BoxLayout:
            id:txt_color_bxlayout
            orientation:'vertical'
            spacing:30
            size_hint_y:None
            height:200

            Label:
                text:'Text Color'
                size_hint_y:None
                height:30
                color:(0,0,0,1)
                bold:True

    Label:
        size_hint_y:None
        height:100

    Label:
        size_hint_y:None
        height:224
                

            
<MailAccountPage>:

    orientation:'vertical'
    id:main_win
    space_x:self.size[0]/3

    submit_btn:submit_btn
    gdlayout1:gdlayout1

    canvas.before:
        Color:
            rgba:(236/255, 240/255, 241/255,1)
        Rectangle:
            size:self.size
            pos:self.pos


    Label:
        size_hint_y:None
        height:261

    BoxLayout:

        size_hint_y:None
        height:200

        Label:
            size_hint_x:0.20

        GridLayout:

            size_hint_x:0.5
            cols:2
            id:gdlayout1
            spacing:[0,20]

        Label:
            
            size_hint_x:0.3

    Label:
        size_hint_y:None
        height:80

    BoxLayout:

        size_hint_y:None
        height:40
        padding:[main_win.space_x+90,0]

        RoundedButtonType1:
            text:'Submit'
            id:submit_btn

    Label:
        size_hint_y:None
        height:283


<popup_logout_confirmation>:

    title:'Logout'
    title_color:[0,0,0,1]
    title_align:'center'
    title_size:20
    size_hint:(None,None)
    size:(400,400)

    logout_btn:logout_btn
    cancel_btn:cancel_btn

    separator_color:app.fnt_fg_color
    background:'./App/Data/Atlas/white_popup/white'

    BoxLayout:

        orientation:'vertical'
        
        Label:
            size_hint_y:0.13

        Label:
            size_hint_y:0.4
            text:"Are you sure to logout ?"
            color:(0,0,0,1)
            font_size:20

        Label:
            size_hint_y:0.25

        BoxLayout:
           
            id:bxlayout
            size_hint_y:0.15
            
            Label:
                size_hint_x:None
                width:40

            RoundedButtonType1:
                size_hint_x:None
                width:120
                id:logout_btn
                text:'Logout'
                bold:True
                on_press:root.logout()

            Label:
                size_hint_x:None
                width:60

            RoundedButtonType1:
                id:cancel_btn
                size_hint_x:None
                width:120
                text:'Cancel'
                bold:True
                on_release:root.dismiss()

            Label:
                size_hint_x:None
                width:50

        Label:
            size_hint_y:0.07
'''




Builder.load_string(kv_file)






def secfetch(x):
    d={'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i'}
    return d[x]

local_storage_theme = JsonStore('./App/Data/Theme/theme.json')
local_storage_mail_service = JsonStore('./App/Data/User/Mail_Service/mail_service.json')

if local_storage_theme.exists('theme_list'):
    theme_fg=local_storage_theme.get('theme_list')['theme_fg']
    theme_txt=local_storage_theme.get('theme_list')['theme_txt']

else:
    local_storage_theme.put('theme_list',theme_fg=[82/255, 179/255, 217/255, 1],theme_txt=[0,0,0,1])
    theme_fg=[82/255, 179/255, 217/255, 1]
    theme_txt=[0,0,0,1]

if local_storage_mail_service.exists('login_data'):
    mail_service_username=local_storage_mail_service.get('login_data')['username']
    mail_service_password=local_storage_mail_service.get('login_data')['password']

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RoundedButtonType1(Button):
    pass

class RoundedButtonType2Left(Button):
    pass

class RoundedButtonType2Right(Button):
    pass

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

class MainWindow(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)


        pass

class WelcomePage(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.switchnext,2.35)

    def switchnext(self,*_):
        app_ref.scmanager_main.transition = RiseInTransition()
        app_ref.scmanager_main.current="Login_Page"
        
class popup_exit(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    def closeapp(self,*_):
        self.dismiss()
        App.get_running_app().stop()
        Window.close()

class LoginPage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.btn.bind(on_press=self.login_task)
        self.btn_signup.bind(on_press=self.signup_task)
        self.exit_btn.bind(on_press=self.exitpp)

        self.btn.text='Login'
        self.btn_signup.text='Sign Up'
        self.username.text=''
        self.passwd.text=''
                 
    def exitpp(self,*_):
        
        exitpopup= popup_exit()
        exitpopup.open()
        

    def login_task(self,*_):
        username=self.username.text
        passwd=self.passwd.text
        try:
            global a
            a=sql.connect(host='localhost',user='root',passwd='{}'.format(passwd),database='{}'.format(username))
            global cur
            cur=a.cursor()
            if (a.is_connected()):
                app_ref.after_login.update_text("Welcome Back {} !".format(username.capitalize()),username)
                app_ref.scmanager_main.transition = SlideTransition(direction="left")
                app_ref.scmanager_main.current= "After_Login"
                
                self.btn.text='Login'
                self.btn_signup.text='Sign Up'
                self.username.text=''
                self.passwd.text=''
        except:
            app_ref.login_page.update_btn()

    def signup_task(self,*_):
        username=self.username.text
        passwd=self.passwd.text

        try:
            a=sql.connect(host='localhost',user='root',passwd='{}'.format(passwd),database='{}'.format(username))
            if (a.is_connected()):
                app_ref.login_page.update_signup_button(self,*_)
                a.close()
        except:
            try:
                a=sql.connect(host='localhost',user='root',passwd='{}'.format(passwd))
                cur=a.cursor()
                if (a.is_connected()):
                    app_ref.scmanager_main.transition = SlideTransition(direction="left")
                    app_ref.scmanager_main.current="SignUp_Page"
                    
                    self.btn.text='Login'
                    self.btn_signup.text='Sign Up'
                    a.close()
                    
            except sql.Error as err:
                print('error code: ',err.errno)
                if err.errno==1045:
                    app_ref.login_page.update_signup_btn_null_password()
        
    def update_signup_btn_null_password(self,*_):

        self.btn_signup.text='No/Incorrect Password Entered'

    def update_btn(self,*_):
        
        self.btn.text="Try Again"

    def update_signup_button(self,*_):
        self.btn_signup.text="Account Exists, Please Login Instead"
    
    def display_time(self,dt):
        self.display_time.text=dt

class SignUpPage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.cont.bind(on_press=self.continu)

    def continu(self,*_):
        app_ref.scmanager_main.transition = SlideTransition(direction="left")
        app_ref.scmanager_main.current="Database_Configuration_Page"
        

class DatabaseConfigurationPage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.submit_btn.bind(on_press=self.configure)

    def continu(self,*_):

        global theme_fg
        
        self.bxlayout.clear_widgets()
        self.bxlayout.add_widget(Button(id='submit_btn',text='Submit',size_hint_y=None,height=40,background_color=theme_fg,background_normal=''))
        app_ref.scmanager_main.transition = SlideTransition(direction="left")
        app_ref.scmanager_main.current="Login_Page"
        
        
    def configure(self,*_):

        global theme_fg
        
        if len(self.highest_class.text)!=2:
            self.highest_class.text="Enter valid input"
            return
        
        if len(self.highest_section.text)!=1:
            self.highest_section.text="Enter valid input"
            return
        
        h_class=self.highest_class.text
        h_section=self.highest_section.text
        username=app_ref.login_page.username.text
        password=app_ref.login_page.passwd.text

        win_notification("School Manager","Please wait till the database\nis configured for use",duration=4)
        win_notification("School Manager","It is recommended not to use the\napp during this time\nIt might crash",duration=4)
        call=dbconfiguration.config(username,password,h_class,h_section)
        
        if call=='Success':

            win_notification("School Manager","Database configured successfully",duration=3)
            self.bxlayout.clear_widgets()
            self.bxlayout.add_widget(Button(text='Continue',size_hint_y=None,height=40,on_press=self.continu,background_color=theme_fg,background_normal=''))

        else:

            win_notification("School Manager","Something went wrong",duration=4)
            
class AfterLogin(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.btn.bind(on_press=self.afterlogin_task)

    def update_text(self,message,usernam):
        
        self.login_stat.text=message
    
    def afterlogin_task(self,*_):
        app_ref.scmanager_main.transition = SlideTransition(direction="left")
        app_ref.scmanager_main.current= "App_Interface_Page"
        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current= "Home_Page"

class AppInterfaceNavBar(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        pass

class AppInterfaceWindow(BoxLayout):

    app_interface_nav_bar = ObjectProperty()
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

class HomePage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.student_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Student_Section"))
        self.teacher_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Teacher_Section"))
        self.othersection_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Other_Section"))
        

class StudentSection(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.fetch_std_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Fetch_Student"))
        self.fetch_class_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Fetch_Class"))
        self.add_student_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Add_Student"))
        self.remove_student_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Remove_Student"))
        
        
class popup_updatestudentperformance(Popup):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.update_btn.bind(on_press=self.update)
        self.cancel_btn.bind(on_press=self.cancel)

        self.form_name = app_ref.fetch_std.form_name.text
        self.title="EDIT"
        
        self.local_storage_performance = app_ref.fetch_std.local_storage_performance
        
        if self.local_storage_performance.exists("performance"):
            self.subjects=self.local_storage_performance.get("performance")["subjects"]
            self.this_test_dict=self.local_storage_performance.get("performance")["this_test"]
            self.previous_test_dict=self.local_storage_performance.get("performance")["previous_test"]
            self.this_test_max_marks_dict=self.local_storage_performance.get("performance")["this_test_max_marks"]
            self.previous_test_max_marks_dict=self.local_storage_performance.get("performance")["previous_test_max_marks"]
            

        for i in range(len(self.subjects)):

            subject=self.subjects[i]

            this_test_marks=self.this_test_dict[subject]
            previous_test_marks=self.previous_test_dict[subject]
            this_test_max_marks=self.this_test_max_marks_dict[subject]
            previous_test_max_marks=self.previous_test_max_marks_dict[subject]
             
            self.gdlayout.add_widget(Label(text='{}'.format(subject.upper()), color=[0,0,0,1], bold=True, size_hint_y=None, height=50, font_size=25))
            self.gdlayout.add_widget(Label(text='', size_hint_y=None, height=50))

            self.gdlayout.add_widget(Label(text='This Test Marks', size_hint_y=None, height=30, color=[0,0,0,1]))
            self.gdlayout.add_widget(TextInput(multiline=False, write_tab=False))

            self.gdlayout.add_widget(Label(text='Maximum Marks', size_hint_y=None, height=30, color=[0,0,0,1]))
            self.gdlayout.add_widget(TextInput(multiline=False, write_tab=False))

            self.gdlayout.add_widget(Label(text='Previous Test Marks', size_hint_y=None, height=30, color=[0,0,0,1]))
            self.gdlayout.add_widget(TextInput(text='{}'.format(str(this_test_marks)), multiline=False, write_tab=False))

            self.gdlayout.add_widget(Label(text='Maximum Marks', size_hint_y=None, height=30, color=[0,0,0,1]))
            self.gdlayout.add_widget(TextInput(text='{}'.format(str(this_test_max_marks)), multiline=False, write_tab=False))

            self.gdlayout.add_widget(Label(text='', size_hint_y=None, height=40))
            self.gdlayout.add_widget(Label(text='', size_hint_y=None, height=40))
              
    def update(self,*_):

        subject=self.subjects
        this_test_marks_indxlst=[3,15,27,39,51,63,75,87,99]
        this_test_max_marks_indxlst=[5,17,29,41,53,65,77,89,101]
        previous_test_marks_indxlst=[7,19,31,43,55,67,79,91,103]
        previous_test_max_marks_indxlst=[9,21,33,45,57,69,81,93,105]

        ctr1_dict={}
        ctr2_dict={}
        ctr3_dict={}
        ctr4_dict={}

        local_storage_performance= app_ref.fetch_std.local_storage_performance
        gdlayout_children_list=self.gdlayout.children
        gdlayout_children_list.reverse()
        
        for i in range(len(self.subjects)):

            subject=self.subjects[i]
            
            ctr1_dict["{}".format(subject)]=gdlayout_children_list[this_test_marks_indxlst[i]].text
            ctr2_dict["{}".format(subject)]=gdlayout_children_list[this_test_max_marks_indxlst[i]].text
            ctr3_dict["{}".format(subject)]=gdlayout_children_list[previous_test_marks_indxlst[i]].text
            ctr4_dict["{}".format(subject)]=gdlayout_children_list[previous_test_max_marks_indxlst[i]].text

        local_storage_performance.put('performance',subjects=list(self.subjects),this_test=dict(ctr1_dict),previous_test=dict(ctr3_dict),this_test_max_marks=dict(ctr2_dict),previous_test_max_marks=dict(ctr4_dict))
        self.dismiss()
        win_notification("School Manager","Result updated successfully",duration=3)
        
          
    def cancel(self,*_):

        self.dismiss()
    
class FetchStudentDetails(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.submit_btn.bind(on_press=self.fetch_details)

    def clear_form(self,*_):

        self.form_stdid.text=''
        self.form_name.text=''
        self.form_class.text=''
        self.form_rollno.text=''
        self.form_phno.text=''
        self.form_attendance.text=''
        self.form_fname.text=''
        self.form_mname.text=''
        self.form_aadhar_num.text=''
        self.form_email.text=''
        self.form_dob.text=''
        self.form_age_gender.text=''

        self.subject_label.text=''
        self.performance_suggestion_box.text=''

        if len(self.image_gdlayout.children)==0:
            pass
        else:
            self.image_gdlayout.clear_widgets()

        if len(self.bxlayout3.children)==0:
            pass
        else:
            self.bxlayout3.clear_widgets()
        
        if len(self.bxlayout4.children)==0:
            pass
        else:
            self.bxlayout4.clear_widgets()

        if len(self.bxlayout5.children)==0:
            pass
        else:
            self.bxlayout5.clear_widgets()
        
    def back(self,*_):
        
        self.submit_btn.text='Submit'
        self.student_id.text=''

        self.scrollview.scroll_y=1
        
        self.clear_form()
        
        if len(self.bxlayout3.children)==0:
            pass
        else:
            self.bxlayout3.clear_widgets()

        if len(self.bxlayout5.children)==0:
            pass
        else:
            self.bxlayout5.clear_widgets()
        
    def update_textarea(self,std_id):
        self.student_id.text=std_id
        
    def fetch_details(self,*_):
        
        global theme_fg
        std_id=self.student_id.text
        
        self.gdlayout.bind(minimum_height=self.gdlayout.setter('height'))
        
        if len(std_id)!=12:
            self.submit_btn.text='Invalid ID'
            self.clear_form()
            return
          
        if std_id[2]=='0':
            self.submit_btn.text='Invalid ID'
            self.clear_form()
            return
            
        if std_id[0]=='9':
            clas_s='9'+std_id[1]
                
        else:
            clas_s=std_id[:2]
            
        if len(self.bxlayout3.children)==0:
            pass
        else:
            self.bxlayout3.clear_widgets()

        if len(self.bxlayout4.children)==0:
            pass
        else:
            self.bxlayout4.clear_widgets()

        if len(self.bxlayout5.children)==0:
            pass
        else:
            self.bxlayout5.clear_widgets()

        self.submit_btn.text='Submit'
        sec=secfetch(str(std_id[2]))
        self.class_sec=clas_s+sec
        cur.execute('select student_id,name,class_sec,roll_no,ph_no,attendance,f_name,m_name,aadhar_num,email_id,shift,dob,age,gender from {} where student_id={}'.format(self.class_sec,std_id))
        i=cur.fetchall()
        if len(i)==0:
            self.submit_btn.text='No Student Found'
            self.clear_form()
            return
        self.subject_label.text=''
        self.performance_suggestion_box.text=''
        lst=i[0]
        self.form_stdid.text=str(lst[0])
        self.form_name.text=str(lst[1])
        self.form_class.text=str(lst[2])+"   ( {} Shift )".format(lst[10])
        self.form_rollno.text=str(lst[3])
        self.form_phno.text=str(lst[4])
        self.form_attendance.text=str(lst[5])
        self.form_fname.text=str(lst[6])
        self.form_mname.text=str(lst[7])
        self.form_aadhar_num.text=str(lst[8])
        self.form_email.text=str(lst[9])
        self.form_dob.text=str(lst[11])
        self.form_age_gender.text=str(lst[12])+",    "+str(lst[13])
        image_gdlayout=Image(source="./App/Data/Student/{}/{}/student.jpg".format(self.class_sec,self.student_id.text),size=[230,230])
        self.image_gdlayout.add_widget(image_gdlayout)
        form_vdr=RoundedButtonType1(text='View Detailed Report',on_press=self.forward)
        self.bxlayout3.add_widget(form_vdr)
            
        
    def forward(self,*_):
        
        self.bxlayout3.children[0].disabled=True
        
        try:
            self.local_storage_performance=JsonStore("./App/Data/Student/{}/{}/performance.json".format(self.class_sec,self.student_id.text))

        except:
            win_notification("School Manager","{} data not available".format(self.form_name.text),duration=3)
            return
        
        self.bxlayout4.add_widget(Label(text="PERFORMANCE",font_size=36,size_hint_y=None,height=70,color=(0,0,0,1)))
        self.bxlayout4.add_widget(Label(text='',size_hint_y=None,height=40))
        self.bxlayout4.add_widget(Label(text="Recent Test ",font_size=22,bold=True,size_hint_y=None,height=50,color=(0,0,0,1)))
        self.bxlayout4.add_widget(Label(text='',size_hint_y=None,height=30))
        
        result_gdlayout=GridLayout(cols=5,spacing=[8,20])

        lst=['Subject','Marks','Current Percentage','Previous Percentage','Percentage Factor']
        for i in lst:
            result_gdlayout.add_widget(Label(text="{}".format(i),size_hint_x=0.2,size_hint_y=None,height=30,color=(0,0,0,1)))


        if self.local_storage_performance.exists("performance"):
            subjects=self.local_storage_performance.get("performance")["subjects"]
            this_test_dict=self.local_storage_performance.get("performance")["this_test"]
            previous_test_dict=self.local_storage_performance.get("performance")["previous_test"]
            this_test_max_marks_dict=self.local_storage_performance.get("performance")["this_test_max_marks"]
            previous_test_max_marks_dict=self.local_storage_performance.get("performance")["previous_test_max_marks"]
            
        else:
            return
        for i in range(len(subjects)):

            subject=subjects[i]
            this_test_marks=int(this_test_dict[subject])
            previous_test_marks=int(previous_test_dict[subject])
            this_test_max_marks=int(this_test_max_marks_dict[subject])
            previous_test_max_marks=int(previous_test_max_marks_dict[subject])
            
            container=score_analyzer.percentage(this_test_marks,previous_test_marks,this_test_max_marks,previous_test_max_marks)

            this_test_percentage=float(container[0])
            previous_test_percentage=float(container[1])
            performance_factor=float(container[2])

            result_gdlayout.add_widget(Button(text="{}".format(subject),size_hint_x=0.2,size_hint_y=None,on_press=partial(self.detail_label,subject),background_color=(236/255, 240/255, 241/255,1),background_normal='',height=30,color=(0,0,0,1)))
            result_gdlayout.add_widget(Label(text="{}".format(this_test_marks),size_hint_x=0.2,size_hint_y=None,height=30,color=(0,0,0,1)))
            result_gdlayout.add_widget(Label(text="{}".format(this_test_percentage),size_hint_x=0.2,size_hint_y=None,height=30,color=(0,0,0,1)))
            result_gdlayout.add_widget(Label(text="{}".format(previous_test_percentage),size_hint_x=0.2,size_hint_y=None,height=30,color=(0,0,0,1)))
            
            if performance_factor>0:
                result_gdlayout.add_widget(Label(text="+{}".format(performance_factor),size_hint_x=0.2,size_hint_y=None,height=30,color=(0,1,0,1)))
            elif performance_factor<0:
                result_gdlayout.add_widget(Label(text="{}".format(performance_factor),size_hint_x=0.2,size_hint_y=None,height=30,color=(1,0,0,1)))
            else:
                result_gdlayout.add_widget(Label(text="{}".format(performance_factor),size_hint_x=0.2,size_hint_y=None,height=30,color=(0,0,0,1)))
        
        self.bxlayout4.add_widget(result_gdlayout)

        self.bxlayout5.add_widget(RoundedButtonType1(text='Edit',on_press=self.update_performance))

    def update_performance(self,*_):

        updatestudentperformance_popup = popup_updatestudentperformance()
        updatestudentperformance_popup.open()
    
    def detail_label(self,subject,*args):

        self.subject_label.text=str(subject)

        try:
            local_storage_subject_suggestion=JsonStore("./App/Data/Student/Subjects/{}/{}.json".format(subject,subject))
        except:
            return
        if local_storage_subject_suggestion.exists("Suggestion"):
            self.performance_suggestion_box.text=local_storage_subject_suggestion.get("Suggestion")
        else:
            self.performance_suggestion_box.text=''

class FetchClassWise(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
        
        self.gdlayout.bind(minimum_height=self.gdlayout.setter('height'))

    def back(self,*_):

        global FetchClassWise_submit
        global FetchClassWise_submit_cont

        FetchClassWise_submit=['']
        FetchClassWise_submit_cont=0
        
        if len(self.gdlayout.children)==0:
            pass
        else:
            self.gdlayout.clear_widgets()
        
        
    def select_student(self,std_id,random):
        app_ref.fetch_std.update_textarea(str(std_id))
        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current='Fetch_Student'
        

    def submit(self,*_):
        global FetchClassWise_submit
        global FetchClassWise_submit_cont

        entered_class=self.enter_class_txt.text
        entered_class_bfr=int(entered_class)
        if entered_class_bfr<10:
            entered_class='9'+entered_class
        entered_section=self.enter_section_txt.text.lower()
        bffr=str(entered_class)+str(entered_section)

        if len(self.gdlayout.children)==0:
            pass
        else:
            self.gdlayout.clear_widgets()
            
        cur.execute("select student_id,name,class_sec,roll_no,ph_no,attendance from {} where name!='dummy' order by roll_no".format(bffr))
        bffr1=[i for i in cur]
        if len(bffr1)==0:
            pass
        else:    
            for i in range(len(bffr1)):
                bffr2=list(bffr1[i])
                for j in range(len(bffr2)):
                    bffr3=bffr2[j]
                    if j==1 or j==5:
                        if j==1:
                            student_id=bffr2[0]
                            self.gdlayout.add_widget(Button(text=str(bffr3),height=50,on_press=partial(self.select_student,student_id),size_hint_y=None,color=[0,0,0,1],background_normal='',background_color=[236/255, 240/255, 241/255,1]))
                        if j==5:
                            student_id=bffr2[0]
                            attendance=bffr2[5]
                            self.gdlayout.add_widget(Button(text=str(bffr3),height=50,on_press=partial(self.student_attendance,bffr,student_id,attendance),size_hint_y=None,color=[0,0,0,1],background_normal='',background_color=[236/255, 240/255, 241/255,1]))
                    else:
                        self.gdlayout.add_widget(Label(text=str(bffr3),height=50,size_hint_y=None,color=[0,0,0,1]))

    def student_attendance(self,class_sec,student_id,attendance,*args):

        self.atdpp_student_id=student_id
        self.atdpp_attendace=attendance
        self.atdpp_class_sec=class_sec
        
        popupattendance=attendance_popup()
        popupattendance.open()
        
    
class attendance_popup(Popup):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.total=210
        self.student_id=app_ref.fetch_class.atdpp_student_id
        self.student_label.text="Student ID:  " + str(self.student_id)
        self.attendance=app_ref.fetch_class.atdpp_attendace
        self.update_attendance_label()
        self.class_sec=app_ref.fetch_class.atdpp_class_sec
        
        self.attendance_list=self.attendance.split("/")
        self.present=int(self.attendance_list[0])    
    
    def update_attendance_label(self,*_):

        self.attendance_label.text="Attendance:  " + self.attendance
    
    def add(self,*_):

        if self.present+1>210:
            return
        else:
            pass
        self.present+=1
        self.attendance=str(self.present)+"/"+str(self.total)
        self.update_attendance_label()
        cur.execute("update {} set attendance='{}' where student_id={}".format(self.class_sec,self.attendance,self.student_id))
        a.commit()
        
    def cancel(self,*_):

        app_ref.fetch_class.submit(FetchClassWise)
        self.dismiss()
        
class popup_exit_without_saving_AddStudent(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.ex_btn.bind(on_press=self.back)

    def back(self,instance):
        
        AddStudent.clear_form(self)
        app_ref.scmanager.current='Student_Section'
        self.dismiss()
        

class AddStudent(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
        self.student_id_label= Label(text='Student ID', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.student_id_label)
        
        self.gdlayout.student_id= TextInput(allow_copy=False, multiline=False, write_tab=False, input_filter=(lambda text, from_undo: text[:12 - len(self.gdlayout.student_id.text)]))
        self.gdlayout.add_widget(self.gdlayout.student_id)
        
        self.name_label= Label(text='Name', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.name_label)
        
        self.gdlayout.name= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.name)
        
        self.age_label= Label(text='Age', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.age_label)
        
        self.gdlayout.age= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.age)
        
        self.gender_label= Label(text='Gender', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.gender_label)
        
        self.gdlayout.gender= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.gender)
        
        self.aadhar_num_label= Label(text='Aadhar Number', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.aadhar_num_label)
        
        self.gdlayout.aadhar_num= TextInput(multiline=False, write_tab=False, hint_text='Enter 12 digit AADHAR number', input_filter=(lambda text, from_undo: text[:12 - len(self.gdlayout.aadhar_num.text)]))
        self.gdlayout.add_widget(self.gdlayout.aadhar_num)
        
        self.ph_no_label= Label(text='Phone Number', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.ph_no_label)
        
        self.gdlayout.ph_no= TextInput(hint_text='Enter 10 digit mobile number', multiline=False, write_tab=False, input_filter=(lambda text, from_undo: text[:10 - len(self.gdlayout.ph_no.text)]))
        self.gdlayout.add_widget(self.gdlayout.ph_no)
        
        self.dob_label= Label(text='Date Of Birth', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.dob_label)
        
        self.gdlayout.dob= TextInput(multiline=False, write_tab=False, hint_text='e.g.  14-08-2018')
        self.gdlayout.add_widget(self.gdlayout.dob)
        
        self.std_class_label= Label(text='Class', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.std_class_label)
        
        self.gdlayout.std_class= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.std_class)
        
        self.section_label= Label(text='Section', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.section_label)
        
        self.gdlayout.section= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.section)
        
        self.shift_label= Label(text='Shift', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.shift_label)
        
        self.gdlayout.shift= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.shift)
        
        self.email_id_label= Label(text='Email ID', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.email_id_label)
        
        self.gdlayout.email_id= TextInput(multiline=False, write_tab=False, hint_text='e.g. xyz@gmail.com')
        self.gdlayout.add_widget(self.gdlayout.email_id)
        
        self.f_name_label= Label(text="Father's Name", color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.f_name_label)
        
        self.gdlayout.f_name= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.f_name)
        
        self.m_name_label= Label(text="Mother's Name", color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.m_name_label)
        
        self.gdlayout.m_name= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.m_name)
        

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        
        
    def back(self,*_):
        
        
        self.gdlayout.student_id.text = ''
        self.gdlayout.name.text = ''
        self.gdlayout.age.text=''
        self.gdlayout.gender.text=''
        self.gdlayout.dob.text=''
        self.gdlayout.ph_no.text=''
        self.gdlayout.std_class.text=''
        self.gdlayout.section.text=''
        self.gdlayout.shift.text=''
        self.gdlayout.email_id.text=''
        self.gdlayout.aadhar_num.text=''
        self.gdlayout.f_name.text=''
        self.gdlayout.m_name.text=''
        self.submit_btn.text='Submit'
        

    def submit(self,*_):
    
        if len(self.gdlayout.student_id.text)!=12:
            self.gdlayout.student_id.text='Enter valid ID'
            return
        else:
            
            if self.gdlayout.student_id.text[2]=='0':
                self.gdlayout.student_id.text="Enter valid ID"
                return
            else:
                pass
            name=str(self.gdlayout.name.text)
            age=int(self.gdlayout.age.text)
            gender=str(self.gdlayout.gender.text)
            dob=str(self.gdlayout.dob.text)
            ph_no=int(self.gdlayout.ph_no.text)
            std_class=self.gdlayout.std_class.text
            if int(std_class)<10:
                std_class_bfr='9'+std_class
            else:
                std_class_bfr=std_class
            section=self.gdlayout.section.text
            class_sec=str(std_class+" "+section.upper())
            class_sec_lower=str(std_class_bfr+section.lower())
            shift=str(self.gdlayout.shift.text)
            email_id=str(self.gdlayout.email_id.text)
            aadhar_num=int(self.gdlayout.aadhar_num.text)
            f_name=str(self.gdlayout.f_name.text)
            m_name=str(self.gdlayout.m_name.text)
            if self.gdlayout.student_id.text[10]==0:
                roll_no=int(self.gdlayout.student_id.text[11])
            else:
                roll_no=int(self.gdlayout.student_id.text[10:12])
            attendance='0/210'
            student_id=int(self.gdlayout.student_id.text)

            try:
                cur.execute("insert into {} values ({},'{}',{},'{}',{},{},'{}','{}','{}','{}','{}','{}','{}',{})".format(class_sec_lower,student_id,name,age,gender,aadhar_num,ph_no,dob,class_sec,shift,email_id,f_name,m_name,attendance,roll_no))
                cur.execute("insert into id_contact values({},'{}',{},{})".format(student_id,email_id,ph_no,aadhar_num))
                cur.execute("insert into library_user_database values ('{}',{},'','','')".format(name,student_id))
                a.commit()
                
                try:
                    if os.path.exists("./App/Data/Student/{}/{}".format(class_sec_lower,student_id))==True:
                        pass
                    else:
                        os.makedirs("./App/Data/Student/{}/{}".format(class_sec_lower,student_id))
                except:
                    print("Error creating directory App/Data/Student/{}/{}".format(class_sec_lower,student_id))
                    
                win_notification('School Manager','New Student Added Successfully'+'\n{}'.format(name)+'\n{}'.format(class_sec))
                self.submit_btn.text='Student Added Successfully'

            except:
                win_notification('School Manager','Cannot add new student'+'\n{}'.format(name)+'\n{}'.format(class_sec)+'\nSomething went wrong')
                win_notification('School Manager','Please verify the details and try again') 


class RemoveStudent(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
        self.delete_btn.bind(on_press=self.delete_record)
        self.delete_btn.text='Delete Records'
        self.delete_btn.disabled=True

        
    def submit(self,*_):

        self.remove_id=self.std_id.text

        if len(self.std_id.text)!=12:
            self.std_id.text='Enter valid ID'
            return
        else:
            
            if self.std_id.text[2]=='0':
                self.std_id.text="Enter valid ID"
                return
            
            else:
                cur.execute("select exists(select * from id_contact where id={})".format(self.std_id.text))
                check_bfr = cur.fetchall()
                check_bfr_1 = check_bfr[0]
                check_bfr_2 = check_bfr_1[0]
                if check_bfr_2 == 0:
                    win_notification("School Manager","ID not found in records",duration=3)
                    return
                self.class_sec=str(self.remove_id[0:2])+str(secfetch(self.remove_id[2]))
                cur.execute("select name,class_sec,roll_no,ph_no,f_name,m_name,attendance from {} where student_id={}".format(self.class_sec,self.remove_id))
                lst=cur.fetchall()
                i=lst[0]
                self.form_stdid.text=str(self.remove_id)
                self.form_name.text=i[0]
                self.form_class.text=i[1]
                self.form_rollno.text=str(i[2])
                self.form_phno.text=str(i[3])
                self.form_fname.text=i[4]
                self.form_mname.text=i[5]
                self.form_attendance.text=i[6]
                self.delete_btn.disabled=False
        
    def delete_record(self,*_):
        
        cur.execute("delete from {} where student_id={}".format(self.class_sec,self.remove_id))
        cur.execute("delete from id_contact where id={}".format(self.remove_id))
        cur.execute("delete from library_user_database where id={}".format(self.remove_id))
        a.commit()
        
        try:
            if os.path.exists("./App/Data/Student/{}/{}".format(self.class_sec,self.remove_id))==True:
                shutil.rmtree("./App/Data/Student/{}/{}".format(self.class_sec,self.remove_id))
        except:
            print("Error deleting directory App/Data/Student/{}/{}".format(self.class_sec,self.remove_id))
            
        self.delete_btn.text='Successful'
        win_notification('School Manager','Student Record Deleted Successfully'+'\n{}'.format(self.form_name.text)+'\n{}'.format(self.form_class.text))

    def back(self,*_):

        self.std_id.text=''
        self.delete_btn.text='Delete Records'
        self.delete_btn.disabled=True
        self.form_stdid.text=''
        self.form_name.text=''
        self.form_class.text=''
        self.form_rollno.text=''
        self.form_phno.text=''
        self.form_fname.text=''
        self.form_mname.text=''
        self.form_attendance.text=''
        
        
class TeacherSection(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.fetch_teacherlist_btn.bind(on_press=self.fetch_teacher)
        self.add_teacher_btn.bind(on_press=self.add_teacher)
        self.remove_teacher_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Remove_Teacher"))

    def fetch_teacher(self,*_):

        app_ref.fetch_teacherlist.fetch()
        app_ref.app_interface_change_screen("Fetch_TeacherList")
        
        
    def add_teacher(self,*_):

        cur.execute('select t_id from teachers order by t_id desc limit 1')
        lc=cur.fetchall()
        i=lc[0]
        bfr_t_id=str(i[0]+1)
        app_ref.add_teacher.gdlayout.t_id.text=bfr_t_id

        app_ref.app_interface_change_screen("Add_Teacher")
        



class FetchTeacherList(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        pass
        
    def back(self,*_):

        self.gdlayout1.clear_widgets()
        
    def fetch(self,*_):
        cur.execute("select t_id,name,age,ph_no,email_id,t_subject,class_teacher,salary from teachers where t_id!=1000000000000")
        bffr1=[i for i in cur]
        if len(bffr1)==0:
            pass
        else:    
            for i in range(len(bffr1)):
                bffr2=list(bffr1[i])
                for j in range(len(bffr2)):
                    bffr3=bffr2[j]
                    if j==1:
                        teacher_id=bffr2[0]
                        self.gdlayout1.add_widget(Button(text=str(bffr3),height=50,on_press=partial(self.select_teacher,teacher_id),size_hint_y=None,color=[0,0,0,1],background_normal='',background_color=[236/255, 240/255, 241/255,1]))
                    else:
                        self.gdlayout1.add_widget(Label(text=str(bffr3),height=50,size_hint_y=None,color=[0,0,0,1]))
            
    def select_teacher(self,teacher_id,*args):
        
        pass


class AddTeacher(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
        self.t_id_label= Label(text='Teacher ID', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.t_id_label)
        
        self.gdlayout.t_id= TextInput(allow_copy=False, multiline=False, write_tab=False, input_filter=(lambda text, from_undo: text[:13 - len(self.gdlayout.t_id.text)]))
        self.gdlayout.add_widget(self.gdlayout.t_id)
        
        self.name_label= Label(text='Name', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.name_label)
        
        self.gdlayout.name= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.name)
        
        self.age_label= Label(text='Age', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.age_label)
        
        self.gdlayout.age= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.age)
        
        self.gender_label= Label(text='Gender', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.gender_label)
        
        self.gdlayout.gender= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.gender)
        
        self.ph_no_label= Label(text='Phone Number', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.ph_no_label)
        
        self.gdlayout.ph_no= TextInput(hint_text='Enter 10 digit mobile number', multiline=False, write_tab=False, input_filter=(lambda text, from_undo: text[:10 - len(self.gdlayout.ph_no.text)]))
        self.gdlayout.add_widget(self.gdlayout.ph_no)
        
        self.dob_label= Label(text='Date Of Birth', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.dob_label)
        
        self.gdlayout.dob= TextInput(multiline=False, write_tab=False, hint_text='e.g.  14-08-2018')
        self.gdlayout.add_widget(self.gdlayout.dob)

        self.email_id_label= Label(text='Email ID', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.email_id_label)
        
        self.gdlayout.email_id= TextInput(multiline=False, write_tab=False, hint_text='e.g. xyz@gmail.com')
        self.gdlayout.add_widget(self.gdlayout.email_id)

        self.aadhar_num_label= Label(text='Aadhar Number', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.aadhar_num_label)
        
        self.gdlayout.aadhar_num= TextInput(multiline=False, write_tab=False, hint_text='Enter 12 digit AADHAR number', input_filter=(lambda text, from_undo: text[:12 - len(self.gdlayout.aadhar_num.text)]))
        self.gdlayout.add_widget(self.gdlayout.aadhar_num)
        
        self.qualification_label= Label(text='Qualification', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.qualification_label)
        
        self.gdlayout.qualification= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.qualification)
        
        self.t_subject_label= Label(text='Teaching Subject', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.t_subject_label)
        
        self.gdlayout.t_subject= TextInput(multiline=False, write_tab=False)
        self.gdlayout.add_widget(self.gdlayout.t_subject)
        
        self.class_teacher_label= Label(text='Class Teacher', color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.class_teacher_label)

        self.gdlayout.class_teacher= TextInput(multiline=False, write_tab=False, hint_text=' ( if assigned ) ')
        self.gdlayout.add_widget(self.gdlayout.class_teacher)
        
        self.t_class_label= Label(text="Teaching Classes", color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.t_class_label)
        
        self.gdlayout.t_class= TextInput(multiline=False, write_tab=False, hint_text=' ( if assigned ) ')
        self.gdlayout.add_widget(self.gdlayout.t_class)
        
        self.salary_label= Label(text="Salary", color=[0,0,0,1], bold=True)
        self.gdlayout.add_widget(self.salary_label)
        
        self.gdlayout.salary= TextInput(multiline=False, write_tab=False, hint_text=' Minimum: Rs.15000 p.m')
        self.gdlayout.add_widget(self.gdlayout.salary)
        

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        

    def back(self,*_):

        self.gdlayout.t_id.text=''
        self.gdlayout.name.text=''
        self.gdlayout.age.text=''
        self.gdlayout.gender.text=''
        self.gdlayout.ph_no.text=''
        self.gdlayout.dob.text=''
        self.gdlayout.email_id.text=''
        self.gdlayout.aadhar_num.text=''
        self.gdlayout.qualification.text=''
        self.gdlayout.t_subject.text=''
        self.gdlayout.class_teacher.text=''
        self.gdlayout.t_class.text=''
        self.gdlayout.salary.text=''
        self.submit_btn.text='Submit'
        

    def submit(self,*_):

        t_id=self.gdlayout.t_id.text
        name=self.gdlayout.name.text
        age=self.gdlayout.age.text
        gender=self.gdlayout.gender.text
        ph_no=self.gdlayout.ph_no.text
        dob=self.gdlayout.dob.text
        email_id=self.gdlayout.email_id.text
        aadhar_num=self.gdlayout.aadhar_num.text
        qualification=self.gdlayout.qualification.text
        t_subject=self.gdlayout.t_subject.text
        class_teacher=self.gdlayout.class_teacher.text
        t_class=self.gdlayout.t_class.text
        salary=self.gdlayout.salary.text
        doj=datetime.now().strftime("%d-%m-%Y")
        
        try:
            cur.execute("insert into teachers values({},'{}',{},'{}',{},'{}','{}',{},'{}','{}','{}','{}',{},'{}')".format(t_id,name,age,gender,ph_no,dob,email_id,aadhar_num,qualification,t_subject,class_teacher,t_class,salary,doj))
            cur.execute("insert into id_contact values ({},'{}',{},{})".format(t_id,email_id,ph_no,aadhar_num))
            cur.execute("insert into library_user_database values ('{}',{},'','','')".format(name,t_id))
            a.commit()
            win_notification('School Manager','New Teacher Added Successfully'+'\n{}'.format(name)+'\n{}'.format(t_id))
            self.submit_btn.text='Teacher Added Successfully'

        except:
            win_notification('School Manager','Cannot add new teacher'+'\n{}'.format(name)+'\n{}'.format(t_id)+'\nSomething went wrong')
            win_notification('School Manager','Please verify the details and try again')
            

class RemoveTeacher(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
        self.delete_btn.bind(on_press=self.delete_record)
        self.delete_btn.disabled=True

    def clear_labels(self,*_):

        self.t_id_textinput.text=''
        self.delete_btn.text='Delete Records'
        self.t_id.text=''
        self.name.text=''
        self.gender.text=''
        self.age.text=''
        self.ph_no.text=''
        self.dob.text=''
        self.email_id.text=''
        self.aadhar_num.text=''
        self.qualification.text=''
        self.t_subject.text=''
        self.class_teacher.text=''
        self.t_class.text=''
        self.salary.text=''
        self.submit_btn.text="Submit"
        self.delete_btn.disabled=True
        

    def submit(self,*_):

        if len(self.t_id_textinput.text)==0:
            self.submit_btn.text="Invalid ID"
            return

        cur.execute("select exists(select * from id_contact where id={})".format(self.t_id_textinput.text))
        check_bfr = cur.fetchall()
        check_bfr_1 = check_bfr[0]
        check_bfr_2 = check_bfr_1[0]
        if check_bfr_2 == 0:
            win_notification("School Manager","ID not found in records",duration=3)
            self.clear_labels()
            return
                
        t_id=self.t_id_textinput.text

        cur.execute("select t_id,name,gender,age,ph_no,dob,email_id,aadhar_num,qualification,t_subject,class_teacher,t_class,salary from teachers where t_id={}".format(t_id))
        
        l=cur.fetchall()
        if len(l)==0:
            self.submit_btn.text="Invalid ID"
            self.clear_labels()
            return
        
        bfr=l[0]
        self.submit_btn.text="Submit"
        self.delete_btn.disabled=False
    
        self.t_id.text=str(bfr[0])
        self.name.text=bfr[1]
        self.gender.text=bfr[2]
        self.age.text=str(bfr[3])
        self.ph_no.text=str(bfr[4])
        self.dob.text=bfr[5]
        self.email_id.text=bfr[6]
        self.aadhar_num.text=str(bfr[7])
        self.qualification.text=bfr[8]
        self.t_subject.text=bfr[9]
        self.class_teacher.text=bfr[10]
        self.t_class.text=bfr[11]
        self.salary.text=str(bfr[12])

    def back(self,*_):

        self.clear_labels()
        
    def delete_record(self,*_):

        try:

            cur.execute("delete from teachers where t_id={}".format(self.t_id_textinput.text))
            cur.execute("delete from id_contact where id={}".format(self.t_id_textinput.text))
            cur.execute("delete from library_user_database where id={}".format(self.t_id_textinput.text))
            a.commit()
            self.delete_btn.text='Successful'
            win_notification('School Manager','Teacher Record Deleted Successfully'+'\n{}'.format(self.name.text)+'\n{}'.format(self.t_id_textinput.text))
            self.delete_btn.disabled=True
            
        except:

            pass

        
class OtherSection(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.push_notification_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Push_Notification"))
        self.main_members_btn.bind(on_press=self.main_members)
        self.library_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Library_Page"))
        
    def main_members(self,*_):

        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current='Main_Members'
        app_ref.main_members.update_label(MainMembers)
        

class MainMembers(BoxLayout):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)

        
    def update_label(self,*_):

        local_storage_school=JsonStore('./App/Data/School/school.json')

        if local_storage_school.exists('school'):

            school_label=local_storage_school.get('school')['school_name']

        if local_storage_school.exists('main_members'):

            principal_label=local_storage_school.get('main_members')['principal']
            vice_principal_label=local_storage_school.get('main_members')['vice_principal']
            
        self.school_label.text=school_label
        self.principal_label.text=principal_label
        self.vice_principal_label.text=vice_principal_label
        


class PushNotification(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.notif_indv_btn.bind(on_press=partial(app_ref.app_interface_change_screen,'Push_NotificationIndividual'))
        self.notif_grp_btn.bind(on_press=partial(app_ref.app_interface_change_screen,'Push_NotificationGroup'))
        self.notif_all_btn.bind(on_press=partial(app_ref.app_interface_change_screen,'Push_NotificationAll'))
        
    def pushnotificationindividual(self,*_):

        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current='Push_NotificationIndividual'
        

    def pushnotificationgroup(self,*_):

        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current='Push_NotificationGroup'
        
        
    def pushnotificationall(self,*_):

        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current='Push_NotificationAll'
        

class PushNotificationIndividual(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
    
        self.student_teacher_id_label= Label(text='Student/Teacher ID', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.student_teacher_id_label)
        
        self.student_teacher_id= TextInput(multiline=False, write_tab=False, input_filter=(lambda text, from_undo: text[:13 - len(self.student_teacher_id.text)]))
        self.gdlayout1.add_widget(self.student_teacher_id)

        self.subject_label= Label(text='Mail Subject', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.subject_label)
        
        self.subject= TextInput(multiline=True, write_tab=False)
        self.gdlayout1.add_widget(self.subject)

        self.message_label= Label(text='Message', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.message_label)
        
        self.message= TextInput(multiline=True, write_tab=False)
        self.gdlayout1.add_widget(self.message)

    def back(self,*_):

        self.student_teacher_id.text=''
        self.subject.text=''
        self.message.text=''
        self.submit_btn.text='Submit'
        

    def submit(self,*_):

        global mail_service_username
        global mail_service_password
        global school_name
        
        if self.student_teacher_id.text=='':

            self.student_teacher_id.text='Please enter student/teacher ID'
            return
        
        if self.subject.text=='':

            self.subject.text='Please enter mail subject'
            return

        if self.message.text=='':

            self.message.text='Please enter some message'
            return
        
        bfr_id=self.student_teacher_id.text
        cur.execute("select email_id from id_contact where id={}".format(int(bfr_id)))
        lc=cur.fetchall()
        i=lc[0]
        receiver_email=i[0]
        response=mail_service.send_mail_single(mail_service_username,mail_service_password,receiver_email,self.subject.text,self.message.text,school_name)

        if response=='Sent Successfully':

            self.submit_btn.text='Successful'
            win_notification('School Manager','Mail sent successfully to\nID: {}\nAddress: {}'.format(bfr_id,receiver_email))
            
        else:
            win_notification('School Manager','Something went wrong\nPlease try again')
        

class PushNotificationGroup(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
        
        self.student_teacher_id_label= Label(text='Student/Teacher IDs', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.student_teacher_id_label)
        
        self.student_teacher_id= TextInput(multiline=True, write_tab=False,hint_text="IDs separated by comma       ','")
        self.gdlayout1.add_widget(self.student_teacher_id)

        self.subject_label= Label(text='Mail Subject', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.subject_label)
        
        self.subject= TextInput(multiline=True, write_tab=False)
        self.gdlayout1.add_widget(self.subject)

        self.message_label= Label(text='Message', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.message_label)
        
        self.message= TextInput(multiline=True, write_tab=False)
        self.gdlayout1.add_widget(self.message)


    def back(self,*_):

        self.student_teacher_id.text=''
        self.subject.text=''
        self.message.text=''

        self.submit_btn.text='Submit'
        self.submit_btn.disabled=False
        

    def submit(self,*_):

        global mail_service_username
        global mail_service_password
        global school_name
        
        if self.student_teacher_id.text=='':

            self.student_teacher_id.text='Please enter student/teacher ID'
            return
        
        if self.subject.text=='':

            self.subject.text='Please enter mail subject'
            return

        if self.message.text=='':

            self.message.text='Please enter some message'
            return
        
        bfr=self.student_teacher_id.text
        bfr1=bfr.split(',')
        win_notification('School Manager','Sending mail(s) to the group',duration=3)
        self.submit_btn.text='Please Wait'
        self.submit_btn.disabled=True
        
        try:
            
            for i in range(len(bfr1)):
                bfr_id=int(bfr1[i])
                cur.execute("select email_id from id_contact where id={}".format(int(bfr_id)))
                lc=cur.fetchall()
                i=lc[0]
                receiver_email=i[0]
                response=mail_service.send_mail_single(mail_service_username,mail_service_password,receiver_email,self.subject.text,self.message.text,school_name)

                if response=='Sent Successfully':
                    win_notification('School Manager','Mail sent successfully to\nID: {}\nAddress: {}'.format(bfr_id,receiver_email))
                else:
                    win_notification('School Manager','Something went wrong\nPlease try again')
                
                time.sleep(1)

            self.submit_btn.text='Successful'
            self.submit_btn.disabled=False
        
        except:
            self.submit_btn.text='Try Again'
            self.submit_btn.disabled=False
            win_notification('School Manager','Something went wrong',duration=4)
            

class PushNotificationAll(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.subject_label= Label(text='Mail Subject', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.subject_label)
        
        self.subject= TextInput(multiline=False, write_tab=False)
        self.gdlayout1.add_widget(self.subject)

        self.message_label= Label(text='Message', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.message_label)
        
        self.message= TextInput(multiline=True, write_tab=False)
        self.gdlayout1.add_widget(self.message)

    def back(self,*_):
        
        self.subject.text=''
        self.message.text=''

        self.submit_btn.text='Submit'
        self.submit_btn.disabled=False
        

    def submit(self,*_):
        
        global mail_service_username
        global mail_service_password
        global school_name

        if self.subject.text=='':

            self.subject.text='Please enter mail subject'
            return

        if self.message.text=='':

            self.message.text='Please enter some message'
            return

        win_notification('School Manager','Sending mail(s) to the all members',duration=3)
        self.submit_btn.text='Please Wait'
        self.submit_btn.disabled=True
        
        try:
            
            cur.execute("select email_id from id_contact")
            lc=cur.fetchall()
            cur.execute("select id from id_contact")
            lcc=cur.fetchall()
            receiver_id_list=lcc[0]
            receiver_email_list=lc[0]
            
            
            for i in range(len(receiver_email_list)):
                
                receiver_id=receiver_id_list[i]
                receiver_email=receiver_email_list[i]
                response=mail_service.send_mail_single(mail_service_username,mail_service_password,receiver_email,self.subject.text,self.message.text,school_name)

                if response=='Sent Successfully':
                    win_notification('School Manager','Mail sent successfully to\nID: {}\nAddress: {}'.format(receiver_id,receiver_email))
                else:
                    win_notification('School Manager','Cannot send mail to\nID: {}\nAddress: {}\nPlease try again'.format(receiver_id,receiver_email),duration=4)
                
                time.sleep(1)

            self.submit_btn.text='Successful'
            self.submit_btn.disabled=False
        
        except:
            self.submit_btn.text='Try Again'
            self.submit_btn.disabled=False
            win_notification('School Manager','Something went wrong',duration=4)


class popup_book_manager_add(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.submit_btn.disabled=False

    def submit(self,*_):

        if len(self.book_id.text)==0 or len(self.book_name.text)==0 or len(self.quantity.text)==0:
            win_notification("School Manager","Invalid Input")
            return
        
        cur.execute("select book_id from library_book_database where book_id='{}' ".format(self.book_id.text))
        m=cur.fetchall()
        if len(m)==0 and self.quantity.text[0]=="+":
            win_notification("School Manager","Book ID not found")
            return
        
        elif len(m)!=0 and self.quantity.text[0]=="+":
            cur.execute("select qty from library_book_database where book_id='{}' ".format(self.book_id.text))
            l=cur.fetchall()
            i=l[0]
            quantity=int(i[0])
            quantity+=int(self.quantity.text[1:])
            cur.execute("update library_book_database set qty={} where book_id='{}' ".format(str(quantity),self.book_id.text))
            a.commit()
            win_notification("School Manager","Book quantity updated successfully\nBook ID: {}\nQuantity: {}".format(self.book_id.text,str(quantity)))
            self.submit_btn.disabled=True
            return
        
        if len(m)==0:
            cur.execute("insert into library_book_database values ('{}','{}',{}) ".format(self.book_name.text,self.book_id.text,self.quantity.text))
            a.commit()
            win_notification("School Manager","Book Added Successfully\nBook Name: {}\nBook ID: {}\nQuantity: {}".format(self.book_name.text,self.book_id.text,self.quantity.text))
            self.submit_btn.disabled=True
            return
        else:
            win_notification("School Manager","Book ID already assigned")
            return
        
    def cancel(self,*_):

        self.book_id.text=''
        self.book_name.text=''
        self.quantity.text=''
        self.dismiss()
        self.submit_btn.disabled=False
        
class popup_book_manager_remove(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.submit_btn.disabled=False

    def submit(self,*_):

        if len(self.book_id.text)==0:
            win_notification("School Manager","Invalid Input")
            return
        
        cur.execute("select book_id from library_book_database where book_id='{}' ".format(self.book_id.text))
        l=cur.fetchall()
        if len(l)==0:
            win_notification("School Manager","Book ID not found")
        else:
            if len(self.quantity.text)==0:
                cur.execute("delete from library_book_database where book_id='{}' ".format(self.book_id.text))
                win_notification("School Manager","Book Deleted Successfully\nBook ID: {}".format(self.book_id.text))
            else:
                cur.execute("select qty from library_book_database where book_id='{}' ".format(self.book_id.text))
                l=cur.fetchall()
                i=l[0]
                quantity=int(i[0])
                if quantity < int(self.quantity.text) or quantity - int(self.quantity.text) == 0:
                    win_notification("School Manager","Present stock is less than {}".format(self.quantity.text))
                    return
                
                quantity-= int(self.quantity.text)   
                cur.execute("update library_book_database set qty={} where book_id='{}' ".format(str(quantity),self.book_id.text))
                win_notification("School Manager","Book quantity updated successfully\nBook ID: {}\nQuantity: {}".format(self.book_id.text,str(quantity)))
            a.commit()
            
            self.submit_btn.disabled=True
            return
            
    
    def cancel(self,*_):

        self.book_id.text=''
        self.quantity.text=''
        self.dismiss()
        self.submit_btn.disabled=False

class popup_book_manager_view(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def open_popup(self,*_):
        self = popup_book_manager_view()
        if len(self.gdlayout.children)!=0:
            self.gdlayout.clear_widgets()
        cur.execute("select book_id,book_name,qty from library_book_database")
        bfr = cur.fetchall()
        for book in bfr:
            self.gdlayout.add_widget(Label(text=str(book[0]),color=(0,0,0,1),size_hint_x=0.2,size_hint_y=None,height=40))
            self.gdlayout.add_widget(Label(text=str(book[1]),color=(0,0,0,1),size_hint_x=0.6,size_hint_y=None,height=40))
            self.gdlayout.add_widget(Label(text=str(book[2]),color=(0,0,0,1),size_hint_x=0.2,size_hint_y=None,height=40))
        self.open()

class popup_book_manager_option(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def add(self,*_):

        self.dismiss()
        bookmanageraddpopup = popup_book_manager_add()
        bookmanageraddpopup.open()

    def remove(self,*_):

        self.dismiss()
        bookmanagerremovepopup = popup_book_manager_remove()
        bookmanagerremovepopup.open()

    def view(self,*_):

        self.dismiss()
        popup_book_manager_view.open_popup(self)

class popup_book_issue(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.submit_btn.disabled=False
        self.cancel_btn.text = "Cancel"
    
    def cancel(self,*_):

        self.book_id.text=''
        self.return_date.text=''
        
        self.dismiss()

    def submit(self,*_):

        book_id=self.book_id.text
        return_date=self.return_date.text
        
        app_ref.library_page.book_issue(book_id,return_date)
        app_ref.library_page.submit(LibraryPage)
        self.submit_btn.disabled=True

class popup_book_return(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.confirm_btn.disabled=False
        self.cancel_btn.text = "Cancel"
        
    def confirm(self,*_):

        app_ref.library_page.book_return(LibraryPage)
        app_ref.library_page.submit(LibraryPage)
        
        self.confirm_btn.disabled=True
        
    def cancel(self,*_):

        self.dismiss()

class LibraryPage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.book_manager_btn.bind(on_press=self.book_manager_popup)
        
        self.submit_btn.bind(on_press=self.submit)

        self.issue_btn.bind(on_press=self.book_issue_popup)
        self.return_btn.bind(on_press=self.book_return_popup)
        self.reminder_btn.bind(on_press=self.send_reminder)
        
        self.issue_btn.disabled=True
        self.return_btn.disabled=True
        self.reminder_btn.disabled=True

    def book_manager_popup(self,*_):

        bookmanageroptionpopup = popup_book_manager_option()
        bookmanageroptionpopup.open()
    
    def submit(self,*_):
        
        if len(self.borrower_id.text)==12 or len(self.borrower_id.text)==13:
            pass  
        else:
            self.submit_btn.text='Invalid ID'
            return

        cur.execute("select email_id,ph_no from id_contact where id={}".format(self.borrower_id.text))
        l=cur.fetchall()
        if len(l)==0:
            win_notification("School Manager","ID not found in records",duration=3)
            return
        else:
            self.submit_btn.text="Submit"
            
        i=l[0]
        email_id=i[0]
        ph_no=i[1]
        
        cur.execute("select * from library_user_database where id={}".format(self.borrower_id.text))
        l=cur.fetchall()
        i=l[0]
        name=i[0]
        book_id=i[2]
        issue_date=i[3]
        return_date=i[4]

        if book_id=='':
            
            self.form_name.text=name
            self.form_phno.text=str(ph_no)
            self.form_email.text=email_id
            self.form_borrowerid.text=self.borrower_id.text

            self.book_name.text=''
            self.book_id.text=''
            self.issue_date.text=''
            self.return_date.text=''
            
            self.issue_btn.disabled=False
            self.return_btn.disabled=True
            self.reminder_btn.disabled=True
            return
        
        else:

            self.form_name.text=name
            self.form_phno.text=str(ph_no)
            self.form_email.text=email_id
            self.form_borrowerid.text=self.borrower_id.text
            
            cur.execute("select * from library_book_database where book_id='{}' ".format(book_id))
            m=cur.fetchall()
            j=m[0]
            book_name=j[0]
            qty=j[2]
            self.book_name.text=book_name
            self.book_id.text=book_id
            self.issue_date.text=issue_date
            self.return_date.text=return_date
            self.issue_btn.disabled=True
            self.return_btn.disabled=False
            
            issue_date_dt_obj=datetime.strptime(issue_date,"%d-%m-%Y")
            return_date_dt_obj=datetime.strptime(return_date,"%d-%m-%Y")
            current_dt=datetime.now().strftime("%d-%m-%Y")
            current_date=datetime.strptime(current_dt,"%d-%m-%Y")
            delta=timedelta(days=5)
            
            if (return_date_dt_obj-current_date)<delta or current_date>return_date_dt_obj:
                self.reminder_btn.disabled=False
            else:
                self.reminder_btn.disabled=True

                
    def book_issue_popup(self,*_):

        bookissuepopup=popup_book_issue()
        bookissuepopup.open()

    def book_issue(self,book_id,return_date,*args):

        cur.execute("select book_name,qty from library_book_database where book_id='{}' ".format(book_id))
        l=cur.fetchall()
        i=l[0]
        book_name=i[0]
        qty=i[1]
        
        if qty<1:
            win_notification("School Manager","Cannot issue book\nBook not available",duration=3)
            return
        else:
            try:
                current_date=datetime.now().strftime("%d-%m-%Y")
                cur.execute("update library_user_database set book_id='{}', issue_date='{}', return_date='{}' where id={}".format(book_id,current_date,return_date,self.borrower_id.text))
                cur.execute("update library_book_database set qty={}".format(qty-1))
                a.commit()
                win_notification("School Manager","Book issued to {}\nBook Name: {}\nReturn Date: {}".format(self.form_name.text,book_name,return_date),duration=3)
                popup_book_issue_ins = popup_book_issue()
                popup_book_issue_ins.cancel_btn.text = "Back"
            except:
                win_notification("School Manager","Cannot issue book\nSomething went wrong",duration=2)
            
    def book_return_popup(self,*_):

        bookreturnpopup=popup_book_return()
        bookreturnpopup.open()

    def book_return(self,*_):

        try:
            cur.execute("select qty from library_book_database where book_id='{}' ".format(self.book_id.text))
            l=cur.fetchall()
            i=l[0]
            qty=i[0]
        
            cur.execute("update library_user_database set book_id='', issue_date='', return_date='' where id={}".format(self.borrower_id.text))
            cur.execute("update library_book_database set qty={} where book_id='{}' ".format(qty+1,self.book_id.text))
            a.commit()

            win_notification("School Manager","Returned book successfully",duration=3)
            popup_book_return_ins = popup_book_return()
            popup_book_return_ins.cancel_btn.text = "Back"
            
        except:
            win_notification("School Manager","Cannot return book\nSomething went wrong",duration=3)
            
    def send_reminder(self,*_):

        global mail_service_username
        global mail_service_password
        global school_name

        receiver_email=self.form_email.text
        subject="School Library"
        message="Dear {},\n\nThis is a reminder to return the issued book by {}\n\nBook Name: {}\nIssue Date: {}\n\n\nReport the school librarian if already returned".format(self.form_name.text,self.return_date.text,self.book_name.text,self.issue_date.text)
        response=mail_service.send_mail_single(mail_service_username,mail_service_password,receiver_email,subject,message,school_name)

        if response=="Sent Successfully":
            win_notification("School Manager","Reminder sent successfully to\n{}".format(self.form_name.text),duration=3)
            self.reminder_btn.disabled=True
        else:
            win_notification("School Manager","Cannot send reminder\nSome erro occured",duration=3)
            
        
    def back(self,*_):

        self.scrollview.scroll_y=1
        self.borrower_id.text=''
        self.form_name.text=''
        self.form_phno.text=''
        self.form_email.text=''
        self.form_borrowerid.text=''

        self.book_name.text=''
        self.book_id.text=''
        self.issue_date.text=''
        self.return_date.text=''
        
        self.issue_btn.disabled=True
        self.return_btn.disabled=True
        self.reminder_btn.disabled=True
        
        
class ApplicationHomePage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def homepage(self,*_):
        app_ref.scmanager.transition = SlideTransition(direction="right")
        app_ref.scmanager.current='Home_Page'
        
       
class SettingsPage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.changetheme_btn.bind(on_press=self.theme)
        self.mailacc_btn.bind(on_press=partial(app_ref.app_interface_change_screen,"Mail_Account"))

    def theme(self,*_):

        app_ref.change_theme.fg_color_bxlayout.fg_color_picker=ColorPicker()
        app_ref.change_theme.fg_color_bxlayout.fg_color_picker.bind(color=app_ref.change_theme.on_color_fg)
        app_ref.change_theme.txt_color_bxlayout.txt_color_picker=ColorPicker()
        app_ref.change_theme.txt_color_bxlayout.txt_color_picker.bind(color=app_ref.change_theme.on_color_txt)
        app_ref.app_interface_change_screen("Change_Theme")
        

        
        

class ChangeTheme(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.fg_color_bxlayout.fg_color_picker=ColorPicker()
        self.fg_color_bxlayout.fg_color_picker.bind(color=self.on_color_fg)
        self.txt_color_bxlayout.txt_color_picker=ColorPicker()
        self.txt_color_bxlayout.txt_color_picker.bind(color=self.on_color_txt)
        
        self.fg_color_bxlayout.add_widget(self.fg_color_bxlayout.fg_color_picker)
        self.txt_color_bxlayout.add_widget(self.txt_color_bxlayout.txt_color_picker)

    def on_color_fg(self,instance,value):

        if value==[1.0,1.0,1.0,1]:
            return
        else:
            pass
        app_ref.fnt_fg_color=value
        local_storage_theme.put('theme_list',theme_fg=app_ref.fnt_fg_color,theme_txt=app_ref.fnt_txt_color)

    def on_color_txt(self,instance,value):
        
        if value==[1.0,1.0,1.0,1]:
            return
        else:
            pass
        app_ref.fnt_txt_color=value
        local_storage_theme.put('theme_list',theme_fg=app_ref.fnt_fg_color,theme_txt=app_ref.fnt_txt_color)

class MailAccountPage(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.submit_btn.bind(on_press=self.submit)
        
        self.smtp_host_label=Label(text='SMTP Host', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.smtp_host_label)
        
        self.smtp_host=TextInput(multiline=False, write_tab=False, text='smtp.google.com', disabled=True)
        self.gdlayout1.add_widget(self.smtp_host)
        
        self.smtp_port_label=Label(text='SMTP Port', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.smtp_port_label)
        
        self.smtp_port=TextInput(multiline=False, write_tab=False, text='587', disabled=True)
        self.gdlayout1.add_widget(self.smtp_port)
        
        self.mail_username_label=Label(text='Mail Adress', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.mail_username_label)
        
        self.mail_username=TextInput(multiline=False, write_tab=False)
        self.gdlayout1.add_widget(self.mail_username)
        
        self.mail_password_label=Label(text='Mail Password', color=[0,0,0,1], bold=True)
        self.gdlayout1.add_widget(self.mail_password_label)
        
        self.mail_password=TextInput(multiline=False, write_tab=False, password=True)
        self.gdlayout1.add_widget(self.mail_password)
        
    def submit(self,*_):

        global mail_service_username
        global mail_service_password

        if len(self.mail_username.text)==0 or len(self.mail_password.text)==0:

            win_notification('School Manager','Mail ID/Password cannot be blank',duration=3)
            return
        
        win_notification('School Manager','Checking Connection',duration=3)

        chk_token=mail_service.MailServiceCheckUp(self.mail_username.text,self.mail_password.text)
        
        if chk_token=='Successful':
            
            mail_service_username=self.mail_username.text
            mail_service_password=self.mail_password.text

            self.submit_btn.disabled=True
            win_notification('School Manager','Test Successful\nMail details updated',duration=3)

            local_storage_mail_service.put('login_data',username=self.mail_username.text,password=self.mail_password.text)

        elif chk_token=='Domain Error':
            
            self.submit_btn.text="Try Again"
            win_notification('School Manager','{}'.format(chk_token),duration=3)
            
        elif chk_token=='Authentication Error':

            self.submit_btn.text="Try Again"
            win_notification('School Manager','{}'.format(chk_token),duration=3)
            
        elif chk_token=='Some Error Occured':

            self.submit_btn.text="Try Again"
            win_notification('School Manager','{}'.format(chk_token),duration=3)
            
    def back(self,*_):

        self.submit_btn.text='Submit'
        self.submit_btn.disabled=False
        
        self.smtp_host.text='smtp.gmail.com'
        self.smtp_port.text='587'
        self.mail_username.text=''
        self.mail_password.text=''
                

class popup_logout_confirmation(Popup):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    def logout(self,*_):

        cur.close()
        a.close()
        app_ref.login_page.username.text=''
        app_ref.login_page.passwd.text=''
        app_ref.scmanager_main.transition = RiseInTransition()
        app_ref.scmanager_main.current='Login_Page'
        self.dismiss()
      
class SchoolManager(App):

    fnt_fg_color = ListProperty()
    fnt_txt_color = ListProperty()

    screen_history = []
    
    def app_interface_change_screen(self,screen_name,*_):

        last_screen = self.scmanager.current
        self.screen_history.append(last_screen)
        app_ref.scmanager.transition = SlideTransition(direction="left")
        self.scmanager.current = "{}".format(screen_name)
    
    def home(self,*_):
        
        last_screen = self.scmanager.current
        self.screen_history.append(last_screen)
        app_ref.scmanager.transition = RiseInTransition()
        app_ref.scmanager.current='Home_Page'
    
    def logout(self,*_):
        
        logoutconfirmationpopup=popup_logout_confirmation()
        logoutconfirmationpopup.open()

    def back(self,*_):

        current_screen = self.scmanager.current
        
        if len(self.screen_history)==0:
            return
        screen_name = self.screen_history[-1]
        self.screen_history.pop()
        app_ref.scmanager.transition = SlideTransition(direction="right")
        app_ref.scmanager.current="{}".format(screen_name)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
        if current_screen == "Fetch_Student":
            app_ref.fetch_std.back()
        if current_screen == "Fetch_Class":
            app_ref.fetch_class.back()
        if current_screen == "Fetch_TeacherList":
            app_ref.fetch_teacherlist.back()
        if current_screen == "Add_Student":
            app_ref.add_student.back()
        if current_screen == "Remove_Student":
            app_ref.remove_student.back()
        if current_screen == "Add_Teacher":
            app_ref.add_teacher.back()
        if current_screen == "Remove_Teacher":
            app_ref.remove_teacher.back()
        if current_screen == "PushNotificationIndividual":
            app_ref.push_notificationindividual.back()
        if current_screen == "PushNotificationGroup":
            app_ref.push_notificationgroup.back()
        if current_screen == "PushNotificationAll":
            app_ref.push_notificationall.back()
        if current_screen == "Library_Page":
            app_ref.library_page.back()
        if current_screen == "Mail_Account":
            app_ref.mail_accountpage.back()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
             

    def settings(self,*_):
        self.screen_history.append("Settings_Page")
        app_ref.scmanager.transition = SlideTransition(direction="left")
        app_ref.scmanager.current='Settings_Page'

    def build(self):
        
        # Creating screenmanager object as scmanager
        # widget object is created as self.(name)
        # screen object is created as S_(name)

        self.fnt_fg_color=theme_fg
        self.fnt_txt_color=theme_txt

        self.background_wallpaper = "./App/Data/Atlas/bg1000.png"
        
        self.scmanager= ScreenManager()
        self.scmanager_main = ScreenManager()

        # Screen - WelcomePage()

        self.welcome_page=WelcomePage()
        S_welcome=Screen(name="Welcome_Page")
        S_welcome.add_widget(self.welcome_page)
        self.scmanager_main.add_widget(S_welcome)


        # Screen - LoginPage()
        
        self.login_page= LoginPage()
        S_login= Screen(name="Login_Page")
        S_login.add_widget(self.login_page)
        self.scmanager_main.add_widget(S_login)


        # Screen - SignUpPage()

        self.signup_page=SignUpPage()
        S_signup=Screen(name="SignUp_Page")
        S_signup.add_widget(self.signup_page)
        self.scmanager_main.add_widget(S_signup)

        # Screen - DatabaseConfigurationPage()

        self.database_configuration_page=DatabaseConfigurationPage()
        S_database_configuration_page=Screen(name="Database_Configuration_Page")
        S_database_configuration_page.add_widget(self.database_configuration_page)
        self.scmanager_main.add_widget(S_database_configuration_page)
        
        # Screen - AfterLogin()
        
        self.after_login=AfterLogin()
        S_afterlogin=Screen(name="After_Login")
        S_afterlogin.add_widget(self.after_login)
        self.scmanager_main.add_widget(S_afterlogin)
        
        # Screen - HomePage()
        
        self.home_page=HomePage()
        S_home= Screen(name="Home_Page")
        S_home.add_widget(self.home_page)
        self.scmanager.add_widget(S_home)

        # Screen - StudentSection()

        self.student_section=StudentSection()
        S_student_section=Screen(name='Student_Section')
        S_student_section.add_widget(self.student_section)
        self.scmanager.add_widget(S_student_section)


        # Screen - FetchStudentDetails()

        self.fetch_std=FetchStudentDetails()
        S_fetch_std=Screen(name="Fetch_Student")
        S_fetch_std.add_widget(self.fetch_std)
        self.scmanager.add_widget(S_fetch_std)

        
        # Screen - FetchClassWise()

        self.fetch_class=FetchClassWise()
        S_fetch_class=Screen(name="Fetch_Class")
        S_fetch_class.add_widget(self.fetch_class)
        self.scmanager.add_widget(S_fetch_class)

        # Screen - AddStudent()

        self.add_student=AddStudent()
        S_add_student=Screen(name='Add_Student')
        S_add_student.add_widget(self.add_student)
        self.scmanager.add_widget(S_add_student)

        # Screen - RemoveStudent()

        self.remove_student=RemoveStudent()
        S_remove_student=Screen(name='Remove_Student')
        S_remove_student.add_widget(self.remove_student)
        self.scmanager.add_widget(S_remove_student)

        # Screen - TeacherSection()

        self.teacher_section=TeacherSection()
        S_teacher_section=Screen(name='Teacher_Section')
        S_teacher_section.add_widget(self.teacher_section)
        self.scmanager.add_widget(S_teacher_section)

        # Screen - FetchTeacherList()

        self.fetch_teacherlist=FetchTeacherList()
        S_fetch_teacherlist=Screen(name='Fetch_TeacherList')
        S_fetch_teacherlist.add_widget(self.fetch_teacherlist)
        self.scmanager.add_widget(S_fetch_teacherlist)

        # Screen - AddTeacher()

        self.add_teacher=AddTeacher()
        S_add_teacher=Screen(name='Add_Teacher')
        S_add_teacher.add_widget(self.add_teacher)
        self.scmanager.add_widget(S_add_teacher)

        # Screen - RemoveTeacher()

        self.remove_teacher=RemoveTeacher()
        S_remove_teacher=Screen(name='Remove_Teacher')
        S_remove_teacher.add_widget(self.remove_teacher)
        self.scmanager.add_widget(S_remove_teacher)

        # Screen - OtherSection()

        self.other_section= OtherSection()
        S_other_section=Screen(name='Other_Section')
        S_other_section.add_widget(self.other_section)
        self.scmanager.add_widget(S_other_section)

        # Screen - MainMembers()

        self.main_members= MainMembers()
        S_main_members=Screen(name='Main_Members')
        S_main_members.add_widget(self.main_members)
        self.scmanager.add_widget(S_main_members)
        
        # Screen - PushNotification()

        self.push_notification= PushNotification()
        S_push_notification=Screen(name='Push_Notification')
        S_push_notification.add_widget(self.push_notification)
        self.scmanager.add_widget(S_push_notification)

        # Screen - PushNotification()

        self.push_notificationindividual= PushNotificationIndividual()
        S_push_notificationindividual=Screen(name='Push_NotificationIndividual')
        S_push_notificationindividual.add_widget(self.push_notificationindividual)
        self.scmanager.add_widget(S_push_notificationindividual)

        # Screen - PushNotificationGroup()

        self.push_notificationgroup= PushNotificationGroup()
        S_push_notificationgroup=Screen(name='Push_NotificationGroup')
        S_push_notificationgroup.add_widget(self.push_notificationgroup)
        self.scmanager.add_widget(S_push_notificationgroup)

        # Screen - PushNotificationAll()

        self.push_notificationall= PushNotificationAll()
        S_push_notificationall=Screen(name='Push_NotificationAll')
        S_push_notificationall.add_widget(self.push_notificationall)
        self.scmanager.add_widget(S_push_notificationall)

        # Screen - LibraryPage()

        self.library_page=LibraryPage()
        S_library_page=Screen(name='Library_Page')
        S_library_page.add_widget(self.library_page)
        self.scmanager.add_widget(S_library_page)
        
        # Screen - SettingsPage()

        self.settings_page=SettingsPage()
        S_settings_page=Screen(name='Settings_Page')
        S_settings_page.add_widget(self.settings_page)
        self.scmanager.add_widget(S_settings_page)

        # Screen - ChangeTheme()

        self.change_theme=ChangeTheme()
        S_change_theme=Screen(name='Change_Theme')
        S_change_theme.add_widget(self.change_theme)
        self.scmanager.add_widget(S_change_theme)

        #Screen = MailAccountPage()

        self.mail_accountpage=MailAccountPage()
        S_mail_accountpage=Screen(name='Mail_Account')
        S_mail_accountpage.add_widget(self.mail_accountpage)
        self.scmanager.add_widget(S_mail_accountpage)

        self.app_interface_window_layout = BoxLayout(size_hint_y=None,height=810)
        self.app_interface_window_layout.add_widget(self.scmanager)

        self.nav_bar = AppInterfaceNavBar()
        
        self.app_interface_window = AppInterfaceWindow()
        S_app_interface_window = Screen(name='App_Interface_Page')
        self.app_interface_window.add_widget(self.nav_bar)
        self.app_interface_window.add_widget(self.app_interface_window_layout)
        S_app_interface_window.add_widget(self.app_interface_window)
        self.scmanager_main.add_widget(S_app_interface_window)

        # returning screen manager
        
        return self.scmanager_main

Window.size = (1920,1080)
Window.fullscreen = True
app_ref=SchoolManager()
app_ref.run()
