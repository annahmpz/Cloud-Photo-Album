from flask import Flask,request,render_template,flash,Blueprint,redirect,url_for,session,g,request,current_app
from .auth import login_required
from .form import ColForm,ChangeForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql,time,datetime,os

bp=Blueprint('album',__name__,url_prefix='/album')
basedir = os.path.abspath(os.path.dirname(__file__))

@bp.route('/home')
@login_required
def home():
    db = pymysql.connect("mysql_container", "root", "123456", "album")
    cursor = db.cursor()
    sql1 = "SELECT * FROM col \
            WHERE user_email = '%s'" % (g.user)
    cursor.execute(sql1)
    res=cursor.fetchall()
    db.close()
    pro=[]
    for row in res:
        item={
            'name':row[1],
            'time':row[2][:10],
            'type':row[3],
            'id':row[0]
        }
        pro.append(item)
    return render_template('home.html',pro=pro)

@bp.route('/detail/<id>')
def detail(id):
    db = pymysql.connect("mysql_container", "root", "123456", "album")
    cursor = db.cursor()
    sql1 = "SELECT * FROM col \
            WHERE id = '%s'" % (id)
    cursor.execute(sql1)
    res=cursor.fetchall()
    col_detail={
        'name':res[0][1],
        'type':res[0][3]
    }
    sql2 = "SELECT * FROM photo \
            WHERE col_id = '%s' ORDER BY create_time DESC" % (id)
    cursor.execute(sql2)
    res2=cursor.fetchall()
    db.close()
    photo_name=[]
    for item in res2:
        photo_name.append(item[0])
    return render_template('file_view.html',photo_name=photo_name,col_detail=col_detail,id=id)

@bp.route('/create',methods=['GET','POST'])
@login_required
def create():
    form=ColForm()
    if request.method=='POST':
        db = pymysql.connect("mysql_container", "root", "123456", "album")
        cursor = db.cursor()
        name=form.name.data
        col_type=form.col_type.data
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        col_id=time.time()
        sql1 = "INSERT INTO col(id,name,create_time,type,user_email) \
                VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                (col_id,name,dt,col_type,g.user)
        try:
            cursor.execute(sql1)
            db.commit()
        except:
            db.rollback()
        db.close()
        return redirect(url_for('album.home'))
    return render_template('import.html',form=form)

@bp.route('/change',methods=['GET','POST'])
@login_required
def change():
    form=ChangeForm()
    if request.method=='POST':
        print(1)
        db = pymysql.connect("mysql_container", "root", "123456", "album")
        cursor = db.cursor()
        old_password=form.old_password.data
        new_password=form.new_password.data
        print(old_password)
        print(new_password)
        sql1 = "SELECT * FROM user \
            WHERE email = '%s'" % (g.user)
        cursor.execute(sql1)
        res=cursor.fetchall()
        if not check_password_hash(res[0][1],old_password):
            flash('密码错误')
            db.close()
            print(2)
        else:
            sql2="UPDATE user SET password = '%s' WHERE email = '%s'" % (generate_password_hash(new_password),g.user)
            try:
                cursor.execute(sql2)
                db.commit()
            except:
                db.rollback()
            db.close()
            flash('修改成功')
            print(3)
    return render_template('change_password.html',form=form)

@bp.route('/upload/<id>', methods=['POST'], strict_slashes=False)
@login_required
def upload(id):
    db = pymysql.connect("mysql_container", "root", "123456", "album")
    cursor = db.cursor()
    file_dir = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['input_file']  # 从表单的file字段获取文件，input_file为该表单的name值
    fname = secure_filename(f.filename)
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time)+'.' + ext  # 修改了上传的文件名
    f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql1 = "INSERT INTO photo(id,create_time,col_id) \
                VALUES ('%s', '%s', '%s')" % \
                (new_filename,dt,id)
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()
    db.close()
    return redirect(url_for('album.detail',id=id))
        