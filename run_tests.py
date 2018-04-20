#!/usr/bin/env python
import unittest
import aiida_zeopp.tests as zt

loader = unittest.TestLoader()
tests = loader.discover('.')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
zt.fixture_manager.destroy_all()
