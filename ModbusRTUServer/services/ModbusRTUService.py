import threading
import time
from ModbusRTUServer.models.modbus import ModbusRTU
from ModbusRTUServer.models.ultis import REGISTER_TYPE


class RealtimeModbusRTU(threading.Thread):
    def __init__(self, service, data):
        super(RealtimeModbusRTU, self).__init__()
        self.service = service
        self.data = data
        self.callback = service.callback
        self.stop = False

    def exit(self):
        self.stop = True

    def run(self):
        fc = None
        if self.data['type'] == REGISTER_TYPE.COILS:
            fc = 1
        elif self.data['type'] == REGISTER_TYPE.DISCRETE_INPUTS:
            fc = 2
        elif self.data['type'] == REGISTER_TYPE.HOLDING_REGISTERS:
            fc = 3
        elif self.data['type'] == REGISTER_TYPE.INPUT_REGISTERS:
            fc = 4
        else:
            pass

        if fc < 3:
            while not self.stop:
                try:
                    self.callback(
                        self.data, 'notify', self.service.modbus.read_bit(self.data['reg'], fc))
                except Exception as error:
                    self.callback(self.data, 'error', error.args)
                finally:
                    time.sleep(5)
        else:
            while not self.stop:
                try:
                    self.callback(
                        self.data, 'notify', self.service.modbus.read_register(self.data['reg'], 1, fc))
                except Exception as error:
                    self.callback(self.data, 'error', error.args)
                finally:
                    time.sleep(5)


class ModbusRTUService():

    def __init__(self, address, port, baudrate, callback):
        self.modbus = ModbusRTU(address, port, baudrate)
        self.threads = []
        self.callback = callback

    def add(self, data):
        for thread in self.threads:
            if thread.name == data['id']:
                pass
        thread = RealtimeModbusRTU(self, data)
        thread.name = data['id']
        self.threads.append(thread)
        thread.start()

    def remove(self, data):
        for thread in self.threads:
            if thread.name == data['id']:
                self.threads.remove(thread)
                thread.exit()
                break
