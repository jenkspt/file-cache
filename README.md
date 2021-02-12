(Pickle) File Cache
==========

Similar to [`@functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache), the `@file_cache.cache` decorator caches
the output of functions to a pickle file on disk. 

* Similar to `@functools.cache`, the order of keyword arguments matters.
* The function arguments and outputs must be pickleable.
* The cache directory can be passed as `@functools.cache('.cache/http')`. Default cache directory is `'.cache'`
* Keyword argument `cache_bust=False` is added to each function. 
Setting to `True` will force the function to be called, and will overwrite previously cached results keyed on the called function arguments
* Cache results will persist when the python kernel is stopped.


Install:
```sh
pip install git+git://github.com/jenkspt/file_cache.git
```

Examples:

```python
import logging
logging.basicConfig(level=logging.INFO)

@file_cache.cache()
def long_running_function(x, y='A', z=(1,2,3)):
	return {'name': 'bob'}

>>> long_running_function(1)	# Results are cached
INFO:root:cache bust: False
INFO:root:cache miss

>>>long_running_function(1)    # Results are loaded from disk
INFO:root:cache bust: False
INFO:root:cache hit
```

```python
import requests

>>> get = file_cache.cache('.cache/http')(requests.get)
>>> r = get('https://github.com')
>>> r = get('https://github.com')
```
