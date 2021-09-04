
1. clone the project from https://github.com/lalithbachimanchi/Algo_Shlef.git

2. Go into Algo_Shlef folder

Configuring the App:

1. Install Postgres
2. Enter sudo -u postgres psql
3. Enter below commands
	CREATE DATABASE algo_assignment;
	CREATE USER algo_user WITH PASSWORD 'algo_password';
	GRANT ALL PRIVILEGES ON DATABASE algo_assignment TO algo_user;
4. Create virtualenvironment using below commands:
	virtualenv env --python=python3
	source env/bin/activate
5. pip3 install -r requirements.txt
6. flask db init
7. flask db migrate
8. flask db upgrade
9.python app.py to run the application




Application can be tested with below calls:

1. POST http://13.126.130.208:5000/api/cluster/
BODY: {"cluster_name":"Cluster2",
"cloud_region": "Cloud Region2"
}
2. DELETE http://13.126.130.208:5000/api/cluster/?cluster_id=3

3. POST http://13.126.130.208:5000/api/machine/
BODY: {"machine_name":"Machine4",
	"instance_type":"Instance4",
	"cluster_id":2,
	"tags":["sandbox"]
}

4. DELETE http://13.126.130.208:5000/api/machine/?machine_id=1

5. PATCH http://13.126.130.208:5000/api/start/?tag_name=sandbox

6. http://13.126.130.208:5000/api/stop/?tag_name=sandbox

7. http://13.126.130.208:5000/api/reboot/?tag_name=sandbox


This applicated is hosted on AWS EC2 instance on port 5000:

url: ec2-13-126-130-208.ap-south-1.compute.amazonaws.com

Design a RESTful API for managing machines in the cloud
Note: There is no need for actual cloud integration

Context
There will be multiple clusters and each cluster will have zero or more machines. Each machine will have zero or more tags.

Also, each cluster will have a name and a cloud region, each machine will have a name, ip address, an instance-type.

The system should allow users to create clusters, create machines in a cluster, add tags to the machine when creating them, delete machines and clusters and perform operations like start, stop, reboot on a group of machines using tags.

Problem Statement
Your API should do everything required to manage the clusters and machines, except actually creating the machines in the cloud.

Deliverables:
Implementation of the API in Python using Flask or Go lang
Test cases
A README explaining the API instructions about how to run it locally
URL of the application deployed to Heroku/Digital Ocean/GCP/AWS
What are we looking for?
Problem solving approach
API design and it's completeness
