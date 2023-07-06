import json
import threading
from datetime import datetime
from ModbusRTUServer import app
from flask_socketio import SocketIO, send, emit
from ModbusRTUServer.services.ModbusRTUService import ModbusRTUService

app.config['SECRET_KEY'] = 'secret!'
io = SocketIO(app)
service = None
items = []


@io.on('connect')
def connect():
    emit('init', items, json=True)


@io.on('add')
def add(data):
    if data in items:
        pass
    data['time'] = str(datetime.now())
    items.append(data)
    emit('add', data, json=True, broadcast=True)
    service.add(data)


@io.on('update')
def update(data):
    for index in range(len(items)):
        if data['id'] == items[index]['id']:
            data['time'] = str(datetime.now())
            items[index] = data
            emit('update', data, json=True, broadcast=True)
            break


@io.on('remove')
def remove(data):
    for item in items:
        if data['id'] == item['id']:
            items.remove(item)
            emit('remove', data, json=True, broadcast=True)
            service.remove(data)
            break


def callback(data, callback_type, value):
    if callback_type == 'error':
        io.emit('message', value, json=True, broadcast=True)
    else:
        data['value'] = value
        data['time'] = str(datetime.now())
        print('notify', data)
        io.emit('notify', data, json=True, broadcast=True)


setting = {
    'address': 1,
    'port': None,
    'baudrate': 9600
}
with open('setting.txt') as file:
    setting = json.load(file)
service = ModbusRTUService(
    setting['address'], setting['port'], setting['baudrate'], callback)
