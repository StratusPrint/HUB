#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from Gmail_Send import send_email
from ConfigManager import Config
import flask
import sys
from flask import Flask
from flask import request
from flask import json
from flask import render_template
app = Flask(__name__)

SND_PASSWD = ""

nodes = {}
conf = Config()

@app.route('/activate')
def activate_sensor():
    """API call to register a sensor.
    The UUID and IP should be provided in json format
    as a variable "payload"
    :returns: TODO
    """

    global nodes
    str_payload = request.args.get('payload')
    json_payload = json.loads(str_payload)
    uuid = json_payload["UUID"]
    ip = json_payload["IP"]
    conf_data = conf.read_data()
    if uuid in conf_data:
        nodes[ip] = conf_data[uuid]
    return uuid + " " + ip

@app.route('/register',methods=['GET', 'POST'])
def register_sensor():
    """Webpage to register the type of a given sensor
    This should be done before activating the sensor.
    :returns: webpage of result
    """

    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        uuid = request.form['uuid']
        chiptype = request.form['chiptype']
        if request.form.get('is_update'):
            success = conf.update_data({uuid: chiptype})
            return str(success)
        else:
            success = conf.add_data({uuid: chiptype})
            return str(success)

@app.route('/')
def sensor_recv():
    """Webpage that takes parameter 'payload' from a 
    sensor in json format. It uses UUID and IP from the
    json to register the sensor as available.
    """
    str_data = request.args.get('payload')
    json_data = json.loads(str_data)
    uuid = json_data["UUID"]
    ip = json_data["IP"]

#    send_email(json.dumps(json_data,
#                          sort_keys = True,
#                          indent = 2,
#                          separators=(',', ':')
#                         ),
#              "Sensor Data",
#              snd_psswd = SND_PASSWD
#              )
    return "Message sent"

if __name__ == '__main__':
    #SND_PASSWD = sys.argv[1]
    #app.run(host="192.168.0.1") #need to test this
    app.run(debug=True)