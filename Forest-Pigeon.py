import serial
import time
from struct import *
from sys import byteorder
def bytes_to_str(b):
	return b.decode("utf-8");
	
class Pigeon:
	def __init__(self,serPort,baudrate=9600):
		try:
			self.serial=serial.Serial(serPort,baudrate);
		except:
			self.serial=None;
		#self.little_endian1=(byteorder=="little");
		self.little_endian1=True;
		self.little_endian2=True;
		"""
			assume both devices are L-endian
		"""
		
	@staticmethod
	def connect_serial(serPort,baudrate=9600):
		return Pigeon(serPort,baudrate);
	@staticmethod
	def to_byte(a):
		if isinstance(a,str):
			a=bytes(last,'utf-8')[0]
		elif isinstance(a,int):
			a=bytes([a])
		return a
	
	def is_valid(self):
		return self.serial!=None;
	def is_invalid(self):
		return self.serial==None;
	def in_waiting(self):#how much bytes are waiting to be read
		try:
			return self.serial.in_waiting()
		except:
			return self.serial.inWaiting()
			
	def read(self,size=1):
		return self.serial.read(size)
	def readAll(self):
		return self.read(self.in_waiting())
	def read_until(self,last=b'\n'):#kept reading until match last character
		r=b""
		last=Pigeon.to_byte(last);
		while True:
			x=self.read(1)
			r+=x
			if x==last:
				break;
		return r
	def read_inMarker(self,start,end):
		start=Pigeon.to_byte(start)
		end=Pigeon.to_byte(end)
		r=b""
		x=0
		while True:
			x=self.read()
			if x==start:
				break
		r+=x
		while True:
			x=self.read()
			r+=x
			if x==end:
				break;
		return r
	
	def read_int(self):
		return unpack("<l",self.read(4))
	def send_int(self,send):
		self.send_bytes(pack("<l",send))

	def read_float(self):
		return unpack("<f",self.read(4))
	def send_float(self,send):
		self.send_bytes(pack("<f",send))
		
	def read_double(self):
		return unpack("<d",self.read(8))
	def send_double(self,send):
		self.send_bytes(pack("<d",send))
		
	def send_str(self,sendStr):
		self.serial.write(bytes(sendStr, 'utf-8'))
	def send_bytes(self,sendBytes):
		self.serial.write(sendBytes)
		
	def read_struct(self,format):
		"""
		[a,b,c,...]=ser.read_struct(
			"LBh..."
		)
		"""
		format="<"+format
		return unpack(format,self.read(calcsize(format)))
	def send_struct(self,*args):
		"""
		ser.send_struct(
			("L",123),--->send 123 in 4bytes
			("B",23),---->send 23 in  1byte
			...
		)
		#format character follow the struct module
		"""
		format="<";
		vs=[]
		for i in args:
			format+=i[0]
			vs.append(i[1])
		bytes_return=pack(format,*vs)
		self.send_bytes(bytes_return)
		return bytes_return
		