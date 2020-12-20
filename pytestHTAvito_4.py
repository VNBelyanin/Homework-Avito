import pytest
from typing import List, Tuple


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


@pytest.mark.parametrize('input_text, exp', [
    (('abc', 'cde'), [('abc', [0, 1]), ('cde', [1, 0])]),
    ('', [('', [1])]),
    (('pen', 'table', 'pen', 'pen'),
     [('pen', [0, 1]),
      ('table', [1, 0]),
      ('pen', [0, 1]),
      ('pen', [0, 1])])
])
def test_pytest(input_text, exp):
    assert fit_transform(input_text) == exp


def test_pytest_with_ex():
    exp = []
    with pytest.raises(TypeError):
        assert fit_transform() == exp
