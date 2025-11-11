"""
Author: Girisakar365

Test harness for the M8085.Parser module.
This module loads test cases from a YAML file named 'test_cases.yml' located
in the same directory as the test module, instantiates M8085.Parser for each
test case, and prints a divider, the test case identifier, and the parser's
result for manual inspection.

Intended use:
- Place test_cases.yml next to this file.
- Run the module to execute all listed test cases and observe printed output.
"""

from pathlib import Path
import yaml

from M8085 import Parser

from M8085._utils import decode, INSTRUCTION


PATH = Path(__file__).parent / 'test_cases.yml'

with open(PATH, 'r') as file:
    test_cases = yaml.safe_load(file)

    test = test_cases['test1']
    parser = Parser(test)

    print(parser.structure)
