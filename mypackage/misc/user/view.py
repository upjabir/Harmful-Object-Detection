from flask import Blueprint,render_template,redirect,url_for
from user.form import AddForm

user_blueprint=Blueprint('user',__name__,template_folder='templates/user')

@user_blueprint.route('/registor',methods=['GET','POST'])
def registor():
    form=AddForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

    return render_template('user.html',form=form)






