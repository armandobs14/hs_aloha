from functools import reduce
import operator


def flatten(nested_list):
    if len(nested_list) > 0:
        return reduce(operator.concat, nested_list)
    return nested_list
