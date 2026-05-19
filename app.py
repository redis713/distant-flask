from datetime import datetime

from flask import Flask, render_template, request, flash, send_file, redirect, url_for, Response, session
from flask_migrate import Migrate
from config import Config
from loader import load_data
from models import db, Listener, Program
from lpgenerator import generate
from sqlalchemy import or_
from export_csv import export_csv_file
from mailsender import send_email

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    all_listeners=Listener.query.all()
    return render_template("index.html", all_listeners=all_listeners)
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        lastname = request.form["lastname"]
        firstname = request.form["firstname"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        job =request.form["job"]
        phone = request.form["phone"]
        institution = request.form["institution"]

        listener = Listener(
            lastname=lastname,
            firstname=firstname,
            username=username,
            password=password,
            email=email,
            start_date=start_date,
            end_date=end_date,
            job=job,
            phone=phone,
            institution=institution
        )

        program_ids = request.form.getlist("programs")
        programs = Program.query.filter(Program.id.in_(program_ids)).all()

        listener.programs = programs

        db.session.add(listener)
        db.session.commit()

        return redirect(url_for("index"))


    programs = Program.query.all()
    return render_template("add.html", programs=programs)


@app.route("/add_program", methods=["GET", "POST"])
def add_program():
    if request.method == "POST":
        course_id = request.form["course_id"]
        title = request.form["title"]

        program = Program(course_id=course_id, title=title)

        db.session.add(program)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_program.html")

@app.route("/change/<int:listener_id>", methods=["GET", "POST"])
def change(listener_id):
    listener = Listener.query.get(listener_id)

    if request.method == "POST":
        listener.lastname = request.form["lastname"]
        listener.firstname = request.form["firstname"]
        listener.username = request.form["username"]
        listener.password = request.form["password"]
        listener.email = request.form["email"]
        listener.start_date = request.form["start_date"]
        listener.end_date = request.form["end_date"]
        listener.job =request.form["job"]
        listener.phone = request.form["phone"]
        listener.institution = request.form["institution"]

        program_ids = request.form.getlist("programs")
        programs = Program.query.filter(Program.id.in_(program_ids)).all()
        listener.programs = programs

        db.session.commit()

        return redirect(url_for("index"))
    programs = Program.query.all()
    return render_template("change.html", listener=listener, programs=programs)

@app.route("/delete/<int:listener_id>", methods=["GET", "POST"])
def delete(listener_id):
    listener = Listener.query.get(listener_id)
    db.session.delete(listener)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add_login", methods=["GET"])
def add_login():
    listeners = Listener.query.filter(Listener.username == "").all()

    for listener in listeners:
        username, password = generate(listener.lastname, listener.firstname)
        listener.username = username
        listener.password = password

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/send_mail/<int:listener_id>", methods=["GET", "POST"])
def send_mail(listener_id):
    listener = Listener.query.get(listener_id)
    send_email(listener.email, listener.firstname, listener.username, listener.password, listener.start_date.strftime('%d.%m.%Y'), listener.end_date.strftime('%d.%m.%Y'))
    return redirect(url_for("index"))


@app.route("/search", methods=["POST"])
def search():
    search = request.form["search"]
    if search =="":
        return redirect(url_for("index"))
    listeners = Listener.query.filter(or_(Listener.lastname.ilike(f"%{search}%"), Listener.firstname.ilike(f"%{search}%"),
                                          Listener.email.ilike(f"%{search}%"), Listener.job.ilike(f"%{search}%"),
                                          Listener.institution.ilike(f"%{search}%"), Listener.phone.ilike(f"%{search}%"))).all()
    return render_template("index.html", all_listeners=listeners, search_value=search)


@app.route("/import_from_csv", methods=["POST"])
def import_from_csv():
    import_csv = request.files.get("file")

    import_list = load_data(import_csv)

    for record in import_list:

        existing_listener = Listener.query.filter(Listener.lastname == record[0][0], Listener.firstname == record[0][1], Listener.email == record[0][4], Listener.job == record[0][7] ).first()

        if existing_listener:
            programs = Program.query.filter(Program.id.in_(record[1])).all()

            for program in programs:

                if program not in existing_listener.programs:
                    existing_listener.programs.append(program)

            existing_listener.start_date = datetime.strptime(record[0][5], '%d.%m.%Y').date()
            existing_listener.end_date = datetime.strptime(record[0][6], '%d.%m.%Y').date()
            existing_listener.phone = record[0][8]
            existing_listener.institution = record[0][9]

            db.session.commit()
            continue

        new_listener = Listener(
            lastname=record[0][0],
            firstname=record[0][1],
            username=record[0][2],
            password=record[0][3],
            email=record[0][4],
            start_date=datetime.strptime(record[0][5], '%d.%m.%Y').date(),
            end_date=datetime.strptime(record[0][6], '%d.%m.%Y').date(),
            job=record[0][7],
            phone=record[0][8],
            institution=record[0][9],
        )

        programs = Program.query.filter(Program.id.in_(record[1])).all()
        new_listener.programs = programs

        db.session.add(new_listener)
        db.session.commit()

    return redirect(url_for("index"))

@app.route("/export_csv", methods=["POST"])
def export_csv():
    date = request.form.get("date")
    code = request.form.get("code")
    export_list = Listener.query.filter(Listener.start_date == date).all()
    csv_file = export_csv_file(export_list, code)
    if code == 1:
        downloadname='export_moodle.csv'
    else:
        downloadname='contact.csv'

    # тут в загрузки отлетает
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=downloadname
    )

'''
@app.route("/export_sendlist", methods=["POST"])
def export_sendlist():
    date = request.form.get("date")
    export_sl =

'''
if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)

