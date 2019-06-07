# Bearer Python

Bearer Python client

Installation:

```
pip install bearer
```

Example usage:

```
from bearer import Bearer

bearer = Bearer('<apiKey>')

# Invoke a function that doesn't need auth details
bearer.invoke('<buid>', '<functionName>')

# Invoke a function using OAuth
bearer.invoke('<buid>', '<functionName>', params={ 'authId': '<authId>' })

# For a function using Basic/API Key auth
bearer.invoke('<buid>', '<functionName>', params={ 'setupId': '<setupId>' })

# Invoke a function with a body payload
bearer.invoke('<buid>', '<functionName>', body={ 'some': 'data' })

```
