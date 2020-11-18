from bson import json_util, ObjectId
from flask import Flask, request
from datetime import datetime

from app.helpers import mongo_client

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))


@app.route('/interactions')
def interactions():
    engagement_id = request.args.get('engagementId')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if engagement_id != None:
        engagement_object_id = ObjectId(engagement_id)

        if start_date and not end_date:
            return json_util.dumps(db.interactions.find({'engagementId': engagement_object_id,\
                    'interactionDate': {"$gte": datetime.fromtimestamp(int(start_date) / 1e3)}}))

        if end_date and not start_date:
            return json_util.dumps(db.interactions.find({'engagementId': engagement_object_id,\
                    'interactionDate': {"$lte": datetime.fromtimestamp(int(end_date) / 1e3)}}))

        if not start_date and not end_date:
            return json_util.dumps(db.interactions.find({'engagementId': engagement_object_id}))

        return json_util.dumps(db.interactions.find({'engagementId': engagement_object_id,\
                'interactionDate':{"$gte": datetime.fromtimestamp(int(start_date) / 1e3),\
                "$lte": datetime.fromtimestamp(int(end_date)/1e3)}}))

    return json_util.dumps(db.interactions.find({}))


@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))
