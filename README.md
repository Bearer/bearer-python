# Bearer Python

Bearer Python client

## Installation

```
pip install bearer
```

## Usage

Get your Bearer [Secret Key](https://app.bearer.sh/keys) and integration id from
the [Dashboard](https://app.bearer.sh) and use the Bearer client as follows:

### Calling any APIs

```python
from bearer import Bearer

bearer = Bearer('BEARER_SECRET_KEY') # find it on https://app.bearer.sh/keys
github = (
    bearer
      .integration('your integration id') # you'll find it on the Bearer dashboard https://app.bearer.sh
      .auth('your auth id') # Create an auth id for your integration via the dashboard
)

print(github.get('/repositories').json())
```

We use [requests](https://2.python-requests.org/en/master/) internally and we
return the response from this library from the request methods (`request`,
`get`, `head`, `post`, `put`, `patch`, `delete`).

More advanced examples:

```python
# With query parameters
print(github.get('/repositories', query={ 'since': 364 }).json())

# With body data
print(github.post('/user/repos', body={ 'name': 'Just setting up my Bearer.sh' }).json())
```

### Setting the request timeout

By default bearer client times out after 5 seconds. Bearer allows to increase the timeout to up to 30 seconds

```python
from bearer import Bearer

bearer = Bearer('BEARER_SECRET_KEY', timeout=10) # increase the request timeout to 10 seconds
github = bearer.integration('your integration id')

print(github.invoke('your function name'))
```
## Development

``` bash
# setup venv
$ python -m venv venv

# install dependencies
$ venv/bin/python setup.py develop

# start the console
$ venv/bin/python
```
