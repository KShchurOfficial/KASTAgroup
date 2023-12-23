from neurosdk.scanner import Scanner
from neurosdk.cmn_types import *

import concurrent.futures
from time import sleep


def sensor_found(scanner, sensors):
    for index in range(len(sensors)):
        print('Сенсор найден: %s' % sensors[index])


def on_sensor_state_changed(sensor, state):
    print('Сенсор {0} это {1}'.format(sensor.name, state))


def on_battery_changed(sensor, battery):
    print('Батарея: {0}'.format(battery))


def on_signal_received(sensor, data):
    print(data)


def on_resist_received(sensor, data):
    print(data)


def on_mems_received(sensor, data):
    print(data)


def on_fpg_received(sensor, data):
    print(data)


def on_amp_received(sensor, data):
    print(data)


try:
    scanner = Scanner([SensorFamily.LEBrainBit])

    scanner.sensorsChanged = sensor_found
    print("Начинаем сканирование...")
    scanner.start()
    sleep(7)
    scanner.stop()

    sensorsInfo = scanner.sensors()

    for i in range(len(sensorsInfo)):
        current_sensor_info = sensorsInfo[i]
        print(sensorsInfo[i])

        def device_connection(sensor_info):
            return scanner.create_sensor(sensor_info)


        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(device_connection, current_sensor_info)
            sensor = future.result()
            print("Подключение устройства")

        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.batteryChanged = on_battery_changed

        sensFamily = sensor.sens_family

        sensorState = sensor.state
        if sensorState == SensorState.StateInRange:
            print("Подключено")
        else:
            print("Не подключено")

        print(sensFamily)
        print(sensor.features)
        print(sensor.commands)
        print(sensor.parameters)
        print(sensor.name)
        print(sensor.state)
        print(sensor.address)
        print(sensor.serial_number)
        if sensor.is_supported_parameter(SensorParameter.SamplingFrequency):
            print(sensor.sampling_frequency)
        if sensor.is_supported_parameter(SensorParameter.Gain):
            print(sensor.gain)
        if sensor.is_supported_parameter(SensorParameter.Offset):
            print(sensor.data_offset)
        print(sensor.commands)
        print(sensor.parameters)

        sensor.sensorAmpModeChanged = on_amp_received

        if sensor.is_supported_feature(SensorFeature.Signal):
            sensor.signalDataReceived = on_signal_received

        if sensor.is_supported_feature(SensorFeature.Resist):
            sensor.resistDataReceived = on_resist_received

        if sensor.is_supported_feature(SensorFeature.MEMS):
            sensor.memsDataReceived = on_mems_received

        if sensor.is_supported_feature(SensorFeature.FPG):
            sensor.fpgDataReceived = on_fpg_received

        if sensor.is_supported_command(SensorCommand.StartSignal):
            sensor.exec_command(SensorCommand.StartSignal)
            print("Начало сигнала")
            sleep(5)
            sensor.exec_command(SensorCommand.StopSignal)
            print("\nСтоп сигнала\n")

        if sensor.is_supported_command(SensorCommand.StartFPG):
            sensor.exec_command(SensorCommand.StartFPG)
            print("Начало FPG")
            sleep(5)
            sensor.exec_command(SensorCommand.StopFPG)
            print("Стоп FPG")

        if sensor.is_supported_command(SensorCommand.StartResist):
            sensor.exec_command(SensorCommand.StartResist)
            print("Начало измерения сопротивления\n")
            sleep(5)
            sensor.exec_command(SensorCommand.StopResist)
            print("\nЗавершение измерения сопротивления\n")

        if sensor.is_supported_command(SensorCommand.StartMEMS):
            sensor.exec_command(SensorCommand.StartMEMS)
            print("Начало MEMS")
            sleep(5)
            sensor.exec_command(SensorCommand.StopMEMS)
            print("Завершение MEMS")

        sensor.disconnect()
        print("Датчик отключен")
        del sensor

    del scanner
    print('Сканер удален')
except Exception as err:
    print(err)
