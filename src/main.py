from proto.message_pb2 import *
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
from serial_util import SerialUsb

usb = SerialUsb()
usb.serConf()

HIVEMIND_ID = 0
REMOTE_ID = 42


def send_message(message):
    message_bytes = _VarintBytes(message.ByteSize()) + message.SerializeToString()
    usb.write(message_bytes)


def read_message():
    data = usb.read(4)
    msg_len, new_pos = _DecodeVarint32(data, 0)
    nb_to_read = msg_len - (4 - new_pos)
    data = data[new_pos:] + usb.read(nb_to_read)
    receivedMessage = Message()
    receivedMessage.ParseFromString(data)
    return receivedMessage


def construct_calib_message():
    calib = CalibrationMessage()

    interloc = InterlocAPI()
    interloc.calibration.CopyFrom(calib)

    message = Message()
    message.source_id = REMOTE_ID
    message.destination_id = HIVEMIND_ID
    message.interloc.CopyFrom(interloc)

    return message


def set_calib_distance():
    distance = float(input("Calibration distance (in meters): "))
    setDistance = SetCalibrationDistance()
    setDistance.distance = distance

    message = construct_calib_message()
    message.interloc.calibration.setDistance.CopyFrom(setDistance)
    send_message(message)


def start_calib():
    print("Please choose a calibration mode:")
    print("1. Initiator")
    print("2. Responder")
    mode = int(input(">"))
    start_calib = StartCalibration()

    if mode == 1:
        start_calib.mode = INITIATOR
    elif mode == 2:
        start_calib.mode = RESPONDER
    else:
        exit()

    message = construct_calib_message()
    message.interloc.calibration.startCalib.CopyFrom(start_calib)
    send_message(message)

    if start_calib.mode == RESPONDER:
        read_message()  # TODO: Check if correct message
        print("Calibration finished")


def stop_calib():
    stop_calib = StopCalibration()
    message = construct_calib_message()
    message.interloc.calibration.stopCalib.CopyFrom(stop_calib)
    send_message(message)


def execute_choice(choice):
    if choice == 1:
        set_calib_distance()
    elif choice == 2:
        start_calib()
    elif choice == 3:
        stop_calib()


# Greet
greet = Greeting()
greet.id = HIVEMIND_ID

greet_msg = Message()
greet_msg.source_id = 0
greet_msg.destination_id = 42
greet_msg.greeting.CopyFrom(greet)

print("Attempting to greet with HiveMind")
send_message(greet_msg)
receivedMessage = read_message()

if receivedMessage.HasField("greeting"):
    HIVEMIND_ID = receivedMessage.greeting.id
    print(f'Greet successful. HM ID: {HIVEMIND_ID}')


choice = -1
while choice != 0:
    print("")
    print("Please choose an action to perform:")
    print("0. Quit")
    print("1. Set calibration distance")
    print("2. Start calibration")
    print("3. End calibration")
    choice = int(input("> "))
    execute_choice(choice)
