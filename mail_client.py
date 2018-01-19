#!/usr/local/bin/python3
# coding=utf-8
# 利用tkiner模块开发一个简单的邮件客户端程序

from  tkinter.filedialog import *
from tkinter import *
from tkinter.scrolledtext import *
import tkinter.ttk
import os
import re
import sys
import threading
import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE
import smtplib


class Lix:
    def __init__(self):
        self.ui = Tk()
        self.add_to = StringVar()
        self.add_from = StringVar()
        self.password = StringVar()
        self.subject = StringVar()
        self.message=''
        self.attachment_list = StringVar()
        self.status=StringVar()
        self.init_ui()
        pass

    def init_ui(self):
        self.ui.title('Mail_sender')
        panel1 = PanedWindow(self.ui)
        panel2 = PanedWindow(self.ui)
        panel3 = PanedWindow(self.ui)
        panel4 = PanedWindow(self.ui)
        panel5 = PanedWindow(self.ui)
        panel6 = PanedWindow(self.ui)
        panel7 = PanedWindow(self.ui)
        panel8 = PanedWindow(self.ui)
        label1 = Label(panel1)
        label2 = Label(panel2)
        label3 = Label(panel2)
        label4 = Label(panel3)
        label5 = Label(panel4)
        label6 = Label(panel5)
        label7 = Label(panel6)
        entry1 = Entry(panel1)
        entry2 = Entry(panel2)
        entry3 = Entry(panel2, show='*')
        entry4 = Entry(panel3)
        entry5 = Entry(panel4)
        self.text = ScrolledText(panel5)
        button1 = Button(panel4)
        button2 = Button(panel4)
        panel1.pack(anchor='n', side='top', fill='x')
        panel2.pack(anchor='n', side='top', fill='x')
        panel3.pack(anchor='n', side='top', fill='x')
        panel4.pack(anchor='n', side='top', fill='x')
        panel5.pack(anchor='n', side='top', fill='x')
        panel6.pack(anchor='n', side='top', fill='x')
        panel6.pack(anchor='n', side='top', fill='x')
        label1.pack(anchor='w', side='left', fill='y')
        entry1.pack(anchor='w', side='left')
        label2.pack(anchor='w', side='left')
        entry2.pack(anchor='w', side='left')
        label3.pack(anchor='w', side='left')
        entry3.pack(anchor='w', side='left')
        label4.pack(anchor='w', side='left')
        entry4.pack(anchor='w', side='left')
        label5.pack(anchor='w', side='left')
        entry5.pack(anchor='w', side='left')
        button1.pack(anchor='w', side='left')
        label6.pack(anchor='w', side='left')
        button2.pack(anchor='w', side='left')
        self.text.pack(anchor='w', side='left')
        label7.pack(anchor='w', side='left', fill='x')
        label1['text'] = '接收人:'
        label1['width'] = 10
        label2['text'] = '发信账号:'
        label2['width'] = 10
        label3['text'] = '发信密码:'
        label3['width'] = 10
        label4['text'] = '邮件标题:'
        label4['width'] = 10
        label5['text'] = '附件:'
        label5['width'] = 10
        label6['text'] = '    正文:'
        entry1['width'] = 75
        entry2['width'] = 43
        entry4['width'] = 75
        entry5['width'] = 58
        button1['text'] = u'选择附件'
        button2['text'] = u'发送邮件'
        entry1['textvariable'] = self.add_to
        entry2['textvariable'] = self.add_from
        entry3['textvariable'] = self.password
        entry4['textvariable'] = self.subject
        entry5['textvariable'] = self.attachment_list
        label7['textvariable'] = self.status
        button1['command'] = self.select_attachment
        button2['command'] = self.send
        #_____________________________Personal  Data_____________________________________
        self.add_to.set('')
        self.add_from.set('')
        self.password.set('')
        #________________________________________________________________________________
        self.ui.mainloop()

    def select_attachment(self):
        attach = self.attachment_list.get()
        for st in askopenfilenames():
            attach += st+','
        self.attachment_list.set(attach)

    def send(self):
        self.message=self.text.get(0.0,'end')
        self.send_mail(self.add_to.get(),self.add_from.get(),self.subject.get(),self.password.get(),self.message,self.attachment_list.get())

    def send_mail(self, add_to, add_from, subject, password, message, attachment):
        to = re.findall(re.compile(r'([^;, ]+@[^,; ]+)[,]?'), add_to)
        smtp = 'smtp.' + re.match('.*@(.*)', add_from).group(1)
        user = re.match('(.*)@.*', add_from).group(1)
        msg = MIMEMultipart()
        for st in re.findall('([^,]+),?', attachment):
            attach = {}
            attach[st] = MIMEText(open(st, 'rb').read(), 'base64', 'gb2312')
            attach[st]["Content-Type"] = 'application/octet-stream'
            attach[st]["Content-Disposition"] = 'attachment; filename=' + re.match(r'.*[\\/]+(.*)', st).group(
                1)
            msg.attach(attach[st])
        msg['to'] = COMMASPACE.join(to)
        msg['from'] = add_from
        msg['subject'] = subject
        part1 = MIMEText(message, 'plain')
        msg.attach(part1)
        try:
            server = smtplib.SMTP()
            server.connect(smtp)
            server.login(user, password)
            server.sendmail(msg['from'], msg['to'], msg.as_string())
            server.quit()
            self.status.set(u'发送成功')
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    q = Lix()
