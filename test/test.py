import cProfile
import os
import shutil
import sys
import time
import timeit
import unittest

shutil.copy("../config_handler.py", "./config_handler.py")
import config_handler
os.remove("config_handler.py")


class TestVersion1(unittest.TestCase):
    def test_create_config(self):
        print("\n[TEST] Running test_create_config()")
        if config_handler.Version1("testconfig.dat", False).new() != 0:
            raise Exception("File already exists")

        if config_handler.Version1("testconfig-base64.conf", True).new() != 0:
            raise Exception("File already exists")

        if config_handler.Version1("testconfig.dat", False).add("aString1", "Hello, world!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("aString2", "Hello again!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("anInt1", 684) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("anInt2", 6844534686) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("aFloat1", 464286.5435414) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("aFloat2", 3.14) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("aBool1", True) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).add("aBool2", False) != 0: raise Exception("Failed to set variable")

        if config_handler.Version1("testconfig-base64.conf", True).add("aString1", "Hello, world!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("aString2", "Hello again!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("anInt1", 684) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("anInt2", 6844534686) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("aFloat1", 464286.5435414) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("aFloat2", 3.14) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("aBool1", True) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).add("aBool2", False) != 0: raise Exception("Failed to set variable")

    def test_get_config_value(self):
        print("\n[TEST] Running test_get_config_value()")
        assert config_handler.Version1("testconfig.dat", False).get("aString1") == "Hello, world!"
        assert config_handler.Version1("testconfig.dat", False).get("aString2") == "Hello again!"
        assert config_handler.Version1("testconfig.dat", False).get("anInt1") == 684
        assert config_handler.Version1("testconfig.dat", False).get("anInt2") == 6844534686
        assert config_handler.Version1("testconfig.dat", False).get("aFloat1") == 464286.5435414
        assert config_handler.Version1("testconfig.dat", False).get("aFloat2") == 3.14
        assert config_handler.Version1("testconfig.dat", False).get("aBool1") == True
        assert config_handler.Version1("testconfig.dat", False).get("aBool2") == False

        assert config_handler.Version1("testconfig-base64.conf", True).get("aString1") == "Hello, world!"
        assert config_handler.Version1("testconfig-base64.conf", True).get("aString2") == "Hello again!"
        assert config_handler.Version1("testconfig-base64.conf", True).get("anInt1") == 684
        assert config_handler.Version1("testconfig-base64.conf", True).get("anInt2") == 6844534686
        assert config_handler.Version1("testconfig-base64.conf", True).get("aFloat1") == 464286.5435414
        assert config_handler.Version1("testconfig-base64.conf", True).get("aFloat2") == 3.14
        assert config_handler.Version1("testconfig-base64.conf", True).get("aBool1") == True
        assert config_handler.Version1("testconfig-base64.conf", True).get("aBool2") == False

    def test_set_config_value(self):
        print("\n[TEST] Running test_set_config_value()")
        assert config_handler.Version1("testconfig.dat", False).get("aString1") == "Hello, world!"
        assert config_handler.Version1("testconfig.dat", False).get("aString2") == "Hello again!"
        assert config_handler.Version1("testconfig.dat", False).get("anInt1") == 684
        assert config_handler.Version1("testconfig.dat", False).get("anInt2") == 6844534686
        assert config_handler.Version1("testconfig.dat", False).get("aFloat1") == 464286.5435414
        assert config_handler.Version1("testconfig.dat", False).get("aFloat2") == 3.14
        assert config_handler.Version1("testconfig.dat", False).get("aBool1") == True
        assert config_handler.Version1("testconfig.dat", False).get("aBool2") == False

        assert config_handler.Version1("testconfig-base64.conf", True).get("aString1") == "Hello, world!"
        assert config_handler.Version1("testconfig-base64.conf", True).get("aString2") == "Hello again!"
        assert config_handler.Version1("testconfig-base64.conf", True).get("anInt1") == 684
        assert config_handler.Version1("testconfig-base64.conf", True).get("anInt2") == 6844534686
        assert config_handler.Version1("testconfig-base64.conf", True).get("aFloat1") == 464286.5435414
        assert config_handler.Version1("testconfig-base64.conf", True).get("aFloat2") == 3.14
        assert config_handler.Version1("testconfig-base64.conf", True).get("aBool1") == True
        assert config_handler.Version1("testconfig-base64.conf", True).get("aBool2") == False

        if config_handler.Version1("testconfig.dat", False).set("aString1", "This is a new string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("aString2", "This is another string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("anInt1", 31854) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("anInt2", 6468435135846843) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("aFloat1", 4354351.254684354) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("aFloat2", 184.84) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("aBool1", False) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig.dat", False).set("aBool2", True) != 0: raise Exception("Failed to set variable")

        if config_handler.Version1("testconfig-base64.conf", True).set("aString1", "This is a new string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("aString2", "This is another string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("anInt1", 31854) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("anInt2", 6468435135846843) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("aFloat1", 4354351.254684354) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("aFloat2", 184.84) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("aBool1", False) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("testconfig-base64.conf", True).set("aBool2", True) != 0: raise Exception("Failed to set variable")

        assert config_handler.Version1("testconfig.dat", False).get("aString1") == "This is a new string."
        assert config_handler.Version1("testconfig.dat", False).get("aString2") == "This is another string."
        assert config_handler.Version1("testconfig.dat", False).get("anInt1") == 31854
        assert config_handler.Version1("testconfig.dat", False).get("anInt2") == 6468435135846843
        assert config_handler.Version1("testconfig.dat", False).get("aFloat1") == 4354351.254684354
        assert config_handler.Version1("testconfig.dat", False).get("aFloat2") == 184.84
        assert config_handler.Version1("testconfig.dat", False).get("aBool1") == False
        assert config_handler.Version1("testconfig.dat", False).get("aBool2") == True

        assert config_handler.Version1("testconfig-base64.conf", True).get("aString1") == "This is a new string."
        assert config_handler.Version1("testconfig-base64.conf", True).get("aString2") == "This is another string."
        assert config_handler.Version1("testconfig-base64.conf", True).get("anInt1") == 31854
        assert config_handler.Version1("testconfig-base64.conf", True).get("anInt2") == 6468435135846843
        assert config_handler.Version1("testconfig-base64.conf", True).get("aFloat1") == 4354351.254684354
        assert config_handler.Version1("testconfig-base64.conf", True).get("aFloat2") == 184.84
        assert config_handler.Version1("testconfig-base64.conf", True).get("aBool1") == False
        assert config_handler.Version1("testconfig-base64.conf", True).get("aBool2") == True

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestVersion1("test_create_config"))
    suite.addTest(TestVersion1("test_get_config_value"))
    suite.addTest(TestVersion1("test_set_config_value"))

    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite)

    os.remove("testconfig.dat")
    os.remove("testconfig-base64.conf")
