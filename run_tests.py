import unittest

suite = unittest.TestLoader().discover(start_dir='./tests', pattern='test*.py')
unittest.TextTestRunner(verbosity=3).run(suite)
