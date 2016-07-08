import zmq
import sys

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)



context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)


def send(msg):
    with context.socket(zmq.REQ) as socket:
        socket.connect ("tcp://76.1.134.36:%s" % port)
        socket.send (msg)
        #  Get the reply.
        message = socket.recv()

    return message


