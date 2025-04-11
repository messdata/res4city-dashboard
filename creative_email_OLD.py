
# clean_creative_email_code =
# import os
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# import imghdr

# def send_creative_email(to_email, subject, html_content, plain_text_content, logo_path=None):
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     username = "testaxyz94@gmail.com"
#     app_password = "eond pzpz wbcx xcob"
#     from_email = "Res4City Tracker <testaxyz94@gmail.com>"

#     subject = subject.replace('\\xa0', ' ')
#     html_content = html_content.replace('\\xa0', ' ')
#     plain_text_content = plain_text_content.replace('\\xa0', ' ')

#     msg = MIMEMultipart("related")
#     msg['Subject'] = subject
#     msg['From'] = from_email
#     msg['To'] = to_email

#     msg_alternative = MIMEMultipart("alternative")
#     msg.attach(msg_alternative)

#     part1 = MIMEText(plain_text_content, "plain", "utf-8")
#     part2 = MIMEText(html_content, "html", "utf-8")
#     msg_alternative.attach(part1)
#     msg_alternative.attach(part2)

#     if logo_path and os.path.exists(logo_path):
#         with open(logo_path, "rb") as img_file:
#             logo_data = img_file.read()
#             subtype = imghdr.what(None, h=logo_data)
#             if not subtype:
#                 subtype = "png"
#             logo = MIMEImage(logo_data, _subtype=subtype)
#         logo.add_header('Content-ID', '<logo>')
#         logo.add_header('Content-Disposition', 'inline', filename=os.path.basename(logo_path))
#         msg.attach(logo)
#     else:
#         print("Logo not found or not provided. Continuing without inline logo.")

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(username, app_password)
#             server.sendmail(from_email, [to_email], msg.as_string())
#         print(f"Email sent to {to_email}")
#         return {"user_email": to_email, "subject": subject, "status": "Sent", "error": ""}
#     except Exception as e:
#         print(f"Failed to send email to {to_email}: {e}")
#         return {"user_email": to_email, "subject": subject, "status": "Failed", "error": str(e)}

# def get_html_template(user_name, hours_to_complete, user_email, course_code):
#     html_template = \"\"\"
# <html>
# <head>
#   <style>
#     body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
#     .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; border: 1px solid #ddd; }}
#     .header {{ background-color: #003366; color: #ffffff; padding: 20px; text-align: center; }}
#     .header img {{ max-width: 150px; margin-bottom: 10px; }}
#     .content {{ padding: 20px; color: #333333; }}
#     .content a {{ color: #ffcc00; text-decoration: none; }}
#     .footer {{ background-color: #003366; color: #ffffff; text-align: center; padding: 10px; font-size: 12px; }}
#   </style>
# </head>
# <body>
#   <div class="container">
#     <div class="header">
#       <img src="cid:logo" alt="Res4City Logo">
#       <h1>Res4City Notification</h1>
#     </div>
#     <div class="content">
#       <p>Dear {user_name},</p>
#       <p>We noticed that your average learning time for the course <strong>{course_code}</strong> is <strong>{hours_to_complete} hours</strong>, which is below our engagement threshold of 90 hours.</p>
#       <p>Please visit our website for more information and support:</p>
#       <p><a href="http://127.0.0.1:5050/redirect?user_id={user_email}&dest=https://www.res4city.eu/">Visit Res4City</a></p>
#       <p>Best regards,<br>The Res4City Team</p>
#     </div>
#     <div class="footer">
#       <p>© 2023 Res4City. All rights reserved.</p>
#     </div>
#   </div>
# </body>
# </html>
#     \"\"\"
#     return html_template.format(user_name=user_name, hours_to_complete=hours_to_complete, user_email=user_email, course_code=course_code)

# def get_plain_text_template(user_name, hours_to_complete, course_code):
#     plain_text_template = (
#         "Dear {user_name},\\n\\n"
#         "We noticed that your average learning time for the course {course_code} is {hours_to_complete} hours, which is below our engagement threshold of 90 hours.\\n\\n"
#         "Please revisit your course to continue your learning journey.\\n"
#         "Visit: https://www.res4city.eu/\\n\\n"
#         "Best regards,\\n"
#         "The Res4City Team"
#     )
#     return plain_text_template.format(user_name=user_name, hours_to_complete=hours_to_complete, course_code=course_code)


