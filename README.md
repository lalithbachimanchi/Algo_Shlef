
1. clone the project from https://github.com/lalithbachimanchi/Algo_Shlef.git
2. Go into Algo_Shlef folder and enter python app.py


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

