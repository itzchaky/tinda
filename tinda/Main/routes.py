from flask import render_template, url_for, flash, redirect, request, Blueprint, send_from_directory
from tinda import app, conn, bcrypt
from flask_login import current_user
from tinda.models import delete_picture, load_chats, select_swipe, update_or_insert_match, dislike_match, load_messages, save_message
from tinda.models import  load_user, insert_picture, select_pictures
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import random


import sys, datetime

#202212
# roles is defined in the init-file
from tinda import roles, mysession

UPLOAD_FOLDER = 'static/uploads'


Main = Blueprint('Main', __name__)


@Main.route("/settings")
def settings():
    if not current_user.is_authenticated or mysession["id"] == 0:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    user = load_user(mysession["email"])
    pictures = select_pictures(mysession["id"])
    print(pictures)
    return render_template('myprofile.html', title='settings', user=user, pictures=pictures)


@Main.route("/messages")
def messages():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    
    user = mysession["id"]
    chats = load_chats(mysession["id"])
    return render_template('messages.html', chats=chats, user=user)


@Main.route("/swipe")
def swipe():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    match = select_swipe(mysession["id"])
    if match:
        pictures = select_pictures(match.id)
        age = calculate_age(str(match.birth))
    else:
        age = ""
        pictures = ""
    print(pictures)
    return render_template('swipe.html', title='settings', match=match, pictures=pictures, age = age)


@Main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('Main.settings'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('Main.settings'))
    if file:
        random_number = random.randint(1000, 9999)
        _, file_extension = os.path.splitext(secure_filename(file.filename))
        filename = str(mysession["id"]) + "-" + str(random_number) + file_extension
        filepath = os.path.join(os.path.join(Main.root_path, UPLOAD_FOLDER), filename)
        file.save(filepath)
        insert_picture(filename,mysession["id"])
        flash('File Uploaded Successfully.','Succes')
        return redirect(url_for('Main.settings'))


@Main.route('/deletepicture/<filename>')
def deletepicture(filename):
    delete_picture(filename)
    return redirect(url_for('Main.settings'))

@Main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@Main.route('/chat/<matchedId>')
def chat(matchedId):
    user = mysession['id']
    messages = load_messages(user, matchedId)
    return render_template('chat.html', messages=messages, matchedId=matchedId)

@Main.route('/goto_chat/<personUserMatchedWith>')
def goto_chat(personUserMatchedWith):
    return redirect(url_for('Main.chat', matchedId=personUserMatchedWith))
    
@Main.route('/send_message/<matchedId>', methods=['POST'])
def send_message(matchedId):
    user = mysession['id']
    message = request.form['message']
    save_message(user, matchedId, message)
    return redirect(url_for('Main.chat', matchedId=matchedId))

def calculate_age(birthdate, reference_date=None):
    # Parse the birthdate string into a datetime object
    birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
    
    # Use today's date as the reference if no reference date is given
    if reference_date is None:
        reference_date = datetime.datetime.today()
    else:
        reference_date = datetime.datetime.strptime(reference_date, "%Y-%m-%d")
    
    # Calculate the difference between the reference date and the birthdate
    age = reference_date.year - birthdate.year
    
    # Adjust the age if the reference day has not yet occurred in the current year
    if (reference_date.month, reference_date.day) < (birthdate.month, birthdate.day):
        age -= 1
    
    return age


@Main.route('/like/<id>')
def match(id):
    update_or_insert_match(mysession["id"],id)
    return redirect(url_for('Main.swipe'))

@Main.route('/dislike/<id>')
def match_dislike(id):
    dislike_match(mysession["id"],id)
    return redirect(url_for('Main.swipe'))


# @Customer.route("/invest", methods=['GET', 'POST'])
# def invest():

#     #202212
#     # Her laves et login check
#     if not current_user.is_authenticated:
#         flash('Please Login.','danger')
#         return redirect(url_for('Login.login'))

#     #202212
#     #customer
#     # CUS4; CUS4-1, CUS4-4
#     # TODO-CUS There us no customer counterpart
#     if not mysession["role"] == roles[iCustomer]:
#         flash('Viewing investents is customer only.','danger')
#         return redirect(url_for('Login.login'))


#     mysession["state"]="invest"
#     print(mysession)

#     #202212
#     # i think this view works for employee and customer but the
#     # view is different as employees have customers.
#     # CUS4; CUS4-1, CUS4-4
#     print(current_user.get_id())

#     investments = select_cus_investments(current_user.get_id())
#     investment_certificates = select_cus_investments_with_certificates(current_user.get_id())
#     investment_sums = select_cus_investments_certificates_sum(current_user.get_id())
#     return render_template('invest.html', title='Investments', inv=investments
#     , inv_cd_list=investment_certificates
#     , inv_sums=investment_sums)


# @Customer.route("/deposit", methods=['GET', 'POST'])
# def deposit():
#     if not current_user.is_authenticated:
#         flash('Please Login.','danger')
#         return redirect(url_for('Login.login'))


#     if not mysession["role"] == roles[iEmployee]:
#         flash('Deposit is employee only.','danger')
#         return redirect(url_for('Login.login'))

#     mysession["state"]="deposit"
#     print(mysession)


#     form = DepositForm()
#     if form.validate_on_submit():
#         amount=form.amount.data
#         CPR_number = form.CPR_number.data
#         update_CheckingAccount(amount, CPR_number)
#         flash('Succeed!', 'success')
#         return redirect(url_for('Login.home'))
#     return render_template('deposit.html', title='Deposit', form=form)

# @Customer.route("/summary", methods=['GET', 'POST'])
# def summary():
#     if not current_user.is_authenticated:
#         flash('Please Login.','danger')
#         return redirect(url_for('Login.login'))
#     if form.validate_on_submit():
#         pass
#         flash('Succeed!', 'success')
#         return redirect(url_for('Login.home'))
#     return render_template('deposit.html', title='Deposit', form=form)
