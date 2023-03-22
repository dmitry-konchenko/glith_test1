from flask import Flask, render_template, redirect
from tests.users_resourse import UsersResource, UsersListResource

from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, logout_user, login_required
from data.login_form import LoginForm
from data.job_form import JobForm
from data import jobs_api
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    names = {user.id: (user.surname, user.name) for user in users}
    return render_template("index.html", jobs=jobs, names=names)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    add_form = JobForm()
    if not add_form.validate_on_submit():
        return render_template('add_job.html', title='Добавление работы', form=add_form)
    db_sess = db_session.create_session()
    jobs = Jobs(
        job=add_form.job_title.data,
        team_leader=add_form.team_leader.data,
        work_size=add_form.duration.data,
        collaborations=add_form.collaborations.data,
        is_finished=add_form.is_job_finished.data
    )
    db_sess.add(Jobs)
    db_sess.commit()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init('db/users.sqlite')
    app.register_blueprint(jobs_api.blueprint)
    api = Api(app, catch_all_404s=True)
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:news_id>')
    app.run(port=8080, host='127.0.0.1')
