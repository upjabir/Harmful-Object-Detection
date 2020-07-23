from flask import current_app as app
from flask import redirect, render_template, flash, Blueprint, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user,logout_user
from mypackage.form import LoginForm,SignUpForm
from mypackage.models import UserModel
from mypackage import login_manager


auth=Blueprint('auth',__name__,template_folder='templates',static_folder='static')

@auth.route('/signup',methods=['GET','POST'])
def signup():

    signup_form=SignUpForm()
    if request.method=='POST':
   # if signup_form.validate_on_submit():
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(email,password)

        existing_user=UserModel.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exist')
            return redirect(url_for('auth.signup'))

        user=UserModel(username=username,email=email,password=generate_password_hash(password, method='sha256'))
        user.save_to_db()
        return redirect(url_for('auth.login'))

    return render_template('signup.html',form=signup_form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    login_form=LoginForm()
    if request.method == 'POST':
        #if login_form.validate_on_submit():
            email=request.form.get('email')
            password=request.form.get('password')
            print(password)
            remember = True if request.form.get('remember') else False

            user=UserModel.query.filter_by(email=email).first()
            print(user)
            if not user and not check_password_hash(user.password, password):
                print(check_password_hash)
                flash('please check your login credentials')
                return redirect(url_for('auth.login'))

            login_user(user,remember=remember)
            return redirect(url_for('main.profile'))

    return render_template('login.html',form=login_form)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return UserModel.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))






@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))