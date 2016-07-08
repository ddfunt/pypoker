import zmq
import time
import sys
from PIL import Image
from io import BytesIO
import pyocr


port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)


def get_image_text(image):
    tool = pyocr.get_available_tools()[0]
    langs = tool.get_available_languages()
    lang = langs[langs.index('eng')]
    txt = tool.image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    return txt

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: ")
    buff = BytesIO(message)
    image = Image.open(buff)
    print(image)
    print(get_image_text(image))
    #time.sleep (1)
    socket.send("rec".encode())