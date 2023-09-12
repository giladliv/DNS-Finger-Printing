# def replace_whitespace(input_string, replacement=' '):
#     return replacement.join(input_string.split())
#
# # Test the function
# original_string = "This is a test\tstring\nwith multiple   spaces."
# replacement_string = replace_whitespace(original_string, '_')
#
# print("Original String:")
# print(original_string)
#
# print("\nString with Whitespace Replaced:")
# print(replacement_string)

def dict_to_tuple_list(d):
    tuple_list = []
    for key, value in d.items():
        if isinstance(value, dict):
            tuple_list.extend(dict_to_tuple_list(value))
        else:
            tuple_list.append((key, value))
    return tuple_list

# Example nested dictionary
nested_dict = {
    'id': '1',
    'info': {
        'name': 'Ninja',
        'details': {
            'code': '101',
            'location': {
                'state': 'Oklahoma',
                'city': 'Moore'
            }
        }
    }
}

tuple_list = dict_to_tuple_list(nested_dict)

for item in tuple_list:
    print(item)

a = 16 / 5
from math import ceil
print('a =', a, '\t', 'type =', type(a))
print(ceil(a))