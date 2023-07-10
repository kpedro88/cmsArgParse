import argparse
import sys as _sys

def cmsArgParse(base=argparse.ArgumentParser, **kwargs):
    # makes a derived class for the given base class; this allows starting from a user's derived ArgumentParser class with custom behavior
    class cmsArgumentParser(base):
        # get only args that come after separator
        def _fix_args(self, args, sep='--'):
                try:
                    sep_index = args.index(sep)
                except ValueError:
                    raise ValueError("Arguments must come after {} separator".format(sep)) from None
                args = args[sep_index+1:]
                return args
        # arg default handling taken from argparse
        def _handle_args(self, args=None):
            if args is None:
                # args default to the system args
                args = _sys.argv[1:]
                # check for separator by default only for command-line input
                # and only for cms executables
                if _sys.argv[0].startswith("cms") or _sys.argv[0].startswith("edm"):
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
            _sys.argv = ['cmsRun','--strict','config.py','--','-t']
            parser = cmsArgParse()
            parser.add_argument("-t","--test",default=False,action="store_true",help="test arg")
            args = parser.parse_args()
            expected = argparse.Namespace(test = True)
            self.assertEqual(args,expected)
        def testNoSep(self):
            orig_argv = deepcopy(_sys.argv)
            _sys.argv = ['cmsRun','--strict','config.py','-t']
            parser = cmsArgParse()
            parser.add_argument("-t","--test",default=False,action="store_true",help="test arg")
            self.assertRaises(ValueError,parser.parse_args)

    unittest.main()
