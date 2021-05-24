# License Key Gen
A small library for creating and validating license keys.

### Installation
```
pip install licensekeygen
```

### Get started
How to generate a key using v1

```Python
from pyactivation.licensekey import v1

# creates a key
key = v1.generate_key()

print(key)
```

How to generate a key using v2

```Python
from pyactivation.licensekey import v2

# creates a key
key = v2.generate_randomkey(1, "07/30/2025")

print(key)
```