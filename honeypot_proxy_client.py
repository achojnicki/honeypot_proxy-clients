import socketio
from threading import Thread
from uuid import uuid4
from time import sleep
from pprint import pprint


class honeypot_proxy_client:
	def __init__(self):
		self._url='https://netheroes.co.uk/socket.io/'

		self._socketio=socketio.Client()
		self._socketio.on('response', namespace='/', handler=self._response)

		self._requests={}

		self.start()

	def _connect(self):
		self._socketio.connect(self._url)

		self._socketio.emit('client_connect')


	def _response(self, message):
		self._requests[message['request_uuid']]=message

	def _build_message(self, request_url, request_uuid):
		return {"request_url": request_url, "request_uuid":str(request_uuid)}


	def _send_request(self, request_url, request_uuid):
		print("Request UUID:",request_uuid)
		print('Request URL:',request_url)

		self._socketio.emit(
			'client_request',
			self._build_message(
				request_uuid=request_uuid,
				request_url=request_url
				)
			)


	def _loop(self):
		while 1:
			request_uuid=uuid4()
			request_url=input('url: ')

			self._send_request(
				request_uuid=request_uuid,
				request_url=request_url
				)

	def _ping(self):
		while 1:
			self._socketio.emit('client_ping')
			sleep(1)

	def start(self):
		self._connect()
		t=Thread(target=self._ping)
		t.start()


	def get(self, address):
		request_uuid=str(uuid4())
		request_url=address

		self._send_request(
			request_uuid=request_uuid,
			request_url=request_url
			)
		while True:
			if request_uuid in self._requests:
				print('ok')
				data=self._requests[request_uuid]
				del self._requests[request_uuid]
				return data['content']
			sleep(0.1)
