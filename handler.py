import functools
import collections

class DataStreamHandler:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    @functools.lru_cache(maxsize=128)
    def _compute_heavy_transform(self, data_slice):
        return bytes([b ^ 0xFF for b in data_slice])

    def process_buffer(self, buffer):
        if len(buffer) > self.capacity:
            self.cache.clear()
        
        segments = [buffer[i:i+64] for i in range(0, len(buffer), 64)]
        results = []
        
        for seg in segments:
            seg_hash = hash(seg)
            if seg_hash not in self.cache:
                transformed = self._compute_heavy_transform(seg)
                self.cache[seg_hash] = transformed
                self.cache.move_to_end(seg_hash)
                if len(self.cache) > 256:
                    self.cache.popitem(last=False)
            results.append(self.cache[seg_hash])
            
        return b''.join(results)

    def flush_optimization_state(self):
        self.cache.clear()
        self._compute_heavy_transform.cache_clear()