from sqlalchemy.exc import IntegrityError

import flask
from flask import jsonify, Response, request
from sqlalchemy import select

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    jobs_dict = [
        item.to_dict(
            only=('id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
        for item in jobs]
    return jsonify({
        'jobs': jobs_dict
    })


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id: int) -> Response | tuple:
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if job is None:
        return jsonify({'error': 'Not found'}), 404
    fields = ('id', 'job', 'team_leader', 'work_size', 'collaborators',
              'start_date', 'end_date', 'is_finished')
    return jsonify({
        'job': job.to_dict(only=fields),
    })


@blueprint.route('/api/news', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Not all fields'}), 400
    db_sess = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborations=request.json['collaborations'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    try:
        db_sess.commit()
    except IntegrityError as error:
        if 'UNIQUE constant failed: jobs.id' not in str(error):
            raise
        return jsonify({'error': 'Id already exists'}), 400
    db_sess.commit()
    return jsonify({'success': 'OK'}), 201
