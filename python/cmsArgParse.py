import argparse
import sys as _sys

def cmsArgParse(base=argparse.ArgumentParser, **kwargs):
    # makes a derived class for the given base class; this allows starting from a user's derived ArgumentParser class with custom behavior
    class cmsArgumentParser(base):
        # get only args that come after the name of the configuration script (following VarParsing convention)
        def _fix_args(self, args):
                config_index = next((index for index, arg in enumerate(args) if arg.endswith('.py')), -1)
                if config_index==-1:
                    raise RuntimeError("No configuration file found ending in .py")
                # optionally remove '--' separator (needed for cmsRun)
                if len(args)>config_index and args[config_index+1]=='--':
                    config_index += 1
                args = args[config_index+1:]
                return args
        # arg default handling taken from argparse
        def _handle_args(self, args=None):
            if args is None:
                # args default to the system args, but including arg 0 (which may be the config name)
                args = _sys.argv[:]
                # check for config by default for command-line input only
                args = self._fix_args(args)
            else:
                # make sure that args are mutable
                args = list(args)
            return args
        def parse_args(self, args=None, namespace=None):
            args = self._handle_args(args)
            return super(cmsArgumentParser,self).parse_args(args=args, namespace=namespace)
        def parse_known_args(self, args=None, namespace=None):
            args = self._handle_args(args)
            return super(cmsArgumentParser,self).parse_known_args(args=args, namespace=namespace)
    return cmsArgumentParser(**kwargs)

if __name__=="__main__":
    import unittest
    from copy import deepcopy

    class TestModuleCommand(unittest.TestCase):
        def setUp(self):
            """Nothing to do """
            None
        def testDefault(self):
            orig_argv = deepcopy(_sys.argv)
            _sys.argv = ['cmsRun','--strict','config.py','-t']
            parser = cmsArgParse()
            parser.add_argument("-t","--test",default=False,action="store_true",help="test arg")
            args = parser.parse_args()
            expected = argparse.Namespace(test = True)
            self.assertEqual(args,expected)
        def testSep(self):
            orig_argv = deepcopy(_sys.argv)
            _sys.argv = ['cmsRun','--strict','config.py','--','-t']
            parser = cmsArgParse()
            parser.add_argument("-t","--test",default=False,action="store_true",help="test arg")
            args = parser.parse_args()
            expected = argparse.Namespace(test = True)
            self.assertEqual(args,expected)
        def testNoConfig(self):
            orig_argv = deepcopy(_sys.argv)
            _sys.argv = ['cmsRun','--strict','config','-t']
            parser = cmsArgParse()
            parser.add_argument("-t","--test",default=False,action="store_true",help="test arg")
            self.assertRaises(RuntimeError,parser.parse_args)

    unittest.main()
