#!/usr/bin/env python
# Copyright 2022
# author: Luis Ackermann <ackermann.luis@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import serial
import time
import sys


def list_files_recursive(path_, filter_str=None):
    # create list of raw spectra files
    file_list = []
    # r=root, d=directories, f = files
    if filter_str is None:
        for r, d, f in os.walk(path_):
            for file in f:
                filename_ = os.path.join(r, file)
                file_list.append(filename_.replace('\\','/'))
    else:
        for r, d, f in os.walk(path_):
            for file in f:
                if filter_str in file:
                    filename_ = os.path.join(r, file)
                    file_list.append(filename_.replace('\\', '/'))
    return sorted(file_list)


output_path = '/home/mrr/Data_Parsivel/PAR_'
port_ = '/dev/ttyUSB1'

com_ports_list = list_files_recursive('/dev/', 'ttyUSB')
error_encountered = False
current_try_port_index = 0

while True:
    try:
        interface = serial.Serial(port=port_,
                                  baudrate=19200,
                                  parity=serial.PARITY_NONE,
                                  bytesize=serial.EIGHTBITS,
                                  stopbits=serial.STOPBITS_ONE,
                                  )
        # read any stuff in the buffer
        time_reading_start = time.time()
        while interface.inWaiting().bit_length() > 0:
            if time.time() > time_reading_start + 60:
                raise ValueError('hang while reading telegram, restarting connection')
            ibuffer = interface.read()
        print('initialized connection')
        time.sleep(5)
        interface.write(b'CS/Z/1\r\n')  # restarts the sensor
        print('sensor restarted, please wait about 10 seconds')
        time.sleep(10)
        interface.write(b'CS/M/S/%13;%01;%02;%03;%05;%06;%07;%08;%11;%12;%17;%18;%34;%35;%93;\n\r\n')  # sets structure of user defined telegram
        header_ = 'datetime;sensor_serial_number;rain_intensity_mm/hr;rain_accumulated_mm;weather_code_SYNOP;'+\
                  'weather_code_METAR;weather_code_NWS;radar_reflectivity_dBz;MOR_visibility_m;' + \
                  'number_of_particles_detected;sensor_temperature;power_supply_voltage_V;sensor_status;' + \
                  'kinetic_energy_J/m2h;snow_intensity_mm/h;raw_spectra;\n'
        # for i_, h_ in enumerate(header_.split(';')):print(i_, h_)
        print('configured telegram')
        time.sleep(1)
        interface.write(b'CS/M/M/1\r\n')  # sets telegram to user defined
        time.sleep(1)
        print('getting current configuration')
        interface.write(b'CS/I/60\r\n')  # polls data
        time.sleep(1)
        interface.write(b'CS/L\r\n')  # get config
        time.sleep(1)

        txt = ''.encode()
        # get response for configuration and print
        time_reading_start = time.time()
        while interface.inWaiting().bit_length() > 0:
            if time.time() > time_reading_start + 60:
                raise ValueError('hang while reading telegram, restarting connection')
            ibuffer = interface.read()
            txt += ibuffer
        txt = txt.decode()
        print(txt)

        print('-' * 40)
        print('starting acquisition loop')

        while True:

            data_not_received = True
            while data_not_received:
                time.sleep(1)
                time_ = time.localtime()
                date_ = time.strftime('%Y%m%d', time_)
                txt = time.strftime('%Y-%m-%d_%H:%M:%S;', time_).encode()

                time_reading_start = time.time()
                while interface.inWaiting().bit_length() > 0:
                    if time.time() > time_reading_start + 60:
                        raise ValueError('hang while reading telegram, restarting connection')
                    ibuffer = interface.readline()
                    txt += ibuffer
                    data_not_received = False
            txt = txt.decode()
            txt_list = txt.strip().split(';')

            if len(txt_list) == 1040:

                if os.path.isfile(output_path + date_ + '.csv'):
                    with open(output_path + date_ + '.csv', 'a') as file_:
                        file_.write(txt)
                else:
                    with open(output_path + date_ + '.csv', 'w') as file_:
                        file_.write(header_)
                        file_.write(txt)


                print(txt_list[0],
                      'precipitation intensity: {0} mm/hr'.format(txt_list[2]),
                      'precipitation type: {0} (NWS)'.format(txt_list[6]))
            else:
                print('skipping time stamp as telegram was received incomplete')

            time.sleep(45)

            # interface.close()
    except BaseException as error_msg:
        if error_encountered:
            while True:
                print('searching available ports')
                com_ports_list = list_files_recursive('/dev/', 'ttyUSB')
                if len(com_ports_list) > 0:
                    if current_try_port_index >= len(com_ports_list) - 1:
                        current_try_port_index = 0
                    else:
                        current_try_port_index += 1
                    port_ = com_ports_list[current_try_port_index]
                    break
                else:
                    time.sleep(3)

        error_encountered = True
        line_number = sys.exc_info()[-1].tb_lineno
        print('error in line {0}, error message:\n{1}'.format(line_number, error_msg))
        try:
            print('trying to close the connection to open it again (reset it)')
            time.sleep(5)
            interface.close()
            time.sleep(5)
            print('successfully closed!')
        except:
            pass
