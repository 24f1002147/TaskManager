from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_token_required, hash_password, verify_password
from flask_cors import CORS
import uuid
import datetime

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'mysecretkey123'
app.config['SECURITY_PASSWORD_SALT'] = 'somesaltvalue'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskapp.db'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['SECURITY_TOKEN_MAX_AGE'] = None

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(500))
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)

with app.app_context():
    db.create_all()


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400

    existing = user_datastore.find_user(email=email)
    if existing:
        return jsonify({'msg': 'user already exists'}), 400

    user = user_datastore.create_user(
        email=email,
        password=hash_password(password),
        fs_uniquifier=uuid.uuid4().hex,
        active=True
    )
    db.session.commit()

    return jsonify({'msg': 'user created', 'email': user.email})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = user_datastore.find_user(email=email)
    if user is None:
        return jsonify({'msg': 'bad email or password'}), 401

    if not verify_password(password, user.password):
        return jsonify({'msg': 'bad email or password'}), 401

    token = user.get_auth_token()
    return jsonify({'token': token, 'email': user.email, 'user_id': user.id})


@app.route('/api/tasks', methods=['GET'])
@auth_token_required
def get_tasks():
    from flask_security import current_user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    result = []
    for t in tasks:
        result.append({
            'id': t.id,
            'title': t.title,
            'desc': t.desc,
            'done': t.done,
            'priority': t.priority
        })
    return jsonify(result)


@app.route('/api/tasks', methods=['POST'])
@auth_token_required
def add_task():
    from flask_security import current_user
    data = request.get_json()

    if data.get('title') == None or data.get('title') == '':
        return jsonify({'msg': 'title is required'}), 400

    t = Task()
    t.title = data.get('title')
    t.desc = data.get('desc')
    t.priority = data.get('priority') if data.get('priority') else 'medium'
    t.user_id = current_user.id
    db.session.add(t)
    db.session.commit()

    return jsonify({'msg': 'task added', 'id': t.id})


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@auth_token_required
def update_task(task_id):
    from flask_security import current_user
    t = Task.query.get(task_id)

    if t == None:
        return jsonify({'msg': 'not found'}), 404

    if t.user_id != current_user.id:
        return jsonify({'msg': 'not allowed'}), 403

    data = request.get_json()
    if 'title' in data:
        t.title = data['title']
    if 'desc' in data:
        t.desc = data['desc']
    if 'done' in data:
        t.done = data['done']
    if 'priority' in data:
        t.priority = data['priority']

    db.session.commit()
    return jsonify({'msg': 'updated'})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@auth_token_required
def delete_task(task_id):
    from flask_security import current_user
    t = Task.query.get(task_id)

    if t == None:
        return jsonify({'msg': 'not found'}), 404

    if t.user_id != current_user.id:
        return jsonify({'msg': 'not allowed'}), 403

    db.session.delete(t)
    db.session.commit()
    return jsonify({'msg': 'deleted'})


if __name__ == '__main__':
    app.run(debug=False, port=5000)
