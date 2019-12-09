import pymongo

myclient = pymongo.MongoClient("mongodb://157.230.44.229:27017/", username='root', password='root', authSource='logs', authMechanism='SCRAM-SHA-256')
mydb = myclient["logs"]
mycol = mydb["bruteforce"]

myDict = { "time": 12.4534, "N": 5 }

x = mycol.insert_one(myDict)

print(x)