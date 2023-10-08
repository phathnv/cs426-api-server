import smtplib
from email.message import EmailMessage
import os

def send_reset_code(email, username, code):
   subject = 'LeFrigo - Reset Your Password'
   message = """
   <!DOCTYPE html>
   <html><body>
   Hello %s,
   <br><br>
   We have received a request to reset your password for your account on our platform. 
   To proceed with resetting your password, please use this code: <b style="color:red">%s</b>.
   <br><br>
   Please note that the code is valid for only 10 minutes. If the code expires, you will need to request a new one.
   <br><br>
   If you did not request a password reset, please disregard this email. Your account will remain secure.
   <br><br>
   Please contact our team at lefrigoteam@gmail.com if you need assistance.
   <br><br>
   Thank you for using our platform!
   <br><br>
   Best regards,
   <br>
   LeFrigo.
   </body>
   </html>
   """%(username,code)    
   try:    
      smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)  
      smtpObj.login(os.getenv('EMAIL_ADDRESS'),os.getenv('EMAIL_PASSWORD'))    
      msg = EmailMessage()
      msg['Subject'] = subject
      msg['From'] = os.getenv('EMAIL_ADDRESS')
      msg['To'] = email
      msg.set_content(message, subtype='html')
      smtpObj.send_message(msg)   
   except Exception:    
      raise