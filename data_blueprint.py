from flask import Blueprint, render_template, session, flash, redirect, url_for
from app import db
from flask_login import current_user
import datetime

data = Blueprint("data_blueprint",__name__)
print("admindata_blueprint executed")


@data.route("/user_page", methods=['GET','POST'])
def user_page(*args, **kwargs):

    try:
        email = session['user']
    except Exception as err:
        print(err)
        return redirect(url_for('autho.login'))

    chk_user = db.execute("SELECT username,userid,created_on FROM assurekit_users WHERE email=%s", (email,))
    # print(chk_user)
    real_time = datetime.datetime.fromtimestamp(chk_user[2]).strftime('%H:%M %d-%m-%Y')
    return render_template("user_page.html", user="logged_in", output = chk_user[0], output_uid = chk_user[1], output_date = real_time)


@data.route("/admin_page_access", methods=['GET','POST'])
def admin_page_access(*args, **kwargs):

    try:
        email = session['user']
    except Exception as err:
        print(err)
        return redirect(url_for('autho.login'))

    chk_admin = db.execute("SELECT isadmin, username FROM assurekit_users WHERE email=%s", (email,))
    print(chk_admin[0])

    if chk_admin[0]:
        all_user_data = db.query_db("SELECT username,email,isadmin FROM assurekit_users", (email,))
        print("----------")
        print(all_user_data)
        flash('Welcome admin', category='success')
        return render_template("admin_page.html", user="logged_in", items = all_user_data)
    else:
        flash(f'Sorry {chk_admin[1]}, you do not have admin access.', category='error')
        return redirect(url_for('data_blueprint.user_page'))
