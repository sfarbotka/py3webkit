from webkitpy.common.checkout.diff_test_data import DIFF_TEST_DATA
            parser = diff_parser.DiffParser(DIFF_TEST_DATA.splitlines())
            patch = p.sub(lambda x: " %s/" % prefix[x.group(1)], DIFF_TEST_DATA)