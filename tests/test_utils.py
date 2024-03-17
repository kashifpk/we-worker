"Test cases for utils module."

from we_worker.utils import code_exec


def test_code_exec_single_lines():
    assert 10 == code_exec("10")
    assert "a" == code_exec("'a'")


sum_code = """
a = 10
b = 20
c = a+b
c
"""


def test_code_exec_multiple_lines():
    assert 30 == code_exec(sum_code)


conditions_code = """
debug = True
ret = None
if debug:
    ret = 10
else:
    ret = 20

ret
"""


def test_code_exec_conditionals():
    assert 10 == code_exec(conditions_code)


loops_code = """
x = 1
for i in range(10):
    x += i

x
"""


def test_code_exec_loops():
    assert 46 == code_exec(loops_code)
