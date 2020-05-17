
from celery import Celery
import time
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobgy.settings")
django.setup()
"""


cele = Celery('celerytask.tasks', broker='redis://127.0.0.1:6379/8')

@cele.task
def taskWork(user, empno):
    # time.sleep(10)
    print('abc/', user, empno)

    title = '邮件发送jjkkm'
    content = '临时使用邮件转发'
    receive_mail = ['keke.jiao@marcpoint.com']
    cc_mail = []
    smp = SendMailProject()
    smp.sendMail(subject=title, content=content, cc_mail=cc_mail, receive_mail=receive_mail)




class SendMailProject(object):
    def __init__(self):

        self.msg_from = '3414474690@qq.com'
        self.passwd = 'goybmvpsglmucjfa'

    def f(self, fi):

        self.__createFile(fi)

    def __createContent(self, mail_body):

        '''处理正文'''
        return mail_body

    def __createFile(self, extra_file):

        '''处理附件'''
        sendFile = MIMEApplication(open(extra_file, 'rb').read())
        sendFile["Content-Type"] = 'application/octet-stream'
        sendFile.add_header('Content-Disposition', 'attachment')
        return sendFile

    def __createPng(self, png_file):

        img_file = open(png_file, 'rb').read()
        image = MIMEImage(img_file)
        image.add_header('Content-ID', '<image1>')
        image["Content-Disposition"] = 'attachment; filename="red_people.png"'
        return image

    def sendMail(self, subject, content, receive_mail, cc_mail=None, extra_file=None, png_file=None):

        msg = MIMEMultipart(_charset='utf-8', _subtype='mixed')
        msg['From'] = self.msg_from
        msg['To'] = ';'.join(receive_mail)
        if cc_mail:
            msg['Cc'] = ';'.join(cc_mail)
        msg['Subject'] = subject
        text_sub = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_sub)
        if png_file:
            msg.attach(self.__createPng(png_file))
        if extra_file:
            msg.attach(self.__createFile(extra_file))
        try:
            sftp_obj = smtplib.SMTP_SSL("smtp.qq.com", 465)
            sftp_obj.login(self.msg_from, self.passwd)
            sftp_obj.sendmail(self.msg_from, receive_mail, msg.as_string(), )
            sftp_obj.quit()
        except Exception as e:
            print('sendemail failed next is the reason\n>>>', e)


