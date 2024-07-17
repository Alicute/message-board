import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)
app.secret_key = 'aaaaaaaaaa6666666'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():

    qr_url = request.url
    qr = qrcode.make(qr_url)
    qr.save(os.path.join('static', 'qrcode.png'))
    messages = Message.query.order_by(Message.time.desc()).all()
    messages = [{'id': msg.id, 'content': msg.content, 'time': msg.time.strftime('%Y-%m-%d %H:%M:%S')} for msg in
                messages]
    return render_template('index.html', qr_url=qr_url, messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    content = request.json.get('content')
    new_message = Message(content=content, time=datetime.now())
    db.session.add(new_message)
    db.session.commit()
    messages = Message.query.all()
    return jsonify({'messages': [{'id': msg.id, 'content': msg.content, 'time': msg.time.strftime('%Y-%m-%d %H:%M:%S')}
                                 for msg in messages]})


@app.route('/delete_message', methods=['POST'])
def delete_message():
    msg_id = request.json.get('id')
    message = Message.query.get(msg_id)
    if message:
        db.session.delete(message)
        db.session.commit()
    messages = Message.query.all()
    return jsonify({'messages': [{'id': msg.id, 'content': msg.content, 'time': msg.time.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]})


@app.route('/delete_selected_messages', methods=['POST'])
def delete_selected_messages():
    ids = request.json.get('ids')
    for msg_id in ids:
        message = Message.query.get(msg_id)
        if message:
            db.session.delete(message)
    db.session.commit()
    messages = Message.query.all()
    return jsonify({'messages': [{'id': msg.id, 'content': msg.content, 'time': msg.time.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]})


@app.route('/edit_message', methods=['POST'])
def edit_message():
    msg_id = request.json.get('id')
    new_content = request.json.get('content')
    message = Message.query.get(msg_id)
    if message:
        message.content = new_content
        db.session.commit()
    messages = Message.query.all()
    return jsonify({'messages': [{'id': msg.id, 'content': msg.content, 'time': msg.time.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
