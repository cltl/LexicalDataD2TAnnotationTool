import operator




def rank_keys(set_of_keys,
              key_to_value,
              key_to_label=None):
    """
    rank a list of keys

    if key_to_label is provided, show label instead of key

    :param set_of_keys: set of keys
    :param key_to_value: dictionary mapping keys to values

    :rtype: list
    :return: list of tuples (key, value)
    """
    ordered = []

    relevant_dict = {key: key_to_value[key]
                     for key in set_of_keys}

    for key, value in sorted(relevant_dict.items(),
                             key=operator.itemgetter(1),
                             reverse=True):

        label = value
        if key_to_label:
            label = key_to_label[key]
            label = f'{label} ({value})'

        ordered.append((key, label))

    assert len(ordered) == len(set_of_keys), f'{ordered}\n{set_of_keys}'
    return ordered

list_of_keys = ["a", "b", "c"]
key_to_value = {"a": 100, "b": 0, "c": 50}
result = rank_keys(set_of_keys=list_of_keys, key_to_value=key_to_value)
assert result == [('a', 100), ('c', 50), ('b', 0)]