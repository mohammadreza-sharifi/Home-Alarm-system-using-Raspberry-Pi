from kavenegar import *
import RPi.GPIO as io
from picamera import PiCamera
import time
import smtplib
import telepot
from telepot.loop import MessageLoop
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'mamadsharifi1377@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'howszywzekkfjyjy'  #change this to match your gmail password

class Emailer:
    def sendmail(self, recipient, subject, content, image):
          
        #Create Headers
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME
 
        #Attach our text data  
        emailData.attach(MIMEText(content))
 
        #Create our Image Data from the defined image
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg') 
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
        session.quit
  
sender = Emailer()

camera = PiCamera()

api = KavenegarAPI('366C44766F67353374315A664431527432477138615153622F64696F6962334948444F696865586D33784D3D')
params = { 'sender' : '1000596446', 'receptor': '09389978239', 'message' :'thief detected' }
sound_params = { 'sender' : '1000596446', 'receptor': '09389978239', 'message' :'a sound detected!!!! , please check the cam' }
#response = api.sms_send(input_params)

#pir sensor connected to pin 3
#sound sensor connected to pin 11
#buzzer connected to pin 5
#led connected to 7
#servo motor connected to pin 13
io.setwarnings(False)
io.setmode(io.BOARD)
io.setup(3,io.IN)
io.setup(5,io.OUT)
io.setup(7,io.OUT)
io.setup(11,io.IN)
#io.setup(13,io.OUT)
#servo = io.PWM(13,50)

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print('got command: %s' % command)
    
    if command == "Capture":
        camera.start_preview()
        time.sleep(2)
        camera.capture('/home/pi/Desktop/telegrambot/botdetector.jpg')
        camera.stop_preview()
        bot.sendMessage(chat_id,"photo captured")
        
    elif command == "Alarm photo":
        bot.sendPhoto(chat_id,photo=open('/home/pi/Desktop/telegrambot/detector.jpg','rb'))
        
    elif command == "my photo":
        bot.sendPhoto(chat_id,photo=open('/home/pi/Desktop/telegrambot/botdetector.jpg','rb'))

bot = telepot.Bot('1889712689:AAF45j3A5BthLfLwhMPQYJBmT5H0LHKV3OA')
bot.message_loop(action)

while True:
    
    pirDetector = io.input(3)
    soundDetector = io.input(11)
    
    if pirDetector == True and soundDetector == False:
        
        io.output(5,1)
        io.output(7,1)
        camera.start_preview()
        time.sleep(5)
        camera.capture('/home/pi/Desktop/detector.jpg')
        camera.stop_preview()
        
        image = '/home/pi/Desktop/detector.jpg'
        sendTo = 'mamadsh.sharifi@gmail.com'
        emailSubject = "somebody Detected!"
        emailContent = "please check the camera: " + time.ctime()
        sender.sendmail(sendTo, emailSubject, emailContent, image)
        print("Email Sent")
        response = api.sms_send( params)
        #print("pirDetector detected!!!")
        
    elif pirDetector == False and soundDetector == True:
       
        response = api.sms_send( sound_params)
        io.output(5,1)
        io.output(7,1)
        #print("soundDetector detected")
    else:
        io.output(5,0)
        io.output(7,0)
        

