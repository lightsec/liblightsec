'''
Created on 26/08/2014

@author: Aitor Gomez Goiri
'''

import unittest
from lightsec.helpers import BaseStationHelper, SensorHelper
from lightsec.tools.key_derivation import KeyDerivationFunctionFactory, Nist800
from lightsec.tools.encryption import AESCTRCipher
from Crypto.Hash.SHA256 import SHA256Hash


class HelpersTest(unittest.TestCase):
    
    def setUp(self):
        self.kdf_factory = KeyDerivationFunctionFactory( Nist800, SHA256Hash(), 256 ) # 512 ) 
        self.base_station = BaseStationHelper( self.kdf_factory )
        self.base_station.install_secret("sensor1", "authms1", "encms1")
    
    def test_encryption(self):
        stuff = self.base_station.create_keys( "user1", "sensor1", 10 )
        self.sensor = SensorHelper( self.kdf_factory,
                                    AESCTRCipher, "authms1", "encms1" )
        ctr = 0 # TODO check what to do with this
        kenc, kauth = self.sensor.create_keys( "user1", stuff["a"], stuff["init_time"], stuff["exp_time"], ctr )
        self.assertSequenceEqual( kenc, stuff["kenc"] )
        self.assertSequenceEqual( kauth, stuff["kauth"] )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()