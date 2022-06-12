from flask import Blueprint, render_template, session
from app import db

data = Blueprint("data_blueprint",__name__)
print("admindata_blueprint executed")


@data.route("/user_page", methods=['GET','POST'])
def user_page(*args, **kwargs):

    # email
    # chk_admin = db.execute("SELECT userid FROM assurekit_users WHERE email=%s", (email,))
    return render_template("home.html", user="logged_in")


@data.route("/admin_page",methods=['GET', 'POST'])
def admin_page(*args, **kwargs):

    email = session['user']
    chk_admin = db.execute("SELECT isadmin FROM assurekit_users WHERE email=%s", (email,))

    if chk_admin == True:
        data = db.query_db("SELECT username,email,isadmin FROM public.userdb")
        return jsonify({"users": data})
    else:
        return jsonify({"Message": "User has no permissions."})