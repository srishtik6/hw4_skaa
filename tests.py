"""
all tests
"""
import pytest
import hw4 as h
import pandas as pd
import numpy as np

@pytest.fixture
def cases():
    t1 = np.array(pd.read_csv('test1.csv', header=None))
    t2 = np.array(pd.read_csv('test2.csv', header=None))
    t3 = np.array(pd.read_csv('test3.csv', header=None))

    return t1, t2, t3

def test_overallocation(cases):
    """testing overallocation function, all tests should pass"""
    test1, test2, test3 = cases
    assert h.overallocation(test1) == 37
    assert h.overallocation(test2) == 41
    assert h.overallocation(test3) == 23

def test_conflicts(cases):
    """testing conflicts function, all tests should pass"""
    test1, test2, test3 = cases
    assert h.conflicts(test1) == 8
    assert h.conflicts(test2) == 5
    assert h.conflicts(test3) == 2

def test_undersupport(cases):
    """testing undersupport function, all tests should pass"""
    test1, test2, test3 = cases
    assert h.undersupport(test1) == 1
    assert h.undersupport(test2) == 0
    assert h.undersupport(test3) == 7

def test_unwilling(cases):
    """testing unwilling function, all tests should pass"""
    test1, test2, test3 = cases
    assert h.unwilling(test1) == 53
    assert h.unwilling(test2) == 58
    assert h.unwilling(test3) == 43

def test_unpreffered(cases):
    """testing unpreferred function, all tests should pass"""
    test1, test2, test3 = cases
    assert h.unpreferred(test1) == 15
    assert h.unpreferred(test2) == 19
    assert h.unpreferred(test3) == 10

