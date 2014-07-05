#!/usr/bin/env python
# coding=utf8

# BTChip-AddrGen Bitcoin Address Generation
# Copyright (C) 2014  Antoine FERRON

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from btchip.btchip import *
from B58 import *
from ECDSA_BTC import *
from ECDSA_256k1 import *
import hashlib

class UserBTChip(btchip):
	def close(self):
		self.dongle.close()
	
	def exchange(self,intr,p1,p2,lenout,params=None):
		apdu = [ self.BTCHIP_CLA, intr, p1, p2, lenout ]
		if params!=None:
			apdu.append(len(params))
			apdu.extend(params)
		return self.dongle.exchange(bytearray(apdu))
	
	def get_random(self,ncar):
		data=self.exchange(self.BTCHIP_INS_GET_RANDOM,0,0,ncar)
		return str(data)
	
	def hashrand(self,num):
		#return sha256 of num times 256bits random data
		rng_data=''
		for idat in range(num):
			rng_data=rng_data+self.get_random(32)
		assert len(rng_data)==num*32
		return hashlib.sha256(rng_data).hexdigest()

try:
	mydongle = UserBTChip(getDongle())
except:
	print "No dongle can be accessed!"
	quit()
print "\nGenerate address from TRNG in BTchip"
privkeynum = 0
while privkeynum<1 or privkeynum>=generator_256.order():
	privkeynum = int(mydongle.hashrand(32), 16)
pubkey = Public_key( generator_256, generator_256 * privkeynum )
pubkey58 = pub_hex_base58(pubkey.point.x(),pubkey.point.y())
privkey = Private_key( pubkey, privkeynum )
print "\nAddr :  ",pubkey58
print "PrivKey:",priv_hex_base58(privkeynum)
