from flask import render_template, url_for, flash, redirect, request, Blueprint
from tinda import app, conn, bcrypt
from tinda.forms import RegisterUser, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from tinda.models import insert_user, email_exists, delete_user_by_email
from tinda.models import check_user, load_user
from tinda import mysession

Login = Blueprint('Login', __name__)

@Login.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and mysession["email"] != "":
        return render_template('home.html')
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Check if the email already exists
        if not check_user(email,password):
            flash('Login failed. Please check your credentials and try again.', 'error')
        else:
            user = load_user(email)
            login_user(user)
            mysession["id"] = user.id
            mysession["email"] = user.email
            mysession["name"] = user.name
            print(mysession["name"])
            flash('You are now logged in.', 'success')
            return render_template('home.html')
    return render_template('login.html', title='Login', form=form)

@Login.route("/logout")
def logout():
    mysession["state"]="logout"
    logout_user()
    return redirect(url_for('Login.login'))

@Login.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    form.location.choices = [(country, country) for country in get_countries_list()]
    if form.validate_on_submit():
        email = form.email.data
        # Check if the email already exists
        if email_exists(email):
            flash('An account with this email already exists.', 'error')
            return render_template('register.html', title='Register User', form=form)
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email=form.email.data
        name=form.name.data
        description=form.description.data
        date=form.date.data
        location=form.location.data
        password=hashed_password
        insert_user(email, name, description, password, date, location)
        flash('Account has been created! You are now able to log in', 'success')
        return redirect(url_for('Login.login'))
    return render_template('register.html', title='Register user', form=form)

def get_countries_list():
    # Normally, you might load this list from a database or another source
    return ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua & Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia & Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre & Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts & Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Turks & Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]


@Login.route("/deleteuser")
def deleteuser():
    if current_user.is_authenticated:
        delete_user_by_email(mysession["email"])
        mysession["state"]="logout"
        logout_user()
        flash('The user is deleted', 'success')
    return redirect(url_for('Login.login'))

# @Login.route("/")
# @Login.route("/home")
# def home():
#     #202212
#     mysession["state"]="home or /"
#     print(mysession)
#     #202212
#     role =  mysession["role"]
#     print('role: '+ role)

#     return render_template('home.html')


# @Login.route("/about")
# def about():
#     mysession["state"]="about"
#     print(mysession)
#     return render_template('about.html', title='About')


# @Login.route("/direct", methods=['GET', 'POST'])
# def direct():

#     mysession["state"]="direct"
#     print("L1", mysession)
#     role=None

#     if current_user.is_authenticated:
#         return redirect(url_for('Login.home'))
    
#     print("L1", request.args.get('is_employee') )
#     #print("L1", request.form('p') )
    
#     is_employee = True if request.args.get('is_employee') == 'true' else False
#     form = DirectCustomerLoginForm()

#     # Først bekræft, at inputtet fra formen er gyldigt... 
#     if form.validate_on_submit():
        
#         user = select_customer_direct(form.p.data)
#         print("L2 user", user)

#         # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
#         # Her checkes om der er logget på
        
#         if user != None:

#             print("L3 role:" + user.role)
#             mysession["role"] = roles[2] #customer
#             mysession["id"] = form.p.data
#             print("L3", mysession)
#             print("L3", roles)

#             login_user(user, remember=form.remember.data)
#             flash('Login successful.','success')
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('Login.home'))
#         else:
#             flash('Login Unsuccessful. Please check identifier and password', 'danger')
 
#     direct_users = select_customers_direct()
#     print("L2 direct", direct_users)

#     #Get lists of employees and customers
#     teachers = [{"id": str(6234), "name":"anders. teachers with 6."}, {"id": str(6214), "name":"simon"},
#                 {"id": str(6862), "name":"dmitry"}, {"id": str(6476), "name":"finn"}]
#     parents =  [{"id": str(4234), "name":"parent-anders. parents with 4.", "address":"address 1"}
#               , {"id": str(5002), "name":"parent-simon", "address":"address 2"}
#               , {"id": str(4862), "name":"parent-dmitry", "address":"address 3"}
#               , {"id": str(5010), "name":"parent-finn", "address":"address 4"}]
#     students = [{"id": str(5002), "name":"student-anders. students with 5."}, {"id": str(5214), "name":"student-simon"},
#                 {"id": str(5010), "name":"student-dmitry"}, {"id": str(5476), "name":"student-finn"}]

#     return render_template('direct.html', title='Direct Login', is_employee=is_employee, form=form
#     , students=students, radio_direct=direct_users, role=role
#     )






# @Login.route("/login", methods=['GET', 'POST'])
# def login():

#     mysession["state"]="login"
#     print(mysession)
#     role=None

#     if current_user.is_authenticated:
#         return redirect(url_for('Login.home'))

#     is_employee = True if request.args.get('is_employee') == 'true' else False
#     form = EmployeeLoginForm() if is_employee else CustomerLoginForm()

#     # Først bekræft, at inputtet fra formen er gyldigt... 
#     if form.validate_on_submit():

#         #
#         # her checkes noget som skulle være sessionsvariable, men som er en GET-parameter
#         # implementeret af AL. Ideen er at teste på om det er et employee login
#         # eller om det er et customer login.
#         # betinget tildeling. Enten en employee - eller en customer instantieret
#         # Skal muligvis laves om. Hvad hvis nu user ikke blir instantieret
#         #
#         user = select_Employee(form.id.data) if is_employee else select_Customer(form.id.data)

#         # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
#         # Her checkes om der er logget på

#         # if user != None and bcrypt.check_password_hash(user[2], form.password.data):
#         if user != None and user[2] == form.password.data:
#             print("role:" + user.role)
#             if user.role == 'employee':
#                 mysession["role"] = roles[1] #employee
#             elif user.role == 'customer':
#                 mysession["role"] = roles[2] #customer
#             else:
#                 mysession["role"] = roles[0] #ingen

#             mysession["id"] = form.id.data
#             print(mysession)
#             print(roles)

#             login_user(user, remember=form.remember.data)
#             flash('Login successful.','success')
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('Login.home'))
#         else:
#             flash('Login Unsuccessful. Please check identifier and password', 'danger')

#     return render_template('login.html', title='Login', is_employee=is_employee, form=form
#     , role=role
#     )


# @Login.route("/account")
# @login_required
# def account():
#     mysession["state"]="account"
#     print(mysession)
#     role =  mysession["role"]
#     print('role: '+ role)

#     accounts = select_cus_accounts(current_user.get_id())
#     print(accounts)
#     return render_template('account.html', title='Account'
#     , acc=accounts, role=role
#     )

