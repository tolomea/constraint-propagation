from src.latin_square import constraint


def test_constraint_only():
    res = constraint([{1, 2, 3, 4}, {2, 3, 4}, {2, 3, 4}, {2, 3, 4}])
    assert res == [{1}, {2, 3, 4}, {2, 3, 4}, {2, 3, 4}]


def test_constraint_basic():
    res = constraint([{1}, {1, 2, 3, 4}, {1, 2, 3, 4}, {3}])
    assert res == [{1}, {2, 4}, {2, 4}, {3}]


def test_constraint_double():
    res = constraint([{1, 2, 3, 4}, {1, 2}, {1, 2}, {1, 2, 3, 4}])
    assert res == [{3, 4}, {1, 2}, {1, 2}, {3, 4}]


def test_constraint_triple():
    res = constraint([{1, 2}, {2, 3}, {1, 3}, {1, 2, 3, 4}])
    assert res == [{1, 2}, {2, 3}, {1, 3}, {4}]


def test_constraint_overlap_up():
    res = constraint([{1, 2}, {1, 2, 3}, {3}, {1, 2, 3, 4}])
    assert res == [{1, 2}, {1, 2}, {3}, {4}]


def test_constraint_overlap_down():
    res = constraint([{1, 2}, {1, 2}, {1, 2, 3}, {1, 2, 3, 4}])
    assert res == [{1, 2}, {1, 2}, {3}, {4}]
