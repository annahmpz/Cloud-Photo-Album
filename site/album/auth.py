import functools,pymysql
from flask import Flask,request,render_template,flash,Blueprint,redirect,url_for,session,g
from werkzeug.security import generate_password_hash, check_password_hash
from .form import AuthForm

bp=Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/register',methods=['GET','POST'])
def register():
    form=AuthForm()
    if form.validate_on_submit():
        db = pymysql.connect("mysql_container", "root", "123456", "album")
        cursor = db.cursor()
        email=form.mail.data
        password=form.password.data
        sql1 = "SELECT * FROM user \
            WHERE email = '%s'" % (email)
        cursor.execute(sql1)
        res=cursor.fetchall()
        if res:
            flash('邮箱已注册')
            db.close()
        else:
            sql2 = "INSERT INTO user(email,password) \
                VALUES ('%s', '%s')" % \
                (email,generate_password_hash(password))
            try:
                cursor.execute(sql2)
                db.commit()
            except:
                db.rollback()
            db.close()
            return redirect(url_for('auth.login'))
    return render_template('register.html',form=form)

@bp.route('/login',methods=['GET','POST'])
def login():
    form=AuthForm()
    if form.validate_on_submit():
        db = pymysql.connect("mysql_container", "root", "123456", "album")
        cursor = db.cursor()
        email=form.mail.data
        password=form.password.data
        sql1 = "SELECT * FROM user \
            WHERE email = '%s'" % (email)
        cursor.execute(sql1)
        res=cursor.fetchall()
        db.close()
        if not res:
            flash('用户不存在')
        elif not check_password_hash(res[0][1],password):
            flash('邮箱或密码错误')
        else:
            session.clear()
            session['email']=email
            return redirect(url_for('album.home'))
    return render_template('login.html',form=form)

@bp.before_app_request
def load_logged_in_user():
    user_mail = session.get('email')

    if not user_mail:
        g.user = None
    else:
        g.user = user_mail

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view




