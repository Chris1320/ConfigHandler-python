import cProfile
import os
import shutil
import sys
import time
import random
import timeit
import unittest

## The lazy way to do it...
try:
    import config_handler

except(ImportError):
    shutil.copy("./config_handler.py", "test/config_handler.py")
    import config_handler
    os.remove("test/config_handler.py")


class TestVersion1(unittest.TestCase):
    def test1_create_config(self):
        if config_handler.Version1("test/v1-testconfig.dat", False).new() != 0:
            raise Exception("File already exists")

        if config_handler.Version1("test/v1-testconfig.dat", False).add("aString1", "Hello, world!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("aString2", "Hello again!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("anInt1", 684) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("anInt2", 6844534686) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("aFloat1", 464286.5435414) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("aFloat2", 3.14) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("aBool1", True) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).add("aBool2", False) != 0: raise Exception("Failed to set variable")

    def test1_get_config_value(self):
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aString1"), "Hello, world!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aString2"), "Hello again!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("anInt1"), 684)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("anInt2"), 6844534686)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aFloat1"), 464286.5435414)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aFloat2"), 3.14)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aBool1"), True)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aBool2"), False)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("nonexistentvariable"), None)

    def test1_set_config_value(self):
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aString1"), "Hello, world!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aString2"), "Hello again!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("anInt1"), 684)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("anInt2"), 6844534686)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aFloat1"), 464286.5435414)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aFloat2"), 3.14)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aBool1"), True)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aBool2"), False)

        if config_handler.Version1("test/v1-testconfig.dat", False).set("aString1", "This is a new string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("aString2", "This is another string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("anInt1", 31854) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("anInt2", 6468435135846843) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("aFloat1", 4354351.254684354) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("aFloat2", 184.84) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("aBool1", False) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig.dat", False).set("aBool2", True) != 0: raise Exception("Failed to set variable")

        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aString1"), "This is a new string.")
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aString2"), "This is another string.")
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("anInt1"), 31854)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("anInt2"), 6468435135846843)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aFloat1"), 4354351.254684354)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aFloat2"), 184.84)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aBool1"), False)
        self.assertEqual(config_handler.Version1("test/v1-testconfig.dat", False).get("aBool2"), True)

    def test2_create_config(self):
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).new() != 0:
            raise Exception("File already exists")

        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("aString1", "Hello, world!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("aString2", "Hello again!") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("anInt1", 684) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("anInt2", 6844534686) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("aFloat1", 464286.5435414) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("aFloat2", 3.14) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("aBool1", True) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).add("aBool2", False) != 0: raise Exception("Failed to set variable")

    def test2_get_config_value(self):
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aString1"), "Hello, world!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aString2"), "Hello again!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("anInt1"), 684)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("anInt2"), 6844534686)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aFloat1"), 464286.5435414)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aFloat2"), 3.14)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aBool1"), True)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aBool2"), False)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("nonexistentvariable"), None)

    def test2_set_config_value(self):
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aString1"), "Hello, world!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aString2"), "Hello again!")
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("anInt1"), 684)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("anInt2"), 6844534686)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aFloat1"), 464286.5435414)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aFloat2"), 3.14)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aBool1"), True)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aBool2"), False)

        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("aString1", "This is a new string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("aString2", "This is another string.") != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("anInt1", 31854) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("anInt2", 6468435135846843) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("aFloat1", 4354351.254684354) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("aFloat2", 184.84) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("aBool1", False) != 0: raise Exception("Failed to set variable")
        if config_handler.Version1("test/v1-testconfig-base64.conf", True).set("aBool2", True) != 0: raise Exception("Failed to set variable")

        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aString1"), "This is a new string.")
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aString2"), "This is another string.")
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("anInt1"), 31854)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("anInt2"), 6468435135846843)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aFloat1"), 4354351.254684354)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aFloat2"), 184.84)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aBool1"), False)
        self.assertEqual(config_handler.Version1("test/v1-testconfig-base64.conf", True).get("aBool2"), True)


class TestVersion2(unittest.TestCase):
    testfile1 = "test/v2-testfile1.dat"
    testfile2 = "test/v2-testfile2.dat"
    testfile3 = "test/v2-testfile3.dat"
    testfile4 = "test/v2-testfile4.dat"
    testfile5 = "test/v2-testfile5.dat"
    testfile6 = "test/v2-testfile6.dat"
    testfile7 = "test/v2-testfile7.dat"
    testphoto1 = "test/photo1.jpg"

    testfiles = [
        testfile1,
        testfile2,
        testfile3,
        testfile4,
        testfile5,
        testfile6
    ]
    testfileinfos = {
        testfile1: {
            "name": "Test Configuration File #1",
            "author": "",
            "compression": "None",
            "encryption": "None",
            "password": None
        },
        testfile2: {
            "name": "Test Configuration File #2",
            "author": "Chris1320",
            "compression": "None",
            "encryption": "None",
            "password": None
        },
        testfile3: {
            "name": "Test Configuration File #3",
            "author": "Chris1320",
            "compression": "zlib",
            "encryption": "None",
            "password": None
        },
        testfile4: {
            "name": "Test Configuration File #4",
            "author": "Chris1320",
            "compression": "None",
            "encryption": "aes256",
            "password": "testpassword123"
        },
        testfile5: {
            "name": "Test Configuration File #5",
            "author": "Chris1320",
            "compression": "zlib",
            "encryption": "aes256",
            "password": "73$T_Password123"
        },
        testfile6: {
            "name": "Test Configuration File #6",
            "author": "Chris1320",
            "compression": "zlib",
            "encryption": "aes256",
            "password": "testP@ssword123"
        }
    }

    def test_create_config(self):
        config1 = config_handler.Version2(self.testfile1)
        config2 = config_handler.Version2(self.testfile2)
        config3 = config_handler.Version2(self.testfile3)
        config4 = config_handler.Version2(self.testfile4, self.testfileinfos[self.testfile4]["password"])
        config5 = config_handler.Version2(self.testfile5, self.testfileinfos[self.testfile5]["password"])
        config6 = config_handler.Version2(self.testfile6, self.testfileinfos[self.testfile6]["password"])

        config1.new(
            name="Test Configuration File #1"
        )

        config2.new(
            name="Test Configuration File #2",
            author="Chris1320"
        )

        config3.new(
            name="Test Configuration File #3",
            author="Chris1320",
            compression="zlib"
        )

        config4.new(
            name="Test Configuration File #4",
            author="Chris1320",
            encryption="aes256"
        )

        config5.new(
            name="Test Configuration File #5",
            author="Chris1320",
            compression="zlib",
            encryption="aes256"
        )

        config6.new(
            name="Test Configuration File #6",
            author="Chris1320",
            compression="zlib",
            encryption="aes256"
        )

    def test_info_config(self):
        for testfile in self.testfileinfos:
            testinfo = self.testfileinfos[testfile]

            if self.testfileinfos[testfile]["password"] is None:
                config = config_handler.Version2(testfile)

            else:
                config = config_handler.Version2(testfile, epass=self.testfileinfos[testfile]["password"])

            config.load()
            configinfo = config.info()

            self.assertEqual(configinfo["name"], testinfo["name"])
            self.assertEqual(configinfo["author"], testinfo["author"])

            self.assertEqual(type(configinfo["version"]), list)
            self.assertEqual(len(configinfo["version"]), 4)
            self.assertEqual(type(configinfo["version"][0]), int)
            self.assertEqual(type(configinfo["version"][1]), int)
            self.assertEqual(type(configinfo["version"][2]), int)
            self.assertEqual(type(configinfo["version"][3]), int)

            self.assertEqual(configinfo["compression"], testinfo["compression"])
            self.assertEqual(configinfo["encryption"], testinfo["encryption"])

    def test_add_config(self):
        with open(self.testphoto1, 'rb') as f:
            testphoto = f.read()

        for testfile in self.testfiles:
            if self.testfileinfos[testfile]["password"] is None:
                config = config_handler.Version2(testfile)

            else:
                config = config_handler.Version2(testfile, epass=self.testfileinfos[testfile]["password"])

            config.load()
            config.add("testVariable_str", "str", "Hello, world!")
            config.add("testVariable_int", "int", 1234)
            config.add("testVariable_float", "float", 1234.5678)
            config.add("testVariable_bool", "bool", True)
            config.add("testVariable_arr1", "arr", ("Test1", "Test2"), "str")
            config.add("testVariable_arr2", "arr", (453, 784, 5468, 12, 3), "int")
            config.add("testVariable_arr3", "arr", (3.14, 5.48), "float")
            config.add("testVariable_arr4", "arr", (True, False, False, True), "bool")
            config.add("testVariable_arr5", "arr", (b'Test String', testphoto, b"Another string", b'one last'), "bin")
            config.add("testVariable_bin", "bin", testphoto)
            config.save()

    def test_get_config(self):
        with open(self.testphoto1, 'rb') as f:
            testphoto = f.read()

        for testfile in self.testfiles:
            if self.testfileinfos[testfile]["password"] is None:
                config = config_handler.Version2(testfile)

            else:
                config = config_handler.Version2(testfile, epass=self.testfileinfos[testfile]["password"])

            config.load()
            self.assertEqual(config.get("testVariable_str"), "Hello, world!")
            self.assertEqual(config.get("testVariable_int"), 1234)
            self.assertEqual(config.get("testVariable_float"), 1234.5678)
            self.assertEqual(config.get("testVariable_bool"), True)
            self.assertEqual(config.get("testVariable_arr1")[0], "Test1")
            self.assertEqual(config.get("testVariable_arr1")[1], "Test2")
            self.assertEqual(config.get("testVariable_arr2")[0], 453)
            self.assertEqual(config.get("testVariable_arr2")[1], 784)
            self.assertEqual(config.get("testVariable_arr2")[2], 5468)
            self.assertEqual(config.get("testVariable_arr2")[3], 12)
            self.assertEqual(config.get("testVariable_arr2")[4], 3)
            self.assertEqual(config.get("testVariable_arr3")[0], 3.14)
            self.assertEqual(config.get("testVariable_arr3")[1], 5.48)
            self.assertEqual(config.get("testVariable_arr4")[0], True)
            self.assertEqual(config.get("testVariable_arr4")[1], False)
            self.assertEqual(config.get("testVariable_arr4")[2], False)
            self.assertEqual(config.get("testVariable_arr4")[3], True)
            self.assertEqual(config.get("testVariable_arr5")[0], b'Test String')
            self.assertEqual(config.get("testVariable_arr5")[1], testphoto)
            self.assertEqual(config.get("testVariable_arr5")[2], b"Another string")
            self.assertEqual(config.get("testVariable_arr5")[3], b'one last')
            self.assertEqual(config.get("testVariable_bin"), testphoto)

    def test_load_config(self):
        for testfile in self.testfiles:
            if self.testfileinfos[testfile]["password"] is None:
                config = config_handler.Version2(testfile)

            else:
                config = config_handler.Version2(testfile, epass=self.testfileinfos[testfile]["password"])

            config.load(False)

            self.assertFalse(config.info()["loaded_dictionary"])

    def test_update_config(self):
        with open(self.testphoto1, 'rb') as f:
            testphoto = f.read()

        tests = {
            "str": ("New test", "Updated test", "Version2Test"),
            "int": (953, 85, 173, 106, 96, 1080),
            "float": (97.1, 85.77, 9563.457, 8.3333332),
            "bool": (False, True),
            "arr": {
                "str": ("arraytest", "Array string test", "arrtest123"),
                "int": (864, 32486, 867, 5, 0, 687, 38, 48),
                "float": (354.54, 657.3, 53.578, 354.588, 699.32),
                "bool": (True, False),
                "bin": (testphoto, b'updated test', b"ver2arrbintest"),
            },
            "bin": (testphoto, b"updated bin datatype test", b'testbindatatype')
        }
        test_keys = list(tests.keys())
        testvars = (
            "testVariable_str",
            "testVariable_int",
            "testVariable_float",
            "testVariable_bool",
            "testVariable_arr1",
            "testVariable_arr2",
            "testVariable_arr3",
            "testVariable_arr4",
            "testVariable_arr5",
            "testVariable_bin",
        )
        for testfile in self.testfiles:
            if self.testfileinfos[testfile]["password"] is None:
                config = config_handler.Version2(testfile)

            else:
                config = config_handler.Version2(testfile, epass=self.testfileinfos[testfile]["password"])

            config.load()

            for testvar in testvars:
                datatype = type(config.get(testvar))
                if datatype == str:
                    datatype = "str"

                elif datatype == int:
                    datatype = "int"

                elif datatype == float:
                    datatype = "float"

                elif datatype == bool:
                    datatype = "bool"

                elif datatype in (list, tuple):
                    datatype = "arr"
                    arrdatatype = type(config.get(testvar)[0])
                    if arrdatatype == str:
                        arrdatatype = "str"

                    elif arrdatatype == int:
                        arrdatatype = "int"

                    elif arrdatatype == float:
                        arrdatatype = "float"

                    elif arrdatatype == bool:
                        arrdatatype = "bool"

                    elif arrdatatype == bytes:
                        arrdatatype = "bin"

                    else:
                        AssertionError("Unknown array datatype encountered")

                elif datatype == bytes:
                    datatype = "bin"

                else:
                    AssertionError("Unknown datatype encountered")

                oldvalue = config.get(testvar)
                random_object_type = datatype
                while random_object_type == datatype or random_object_type == "arr":
                    random_object_type = test_keys[random.randint(0, (len(list(tests.keys())) - 1))]

                random_object = tests[random_object_type][random.randint(0, (len(tests[random_object_type]) - 1))]

                if datatype == "arr":
                    # update() must raise a TypeError because this will not
                    # pass a tuple/list object to it.
                    try:
                        config.update(testvar, random_object)

                    except(TypeError):
                        pass

                    else:
                        raise AssertionError("Type checking failed")

                else:
                    # update() must raise a ValueError because this
                    # will pass an object with a different datatype
                    try:
                        config.update(testvar, random_object)

                    except(ValueError):
                        pass

                    else:
                        raise AssertionError("Type checking failed")

                if datatype == "arr":
                    # Test arrays
                    used_object_types = [datatype, "arr"]
                    while random_object_type in used_object_types:
                        random_object_type = test_keys[random.randint(0, (len(list(tests.keys())) - 1))]

                    used_object_types.append(random_object_type)

                    try:
                        randomobject = tests["arr"][random_object_type]
                        # Test updating an array with an object that has a different data type.
                        config.update(testvar, randomobject)

                    except(TypeError):
                        pass

                    else:
                        raise AssertionError("Type checking failed")

                    # config.update(testvar, tests["arr"][arrdatatype][random.randint(0, (len(tests["arr"][arrdatatype]) - 1))])

                else:
                    newvalue = tests[datatype][random.randint(0, (len(tests[datatype]) - 1))]
                    config.update(testvar, newvalue)
                    self.assertEqual(config.get(testvar), newvalue)

    def test_import_and_export_config(self):
        if self.testfileinfos[self.testfile6]["password"] is None:
                config = config_handler.Version2(self.testfile6)

        else:
            config = config_handler.Version2(self.testfile6, epass=self.testfileinfos[self.testfile6]["password"])

        config.load()

        exported_data = config.export_config()

        newconfig = config_handler.Version2(self.testfile7)
        newconfig.new(
            "Test Configuration File #7 (Data Imported from #6)",
            "Somebody",
            "zlib",
            "None"
        )
        newconfig.import_dict(exported_data["dictionary"])
        newconfig.save()

        self.assertEqual(newconfig.info()["name"], "Test Configuration File #7 (Data Imported from #6)")
        self.assertEqual(newconfig.info()["author"], "Somebody")

        self.assertEqual(type(newconfig.info()["version"]), list)
        self.assertEqual(len(newconfig.info()["version"]), 4)
        self.assertEqual(type(newconfig.info()["version"][0]), int)
        self.assertEqual(type(newconfig.info()["version"][1]), int)
        self.assertEqual(type(newconfig.info()["version"][2]), int)
        self.assertEqual(type(newconfig.info()["version"][3]), int)

        self.assertEqual(newconfig.info()["compression"], "zlib")
        self.assertEqual(newconfig.info()["encryption"], "None")

        testvars = (
            "testVariable_str",
            "testVariable_int",
            "testVariable_float",
            "testVariable_bool",
            "testVariable_arr1",
            "testVariable_arr2",
            "testVariable_arr3",
            "testVariable_arr4",
            "testVariable_arr5",
            "testVariable_bin",
        )
        for key in testvars:
            self.assertEqual(config.get(key), newconfig.get(key))

    def test_remove_variables(self):
        testvars = (
            "testVariable_str",
            "testVariable_int",
            "testVariable_float",
            "testVariable_bool",
            "testVariable_arr1",
            "testVariable_arr2",
            "testVariable_arr3",
            "testVariable_arr4",
            "testVariable_arr5",
            "testVariable_bin",
        )
        for path in self.testfiles:
            if self.testfileinfos[path]["password"] is None:
                    config = config_handler.Version2(path)

            else:
                config = config_handler.Version2(path, epass=self.testfileinfos[path]["password"])

            config.load()
            for var in testvars:
                config.get(var)
                config.remove(var)
                try:
                    config.get(var)

                except(KeyError):
                    pass

                else:
                    raise AssertionError("Failed to remove <var> from the configuration file")

def run():
    print("[i] Starting test suite...")
    print("Current Working Directory: `{0}`".format(os.getcwd()))

    suite = unittest.TestSuite()

    # Version 1 test cases
    suite.addTest(TestVersion1("test1_create_config"))
    suite.addTest(TestVersion1("test1_get_config_value"))
    suite.addTest(TestVersion1("test1_set_config_value"))

    suite.addTest(TestVersion1("test2_create_config"))
    suite.addTest(TestVersion1("test2_get_config_value"))
    suite.addTest(TestVersion1("test2_set_config_value"))

    # Version 2 test cases
    suite.addTest(TestVersion2("test_create_config"))
    suite.addTest(TestVersion2("test_info_config"))
    suite.addTest(TestVersion2("test_add_config"))
    suite.addTest(TestVersion2("test_get_config"))
    suite.addTest(TestVersion2("test_load_config"))
    suite.addTest(TestVersion2("test_update_config"))
    suite.addTest(TestVersion2("test_import_and_export_config"))
    suite.addTest(TestVersion2("test_remove_variables"))

    runner = unittest.TextTestRunner(verbosity=2, failfast=True)
    runner.run(suite)

    print("[i] Cleaning up...")
    files2remove = [
        "v1-testconfig.dat",
        "v1-testconfig-base64.conf",
        "v2-testfile1.dat",
        "v2-testfile2.dat",
        "v2-testfile3.dat",
        "v2-testfile4.dat",
        "v2-testfile5.dat",
        "v2-testfile6.dat",
        "v2-testfile7.dat"
    ]
    for file in files2remove:
        print("[+] Deleting `test/{0}`...".format(file))
        try:
            os.remove("test/{}".format(file))

        except FileNotFoundError:
            pass

    print("[i] Finished!")

if __name__ == "__main__":
    run()
