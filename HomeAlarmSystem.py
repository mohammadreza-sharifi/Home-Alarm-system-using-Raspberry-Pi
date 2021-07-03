from kavenegar import *
import RPi.GPIO as io
from picamera import PiCamera
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587 
GMAIL_USERNAME = 'your gmail address' 
GMAIL_PASSWORD = 'app password'  

class Emailer:
    def sendmail(self, recipient, subject, content, image):
          
        
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME
 
        
        emailData.attach(MIMEText(content))
 
        
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg') 
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)
  
        
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        
        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
        session.quit
  
sender = Emailer()

camera = PiCamera()

api = KavenegarAPI('366C44766F67353374315A664431527432477138615153622F64696F6962334948444F696865586D33784D3D')
params = { 'sender' : '1000596446', 'receptor': '09389978239', 'message' :'thief detected' }
sound_params = { 'sender' : '1000596446', 'receptor': '09389978239', 'message' :'a sound detected!!!! , please check the cam' }


io.setwarnings(False)
io.setmode(io.BOARD)
io.setup(3,io.IN)
io.setup(5,io.OUT)
io.setup(7,io.OUT)
io.setup(11,io.IN)
io.setup(13,io.OUT)


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
