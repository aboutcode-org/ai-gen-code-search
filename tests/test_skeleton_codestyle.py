#
# Copyright (c) AboutCode.org and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
#

import configparser
import subprocess
import unittest


class BaseTests(unittest.TestCase):
    def test_skeleton_codestyle(self):
        """
        This test shouldn't run in proliferated repositories.
        """
        setup_cfg = configparser.ConfigParser()
        setup_cfg.read("setup.cfg")
        if setup_cfg["metadata"]["name"] != "skeleton":
            return

        args = "venv/bin/black --check -l 100 setup.py etc tests"
        try:
            subprocess.check_output(args.split())
        except subprocess.CalledProcessError as e:
            print("===========================================================")
            print(e.output)
            print("===========================================================")
            raise Exception(
                "Black style check failed; please format the code using:\n"
                "  python -m black -l 100 setup.py etc tests",
                e.output,
            ) from e
