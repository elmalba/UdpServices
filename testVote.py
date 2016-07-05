import requests
from core.crypto import *
import json
import threading


import psycopg2

def notification(rut,opcion):
	threads = list()
	t = threading.Thread(target=notification_url, args=(rut,opcion,))
	threads.append(t)
	t.start()

def notification_url(rut,opcion):

    url = "http://127.0.0.1:5080/Votar"

    if opcion =='No':
        opcion="Clases"
    if opcion =="Toma" or opcion=='Paro':
        opcion="Paro Indefinido"

    payload = json.dumps({"rut":rut,"opcion":opcion})
    headers = {
        'accept': "application/json, text/plain, */*",
        'origin': "https://udpcursos.com",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        'content-type': "application/json;charset=UTF-8",
        'referer': "https://udpcursos.com/",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "es-ES,es;q=0.8,en;q=0.6",
        'cache-control': "no-cache",
        'postman-token': "8f9c65df-b839-32e9-5fff-e69f37663727"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    #print payload

    text = json.loads(response.text)

    if text['message'] != "Tu voto ya fue emitido":
        print payload
        print text



DBNAME="votaciones2"
USER="postgres"
PASSWD="mmae2010"
HOST="localhost"
conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %(DBNAME, USER, HOST,PASSWD))
cur = conn.cursor()
cur.execute("SELECT token,opcion from available,votes where available.hash_id = votes.hash_id ;")
rows = cur.fetchall()
print "\nShow me the databases:\n"
for row in rows:
        rut=decode_token(row[0])[0]
        opcion=row[1]
        notification(rut,opcion)
cur.close()
conn.close()




