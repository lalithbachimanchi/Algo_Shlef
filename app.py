import os
from flask import Flask
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from flask_restful import Api
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://algo_user:algo_password@localhost/algo_assignment'
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class Cluster(db.Model):
    __tablename__='cluster'
    cluster_id = db.Column(db.Integer, primary_key=True)
    cluster_name = db.Column(db.String(60), nullable=False)
    cloud_region = db.Column(db.String(60), nullable=True)


class Machine(db.Model):
    __tablename__='machine'
    machine_id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(60), nullable=False)
    instance_type = db.Column(db.String(60), nullable=True)
    tags = db.Column(ARRAY(db.String), nullable=True)
    cluster_id = db.Column(db.ForeignKey('cluster.cluster_id'), nullable=False,index=True)
    machine_status = db.Column(db.String(30), nullable=True)


class ClusterAPI(Resource):
    cluster_parser = reqparse.RequestParser()
    cluster_parser.add_argument('cluster_name', required=True, type=str)
    cluster_parser.add_argument('cloud_region', required=False, type=str)

    def post(self):
        create_cluster_data = self.cluster_parser.parse_args()
        create_cluster = Cluster(cluster_name=create_cluster_data['cluster_name'],
                                 cloud_region=create_cluster_data['cloud_region'])
        db.session.add(create_cluster)
        db.session.commit()
        cluster_response = {"message": "Cluster Creation is successful",
                            "data": {"cluster_name": create_cluster.cluster_name,
                                     "cluster_id": create_cluster.cluster_id}}
        return cluster_response, 201

    def delete(self):
        delete_cluster_parser = reqparse.RequestParser().add_argument(
            'cluster_id', required=True, type=int, location='args')
        delete_cluster_data = delete_cluster_parser.parse_args()
        delete_cluster = Cluster.query.filter_by(cluster_id=delete_cluster_data['cluster_id']).first()
        if delete_cluster:
            db.session.delete(delete_cluster)
            db.session.commit()
            return {"message": "Cluster Deletion in Successful"}, 200
        return {"message": "Resource does not exist"}, 400


class MachineAPI(Resource):
    machine_parser = reqparse.RequestParser()
    machine_parser.add_argument('machine_name', required=True, type=str)
    machine_parser.add_argument('instance_type', required=False, type=str)
    machine_parser.add_argument('tags', required=False, type=list, location='json')
    machine_parser.add_argument('cluster_id', required=True, type=int)

    def post(self):
        create_machine_data = self.machine_parser.parse_args()
        create_machine = Machine(machine_name=create_machine_data['machine_name'],
                                 instance_type=create_machine_data['instance_type'],
                                 cluster_id=create_machine_data['cluster_id'],
                                 tags=create_machine_data['tags'])
        db.session.add(create_machine)
        db.session.commit()
        machine_response = {"message": "Machine creation successful",
                            "data": {"machine_id": create_machine.machine_id,
                                     "machine_name": create_machine.machine_name}}
        return machine_response, 201

    def delete(self):
        delete_machine_parser = reqparse.RequestParser().add_argument('machine_id', required=True, type=int, location='args')
        delete_machine_data = delete_machine_parser.parse_args()
        delete_machine = Machine.query.filter_by(machine_id=delete_machine_data['machine_id']).first()
        if delete_machine:
            db.session.delete(delete_machine)
            db.session.commit()
            return {"message": "Machine Deletion is successful"}, 200
        return {"message": "Resource does not exist"}, 400


class StartMachineAPI(Resource):

    def patch(self):
        start_machine_parser = reqparse.RequestParser().add_argument('tag_name', location='args')
        start_machine_data = start_machine_parser.parse_args()
        change_machine_status(start_machine_data['tag_name'], "Started")
        return {"message": "Machine Started Successfully"}, 200

class StopMachineAPI(Resource):

    def patch(self):
        stop_machine_parser = reqparse.RequestParser().add_argument(
            'tag_name', location='args')
        stop_machine_data = stop_machine_parser.parse_args()
        change_machine_status(stop_machine_data['tag_name'], "Stopped")
        return {"message": "Machine Stopped Successfully"}, 200


class RebbotMachineAPI(Resource):

    def patch(self):
        stop_machine_parser = reqparse.RequestParser().add_argument(
            'tag_name', location='args')
        stop_machine_data = stop_machine_parser.parse_args()
        change_machine_status(stop_machine_data['tag_name'], "Restarting")
        return {"message": "Machine Restarted Successfully"}, 200


api.add_resource(ClusterAPI, '/api/cluster/')
api.add_resource(MachineAPI, '/api/machine/')
api.add_resource(StartMachineAPI, '/api/start/')
api.add_resource(StopMachineAPI, '/api/stop/')
api.add_resource(RebbotMachineAPI, '/api/reboot/')

def change_machine_status(tag_name, status_to_update):
    device_ids = set()
    machine_with_tags = Machine.query.filter(Machine.tags!=None).all()
    for each_machine in machine_with_tags:
        if tag_name in each_machine.tags:
            device_ids.add(each_machine.machine_id)
    update_machine = Machine.query.filter(Machine.machine_id.in_(device_ids)).all()
    for upt_mach in update_machine:
        upt_mach.machine_status = status_to_update
    db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
