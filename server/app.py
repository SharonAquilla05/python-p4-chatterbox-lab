from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        return make_response(
            jsonify(messages), 
            200
        )
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            username=data.get("username"),
            body=data.get("body")
        )
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        response = make_response(
            jsonify(message_dict),
            201
        )
        response.headers["Content-Type"] = "application/json"
        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def message(id):
    message = Message.query.filter_by(id=id).first()

    if message is None:
        return make_response(
            jsonify({"error": "Message not found"}),
            404
        )

    if request.method == 'GET':
        message_serialized = message.to_dict()
        return make_response(
            jsonify(message_serialized),
            200
        )
    elif request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Message deleted"
        }
        response = make_response(
            jsonify(response_body),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response

if __name__ == '__main__':
    app.run(port=5555)