from pathlib import Path
import functools
import pickle
import hashlib
import logging


def make_key(function, args, kwargs, typed=False):
    key = args + tuple(kwargs.values())
    if typed:
        key = zip(key, map(type, key))
    return (function.__module__, function.__name__) + tuple(key)


def hash_key(key):
    """ Create stable hash from pickle bytes """
    key_bytes = pickle.dumps(key)
    key_hash = hashlib.sha1(key_bytes).hexdigest()
    return key_hash

def write_cache_file(path, key, data):
    with open(path, 'wb') as f:
        pickle.dump((key, data), f)

def read_cache_file(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def cache(path: str='.cache', typed: bool =False):
    """
    Creates a persistent local file cache, keyed on the 
    function and function arguments.

    Args:
        path: Directory path to store the cache
        typed: If true, cache on argument types
    """
    path = Path(path)
    path.mkdir(exist_ok=True, parents=True)

    def decorating_function(user_function):

        @functools.wraps(user_function)
        def wrapper(*args, **kwargs):
            cache_bust = kwargs.pop('cache_bust', False)
            logging.info(f'cache bust: {cache_bust}')
            # Create the identifier from the function and arguments
            key = make_key(user_function, args, kwargs, typed)
            # Create a stable hash of the key
            hashed_key = hash_key(key)
            
            cache_file = None 
            for cache_file in path.glob(f'{hashed_key}_*.pkl'):
                saved_key, data = read_cache_file(cache_file)
                # Check for hash collisions
                if key == saved_key:
                    logging.info('cache hit')
                    if cache_bust:
                        data = user_function(*args, **kwargs)
                        write_cache_file(cache_file, key, data)
                    return data
            logging.info('cache miss')
            # Collisions will increment the file suffix
            n = int(cache_file.stem.split('_')[-1]) + 1 if cache_file else 0
            data = user_function(*args, **kwargs)
            write_cache_file(path / f'{hashed_key}_{n}.pkl', key, data)
            return data

        return wrapper

    return decorating_function


if __name__ == "__main__":

    @cache('cache')
    def get_json(a):
        return {'name': 'penn'}
    
    print(get_json(5))
