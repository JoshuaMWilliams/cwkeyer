import time
import sys
import serial
import argparse

chars =   {'A':'.-',
           'B':'-...',
           'C':'-.-.',
           'D':'-..',
           'E':'.',
           'F':'..-.',
           'G':'--.',
           'H':'....',
           'I':'..',
           'J':'.---',
           'K':'-.-',
           'L':'.-..',
           'M':'--',
           'N':'-.',
           'O':'---',
           'P':'.--.',
           'Q':'--.-',
           'R':'.-.',
           'S':'...',
           'T':'-',
           'U':'..-',
           'V':'...-',
           'W':'.--',
           'X':'-..-',
           'Y':'-.--',
           'Z':'--..',
           '0':'-----',
           '1':'.----',
           '2':'..---',
           '3':'...--',
           '4':'....-',
           '5':'.....',
           '6':'-....',
           '7':'--...',
           '8':'---..',
           '9':'----.',
           '?':'..--..',
	   '.':'.-.-.-',
           ',':'--..--',
           '/':'-..-.'
           }

cut_nums = {
            '1':'.-',
            '9':'-.',
            '0':'-'
           }

def gap():
  time.sleep(charspace)

def wordgap():
  time.sleep(wordspace)

def dah():
  cw_key(key_open)
  cw_key(key_close)
  time.sleep(dahspeed)
  cw_key(key_open)
  time.sleep(ditspeed)

def dit():
  cw_key(key_open)
  cw_key(key_close)
  time.sleep(ditspeed)
  cw_key(key_open)
  time.sleep(ditspeed)

def word(w):
  i = 0 
  while i < len(w): 
    if w[i] == '*': 
      if w[i+1] == '+': 
        wpm+=1 
        setKeySpeed(wpm) 
        i+=2 
        continue 
      elif w[i+1] == '-': 
        setKeySpeed(wpm-1) 
        i+=2 
        continue 
    try: 
      code=chars[w[i]] 
      i+=1 
    except KeyError:
          # FIXME: Use proper logging facility here
          print('Skipping unknown character %s' % c)
          continue
    for dahdit in code:
      if dahdit == '-':
        dah()
      else:
        dit()
    gap()
  wordgap()

def paris():
  count=0
  while True:
    word("PARIS")
    count+=1
    print(count)

parser = argparse.ArgumentParser(description='CW keyer for serial interface.')
parser.add_argument('-d', '--device', dest='device', default='/dev/ttyUSB0', help='Path to serial device. (default: /dev/ttyUSB0)')
parser.add_argument('-w', '--wpm', dest='wpm', type=int, default=20, help='CW keying speed in words per minutes. (default: 20 wpm)')
parser.add_argument('-t', '--text', dest='text', required=True, help='Text to transmit. Surround multiple words by quotes.')
parser.add_argument('--dtr', dest='dtr', action='store_true', help='Use DTR pin instead of RTS pin for keying.')
parser.add_argument('--invert', dest='invert', action='store_true', help='Invert logic signals on pin used for keying.')
parser.add_argument('--cut-nums',dest='cutnums',action='store_true',help='Use contest-style abbreviated numbers.')
args = parser.parse_args()

ser = serial.Serial(args.device, 9600)
if args.dtr:
  cw_key = ser.setDTR
else:
  cw_key = ser.setRTS

if args.invert:
  key_close = False
  key_open = True
else:
  key_close = True
  key_open = False

if args.cutnums:
  chars.update(cut_nums)

ditspeed = (1200.0 / float(wpm)) / 1000.0
dahspeed = ditspeed * 3
charspace = ditspeed * 1
wordspace = ditspeed * 7

def setKeySpeed(wpm):
  ditspeed = (1200.0 / float(wpm)) / 1000.0
  dahspeed = ditspeed * 3
  charspace = ditspeed * 1
  wordspace = ditspeed * 7

wpm = args.wpm
setKeySpeed(wpm)

for w in args.text.upper().split():
   word(w)
