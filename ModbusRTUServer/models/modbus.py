#!/usr/bin/env python3
import sys
import glob
import serial
import minimalmodbus


class ModbusRTU(object):
    def __init__(self, address, port, baudrate=9600):
        # port name, slave address (in decimal)
        if port is None:
            try:
                port = ModbusRTU.serial_ports()[0]
            except:
                raise 'Cannot find any serial port!'
        print('Connect to', port)
        self.instrument = minimalmodbus.Instrument(port, address)
        # this is the serial port name
        # self.instrument.serial.port
        self.instrument.serial.baudrate = baudrate      # Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = 'O'
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 5          # seconds
        self.instrument.close_port_after_each_call = True

    @staticmethod
    def serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def read_bit(self, registeraddress, functioncode=2):
        try:
            return self.instrument.read_bit(registeraddress, functioncode)
        except Exception as error:
            raise error

    def write_bit(self, registeraddress, value, functioncode=5):
        try:
            return self.instrument.write_bit(registeraddress, value, functioncode)
        except Exception as error:
            raise error

    def read_bits(self, registeraddress, number_of_bits, functioncode=2):
        try:
            return self.instrument.read_bits(registeraddress, number_of_bits, functioncode)
        except Exception as error:
            raise error

    def write_bits(self, registeraddress, values):
        try:
            return self.instrument.write_bits(registeraddress, values)
        except Exception as error:
            raise error

    def read_register(self, registeraddress, number_of_decimals=0, functioncode=3, signed=False):
        try:
            return self.instrument.read_register(registeraddress, number_of_decimals, functioncode, signed)
        except Exception as error:
            raise error

    def write_register(
        self,
        registeraddress,
        value,
        number_of_decimals=0,
        functioncode=16,
        signed=False,
    ):
        try:
            return self.instrument.write_register(
                registeraddress,
                value,
                number_of_decimals,
                functioncode,
                signed,
            )
        except Exception as error:
            raise error

    def read_long(
        self, registeraddress, functioncode=3, signed=False, byteorder=0
    ):
        try:
            return self.instrument.read_long(
                registeraddress, functioncode, signed, byteorder
            )
        except Exception as error:
            raise error

    def write_long(self, registeraddress, value, signed=False, byteorder=0):
        try:
            return self.instrument.write_long(registeraddress, value, signed, byteorder)
        except Exception as error:
            raise error

    def read_float(self, registeraddress, functioncode=3, number_of_registers=2, byteorder=0):
        try:
            return self.instrument.read_float(registeraddress, functioncode, number_of_registers, byteorder)
        except Exception as error:
            raise error

    def write_float(self, registeraddress, value, number_of_registers=2, byteorder=0):
        try:
            return self.instrument.write_float(registeraddress, value, number_of_registers, byteorder)
        except Exception as error:
            raise error

    def read_string(self, registeraddress, number_of_registers=16, functioncode=3):
        try:
            return self.instrument.read_string(registeraddress, number_of_registers, functioncode)
        except Exception as error:
            raise error

    def write_string(self, registeraddress, textstring, number_of_registers=16):
        try:
            return self.instrument.write_string(registeraddress, textstring, number_of_registers)
        except Exception as error:
            raise error

    def read_registers(self, registeraddress, number_of_registers, functioncode=3):
        try:
            return self.instrument.read_registers(registeraddress, number_of_registers, functioncode)
        except Exception as error:
            raise error

    def write_registers(self, registeraddress, values):
        try:
            return self.instrument.write_registers(registeraddress, values)
        except Exception as error:
            raise error
