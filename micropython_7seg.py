from machine import Pin
import time

class Sevseg:
    def __init__(self,com):
        self.com=com
        self.pin_map={"anode":None,"cathode":None}
    def anode(self,*pins):
        self.pin_map["cathode"]=[i for i in pins]
    def cathode(self,*pins):
        self.pin_map["anode"]=[i for i in pins]
    def reset(self):
      if self.com=="anode":
         for pin in self.pin_map["anode"]:
           Pin(pin,Pin.OUT).value(1)
      elif self.com=="cathode":
         for pin in self.pin_map["cathode"]:
           Pin(pin,Pin.OUT).value(0)

    def _show_(self,n):
      self.reset()
      if n==1 or n==7:
        Pin(self.pin_map[self.com][1],Pin.OUT).value(0)
        Pin(self.pin_map[self.com][2],Pin.OUT).value(0)
        if n==7:Pin(self.pin_map[self.com][0],Pin.OUT).value(0)
      for i in range(7):
        if n==1 or n==7:break
        if n==0 and(self.pin_map[self.com][i]==self.pin_map[self.com][6]):continue
        if n==2 and(self.pin_map[self.com][i] in (self.pin_map[self.com][2],self.pin_map[self.com][5])):continue
        if n==3 and(self.pin_map[self.com][i] in (self.pin_map[self.com][4],self.pin_map[self.com][5])):continue
        if n==4 and(self.pin_map[self.com][i] in (self.pin_map[self.com][0],self.pin_map[self.com][3],self.pin_map[self.com][4])):continue
        if n==5 and(self.pin_map[self.com][i] in (self.pin_map[self.com][1],self.pin_map[self.com][4])):continue
        if n==6 and(self.pin_map[self.com][i]==self.pin_map[self.com][1]):continue
        if n==9 and(self.pin_map[self.com][i]==self.pin_map[self.com][4]):continue
        if self.com=="anode":Pin(self.pin_map[self.com][i],Pin.OUT).value(0)
        if self.com=="cathode":Pin(self.pin_map[self.com][i],Pin.OUT).value(1)

    def display(self,val,flicker=0.005):
      while True:
        for i in range(len(str(val))):
          self._show_(int(str(val)[-(i+1)]))
          if self.com=="anode":
            Pin(self.pin_map["cathode"][i],Pin.OUT).value(1)
            time.sleep(flicker)
            Pin(self.pin_map["cathode"][i],Pin.OUT).value(0)
          elif self.com=="cathode":
             Pin(self.pin_map["anode"][i],Pin.OUT).value(0)
             time.sleep(flicker)
             Pin(self.pin_map["anode"][i],Pin.OUT).value(1)

    def count_down(self,initial,final=0,delay=1,decrement=-1,flicker=0.005):
      while True:
        start=time.time()
        for i in range(len(str(initial))):
          self._show_(int(str(initial)[-(i+1)]))
          if self.com=="anode":
            Pin(self.pin_map["cathode"][i],Pin.OUT).value(1)
            time.sleep(flicker)
            Pin(self.pin_map["cathode"][i],Pin.OUT).value(0)
          elif self.com=="cathode":
            Pin(self.pin_map["anode"][i],Pin.OUT).value(0)
            time.sleep(flicker)
            Pin(self.pin_map["anode"][i],Pin.OUT).value(1)
        stop=time.time()
        if (stop-start)>=delay:initial+=decrement
        if abs(initial-final)<=0:break