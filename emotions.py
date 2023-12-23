from neurosdk.scanner import Scanner
from em_st_artifacts.utils import lib_settings
from em_st_artifacts.utils import support_classes
from em_st_artifacts import emotional_math
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
    raw_channels = []
    for sample in data:
        left_bipolar = sample.T3-sample.O1
        right_bipolar = sample.T4-sample.O2
        raw_channels.append(support_classes.RawChannels(left_bipolar, right_bipolar))

    math.push_data(raw_channels)
    math.process_data_arr()
    if not math.calibration_finished():
        print(f'Артефакты: {math.is_both_sides_artifacted()}')
        print(f'Прогресс калибровки: {math.get_calibration_percents()}')
    else:
        print(f'Артефакты: {math.is_artifacted_sequence()}')
        print(f'Ментальные данные: {math.read_mental_data_arr()}')
        print(f'Спектральные данные: {math.read_spectral_data_percents_arr()}')

    print(data)


try:
    scanner = Scanner([SensorFamily.LEBrainBit])

    scanner.sensorsChanged = sensor_found
    scanner.start()
    print("Поиск в течение 10 сек...")
    sleep(10)
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
            print("Устройство подключено")

        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.batteryChanged = on_battery_changed

        if sensor.is_supported_feature(SensorFeature.Signal):
            sensor.signalDataReceived = on_signal_received


        # init emotions lib
        calibration_length = 8
        nwins_skip_after_artifact = 10

        mls = lib_settings.MathLibSetting(sampling_rate=250,
                             process_win_freq=25,
                             fft_window=1000,
                             n_first_sec_skipped=4,
                             bipolar_mode=True,
                             channels_number=4,
                             channel_for_analysis=3)
        ads = lib_settings.ArtifactDetectSetting(hanning_win_spectrum=True, num_wins_for_quality_avg=125)
        sads = lib_settings.ShortArtifactDetectSetting(ampl_art_extremum_border=25)
        mss = lib_settings.MentalAndSpectralSetting()

        math = emotional_math.EmotionalMath(mls, ads, sads, mss)
        math.set_calibration_length(calibration_length)
        math.set_mental_estimation_mode(True)
        math.set_skip_wins_after_artifact(nwins_skip_after_artifact)
        math.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
        math.set_spect_normalization_by_bands_width(True)

        if sensor.is_supported_command(SensorCommand.StartSignal):
            sensor.exec_command(SensorCommand.StartSignal)
            print("Начало сигнала")
            math.start_calibration()
            sleep(120)
            sensor.exec_command(SensorCommand.StopSignal)
            print("Стоп сигнала")

        sensor.disconnect()
        print("Отключение датчика")
        del sensor
        del math

    del scanner
    print('Удаление сканера')
except Exception as err:
    print(err)
