"""
This is also a block comment
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
from src.accum import Accumulator


# --------------------------------------------------------------------------------
# Test Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def accum():
  return Accumulator()


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Verifies the new instance of the Accumulator class has a starting count of zero
# --------------------------------------------------------------------------------

def test_accumulator_init(accum):
  assert accum.count == 0


# --------------------------------------------------------------------------------
#  verifies the add() method adds one to the internal count when it is called
#  with no other arguments
# --------------------------------------------------------------------------------

def test_accumulator_add_one(accum):
  accum.add()
  assert accum.count == 1


# --------------------------------------------------------------------------------
#  verifies the add() method adds 3 to the count when it is called with the
#  argument of 3
# --------------------------------------------------------------------------------

def test_accumulator_add_three(accum):
  accum.add(3)
  assert accum.count == 3


# --------------------------------------------------------------------------------
# verifies that the count increases appropriately with multiple add() calls.
# --------------------------------------------------------------------------------

def test_accumulator_add_twice(accum):
  accum.add()
  accum.add()
  assert accum.count == 2


# --------------------------------------------------------------------------------
# verifies that the count attribute cannot be assigned directly because it is a
# read-only property. Uses pytest.raises to verify the AttributeError
# --------------------------------------------------------------------------------

def test_accumulator_cannot_set_count_directly(accum):
  with pytest.raises(AttributeError, match=r"property 'count' of 'Accumulator' object has no setter") as e:
    accum.count = 10