from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import pandas as pd
import os

from werkzeug.utils import secure_filename
from datetime import datetime
import secrets
import bcrypt
import smtplib
from blockchain import *
from collections import defaultdict
import random
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
import os

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# MySQL database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="lightwaitimage",
    charset='utf8',
    port=3306
)
mycursor = mydb.cursor()

# Serializer for generating confirmation tokens
s = URLSafeTimedSerializer(app.secret_key)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['Con_Password']
        phone = request.form['phone']
        address = request.form['address']
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()
        
        if password == password1:
            sql = "SELECT * FROM users WHERE email = %s"
            mycursor.execute(sql, (email,))
            data = mycursor.fetchall()
            
            if data:
                message = "With this email, data is already present."
                return render_template('register.html', message=message)
            else:
                sql = """
                INSERT INTO users (username, password, email, phone, address)
                VALUES (%s, %s, %s, %s, %s)
                """
                val = (username, hashpassword, email, phone, address)
                mycursor.execute(sql, val)
                mydb.commit()
                message = "Registered successfully."
                return render_template('register.html', message=message)
                
    return render_template('register.html')




# Route to confirm email
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    sql = "UPDATE users SET is_verified = %s WHERE email = %s"
    val = (True, email)
    mycursor.execute(sql, val)
    mydb.commit()
    flash('Your account has been verified.', 'success')
    return redirect(url_for('login'))

# Route for login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        hashedpassword = hashlib.md5(password.encode())
        hashpassword = hashedpassword.hexdigest()
        sql = "select * from users where email='%s' and password='%s'" % (email, hashpassword)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if results != []:
            # session['username'] = username
            session['email'] = email
            message = "Login successfully, Welcome to Homepage."
            return render_template('userhome.html',data=results,message=message)
        else:
            message = "Login  Failed Entered Correct Data."
            return render_template('login.html',message=message) 
       
    return render_template('login.html')   


from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
from datetime import datetime
from cryptography.fernet import Fernet
import os
import mysql.connector



# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to encrypt the file using Fernet symmetric encryption
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        original_data = file.read()
    
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(original_data)
    
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

@app.route("/UploadFiles", methods=['POST', 'GET'])
def UploadFiles():
    message = ""
    if request.method == "POST":
        try:
            file = request.files['file']
            Keywords = request.form['Keywords']
            description = request.form['description']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            now = datetime.now()
            current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

            # Check if file already exists in the database
            sql_check = "SELECT * FROM uploadfile WHERE Filename = %s"
            mycursor.execute(sql_check, (filename,))
            existing_file = mycursor.fetchone()
            
            if existing_file:
                message = "File with this name already exists. Please use a different name."
            else:
                # Save the file to the upload folder
                file.save(filepath)

                # Generate encryption key and encrypt the file
                key = generate_key()
                encrypt_file(filepath, key)

                # Insert file details into the database, including the key (stored securely)
                sql_insert = "INSERT INTO uploadfile (doemail, Filename, Keywords, filepath, description, Datetime, encryption_key) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (session['email'], filename, Keywords, filepath, description, current_datetime, key.decode())
                mycursor.execute(sql_insert, values)
                mydb.commit()
                message = "File uploaded and encrypted successfully."
        except Exception as e:
            message = f"An error occurred: {str(e)}"
    return render_template("UploadFiles.html", message=message)


@app.route('/viewfile')
def viewfile():
    sql="select * from uploadfile where doemail='%s' "%(session['email'])
    mycursor.execute(sql,)
    data = mycursor.fetchall()
    print(data)
    return render_template('viewfile.html',data=data)


@app.route('/filerequest')
def filerequest():
    sql = "SELECT * FROM uploadfile"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    return render_template('filerequest.html', data=data)

from flask import Flask, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import pandas as pd
import mysql.connector
import random
from datetime import datetime
from PIL import Image
import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Function to encrypt image data
def encrypt_image(image_bytes, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=b'initialvector123')
    encrypted_bytes = cipher.encrypt(pad(image_bytes, AES.block_size))
    return encrypted_bytes

@app.route('/filerequests/<Id>')
def filerequests(Id):
    sql = "SELECT * FROM uploadfile WHERE Id=%s"
    x = pd.read_sql_query(sql, mydb, params=[Id])

    if not x.empty:
        Id = x.values[0][0]
        doemail = x.values[0][1]
        FileName = x.values[0][2]
        Keyword = x.values[0][3]
        filepath = x.values[0][4]
        description = x.values[0][5]
        encryption_key = x.values[0][7]
        status = 'Requested'
        receiveremail = session.get('email')

        if receiveremail == doemail:
            flash("You are the owner of this file and cannot request it.")
            return redirect(url_for('filerequest'))

        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        otp = random.randint(0, 999999)

        # # Generate image data (black image)
        # width, height = 256, 256  # Define size of the image
        # black_image = Image.new('RGB', (width, height), color='black')
        # buffered = io.BytesIO()
        # black_image.save(buffered, format="JPEG")
        # black_image_bytes = buffered.getvalue()

        # # Encryption key (must be 16 bytes for AES)
        # encryption_key = b'mysecretpassword123'  # Update with a 16-byte key
        
        # # Encrypt the black image
        # encrypted_image = encrypt_image(black_image_bytes, encryption_key)
        
        # # Save encrypted image to file
        # encrypted_image_path = os.path.join('path/to/save', 'encrypted_image.jpg')
        # with open(encrypted_image_path, 'wb') as f:
        #     f.write(encrypted_image)

        # Insert request into database
        sql_insert = """
            INSERT INTO request (FileId, owneremail, receiveremail, otp, FileName, Keyword,encryption_key, description, Files, Datetime, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        val = (Id, doemail, receiveremail, otp, FileName, Keyword,encryption_key, description, filepath, current_datetime, status)
        mycursor.execute(sql_insert, val)
        mydb.commit()

        flash("Request sent successfully")
    else:
        flash("File not found.")
    
    return redirect(url_for('filerequest'))


@app.route('/viewrequest')
def viewrequest():
    sql = "SELECT * FROM request where owneremail='%s'"%(session['email'])
    mycursor.execute(sql)
    data = mycursor.fetchall()
    return render_template('viewrequest.html', data=data)


@app.route("/accept_request/<Id>")
def accept_request(Id):
    try:
        # Fetch the request details
        sql = "SELECT * FROM request WHERE Id=%s"
        mycursor.execute(sql, (Id,))
        request_data = mycursor.fetchone()
        
        if not request_data:
            flash('Request not found.', 'danger')
            return redirect(url_for('viewrequest'))
        
        # Extract email and key from the request
        email = request_data[3]
        key = request_data[7]
        
        # Fetch the file details
        sql = "SELECT * FROM uploadfile WHERE Id=%s"
        mycursor.execute(sql, (Id,))
        file_data = mycursor.fetchone()
        
        if not file_data:
            flash('File not found.', 'danger')
            return redirect(url_for('viewrequest'))
        
        fId = file_data[0]
        
        # Update request status to 'Accepted'
        sql = "UPDATE request SET status='Accepted' WHERE Id=%s"
        mycursor.execute(sql, (Id,))
        mydb.commit()
        
        # Send email
        mail_content = f'Your request is accepted by Admin. Your Secret key is: {key} and File Id is: {fId}'
        sender_address = 'appcloud887@gmail.com'
        sender_pass = 'uihywuzqiutvfofo'
        receiver_address = email
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Request Accepted'
        message.attach(MIMEText(mail_content, 'plain'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            session.starttls()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
        
        flash('Key sent to user email.', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('viewrequest'))

# reject data owner request
@app.route("/reject_request/<Id>")
def reject_request(Id=0):
    print(Id)
    sql = "select * from request where status='Requested'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    print("**********")
    email = dc[0][2]
    # password = dc[0][3]
    print(email)
    
    otp="Your request is Rejected:"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is Rejected by Admin and email is:'+ email + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A Lightweight Image Encryption Algorithm  Based on Secure Key Generation'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql = "update request set status='Rejected' where Id='%s'" % (Id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Your Request Send Rejected By owner Just Try again', 'success')
    return redirect(url_for('viewrequest'))

@app.route('/fileresponse')
def fileresponse():
    sql = "SELECT * FROM request where receiveremail=%s"
    mycursor.execute(sql, (session['email'],))
    data = mycursor.fetchall()
    return render_template('fileresponse.html', data=data)


from cryptography.fernet import Fernet
from flask import send_file, flash

# Function to decrypt the file using Fernet symmetric encryption
def decrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        
        return True
    except Exception as e:
        print(f"An error occurred during decryption: {str(e)}")
        return False

@app.route("/decrypt", methods=['POST', 'GET'])
def decrypt():
    message = ""
    if request.method == "POST":
        file_id = request.form['file_id']
        decryption_key = request.form['decryption_key']
        
        # Fetch file details from the database based on file ID
        sql = "SELECT filepath, encryption_key FROM uploadfile WHERE Id = %s"
        mycursor.execute(sql, (file_id,))
        result = mycursor.fetchone()

        if result:
            filepath = result[0]
            stored_key = result[1].encode()  # Retrieve the encryption key stored in the database

            # Verify the provided key matches the stored key
            if decryption_key.encode() == stored_key:
                if decrypt_file(filepath, stored_key):
                    flash("File decrypted successfully!")
                    return send_file(filepath, as_attachment=True)
                else:
                    message = "Decryption failed. Please try again."
            else:
                message = "Incorrect decryption key."
        else:
            message = "File not found."

    return render_template("decrypt.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)
