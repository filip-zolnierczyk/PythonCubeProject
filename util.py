
def mul_vector(v,s):
    return tuple(x*s for x in v)

def add_to_vector(v,s):
    return tuple(x+s for x in v)

def add_vectors(v1,v2):
    return tuple(x + y for x, y in zip(v1, v2))

def sub_vectors(v1,v2):
    return tuple(x - y for x, y in zip(v1, v2))