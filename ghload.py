from rhino3dm import *
import compute_rhino3d.Util
import compute_rhino3d.Brep
import rhino3dm
import requests
import pprint
import base64
import json

compute_rhino3d.Util.authToken = ""
compute_rhino3d.Util.url = "http://127.0.0.1:8081/"

post_url = compute_rhino3d.Util.url + "grasshopper"

gh_data = open("./voronoi.ghx", mode="r", encoding="utf-8-sig").read()
data_bytes = gh_data.encode("utf-8")
encoded = base64.b64encode(data_bytes)
decoded = encoded.decode("utf-8")

response = requests.post(post_url, json={
    "algo": decoded,
    "pointer": None,
    "values": [
        {
            "ParamName": "RH_IN:Size",
            "InnerTree": {
                "{ 0; }": [
                    {
                        "type": "System.Double",
                        "data": "100.0"
                    }
                ]
            }
        }
    ]
})

res = response.content.decode("utf-8")
res = json.loads(res)

values = res["values"]

for val in values:
    paramName = val['ParamName']
    print(paramName)
    innerTree = val['InnerTree']
    for key, innerVals in innerTree.items():
        print(key)
        for innerVal in innerVals:
            data = json.loads(innerVal['data'])
            geo = rhino3dm.CommonObject.Decode(data)
            pprint.pprint(geo)