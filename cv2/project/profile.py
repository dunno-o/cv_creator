from flask import Blueprint, Flask, redirect, url_for, render_template, request, session, send_file
from flask_login import login_required, current_user
import datetime
import os
import pdfkit
import base64

from .__init__ import db
from .models import CV

profile = Blueprint('profile', __name__, url_prefix='/profile')


@profile.route("/profile")
@login_required
def main():
    return render_template("profile.html", name=current_user.name)


@profile.route("/create", methods=["POST", "GET"])
@login_required
def create():
    if request.method == "POST":
        if request.form['action'] == 'save':
            cv = CV(name=request.form['name'], about=request.form['about'],
    work_experience=request.form['work_experience'], education=request.form['education'], email=request.form['email'],
                    user_id=current_user.id)
            db.session.add(cv)
            db.session.commit()
            session['cv_id'] = cv.id
            return render_template("save_cv.html", cv=cv)

    data = [item for item in CV.query.filter_by(user_id=current_user.id)]
    if len(data) == 0:
        return render_template("save_cv.html",
                               cv=CV(name="", about="", work_experience="", education="",
                                     user_id=current_user.id))
    last = data[-1]
    return render_template("save_cv.html", cv=last)
