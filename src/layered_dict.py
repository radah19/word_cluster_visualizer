import copy

class CustomKey:
    def __init__(self, value, layers):
        self.value = value

    def __hash__(self):
        # Custom hash function
        return hash(self.value[self.layers:])
        
class LayeredDict:
    def __init__(self, layers, buckets):
        self.layers = layers
        self.buckets = buckets

        ls = [{}] * buckets

        num_layers = layers
        while num_layers > 1:
            num_layers -= 1
            new_layer = []

            for i in buckets:
                new_layer.append(copy.deepcopy(ls))

            ls = new_layer

        self.ls = ls
    
    def get_entry(self, key):
        d = self.seek_dict(key)
        return d[CustomKey(key, self.layers)]

    def set_entry(self, key, val):
        d = self.seek_dict(key)
        d[CustomKey(key, self.layers)] = val
    
    def increment_entry(self, key):
        d = self.seek_dict(key)
        
        if CustomKey(key, self.layers) not in d:
            d[CustomKey(key, self.layers)] = 0
        d[CustomKey(key, self.layers)] = d[CustomKey(key, self.layers)] + 1

    def seek_dict(self, key):
        d = self.ls
        for i in self.layers:
            d = d[int(key[i])-97]
        return d

    def items(self):
        ret = []

    def rec(self, layer, ret):
        



