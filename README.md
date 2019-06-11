# conjur-python-2-client

## Installing the code

### From source
```bash
$ git clone https://github.com/AndrewCopeland/conjur-python-2-client.git
$ cd conjur-python-2-client; pip install . --user
```

## Usage

#### Setting conjur auth files

Setting these files is optional however it may be easier for your use case to create these files.

~/.conjurrc
```
---
account: myorg
plugins: []
appliance_url: https://conjur.myorg.com
cert_file: "/path/to/certificate/conjur.pem"
```

~/.netrc
```
machine https://conjur.myorg.com/authn
  login conjurUsername
  password conjurApiKey
```

#### authenticate w/ auth files

This method will raise a ConjurApiError exception if it could not authenticate

```python
>>> from conjur.client import Client
>>> client = Client()
>>> client.authenticate()
```

#### authenticate w/ inline arguments

This method will raise a ConjurApiError exception if it could not authenticate

```python
>>> from conjur.client import Client
>>> client = Client("https://conjur.myorg.com", "/path/to/certificate/conjur.pem", "myorg", "conjurUsername", "conjurApiKey")
>>> client.authenticate()
```


#### retrieve_secret

This method will retrieve a specific variable for the conjur api and will return as a unicode string. If a 401 status code is returned it will attempt to re-authenticate once. If this re-authentication fails then a ConjurApiError exception will be raised.

```python
>>> from conjur.client import Client
>>> client = Client()
>>> client.retrieve_secret("secrets/db/username")
```

#### list_resources

This method will return a list of all of the resources and all of the information associated with the resource. A list is returned containing a dictionary of each resource. Like the retrieve_secret() method, if a 401 is returned it will attempt to re-authenticate once. If you are just looking for the resource ids use the list_resources_simple() method.

```python
>>> from conjur.client import Client
>>> client = Client()
>>> client.list_resources()
```

#### list_resources_simple

This method will return a list of all of the resource ids. A list with all of the resource ids are returned, if a 401 is returned it will attempt to re-authenticate once. If you are looking for more verbose information regarding the resource see the list_resources() method.

```python
>>> from conjur.client import Client
>>> client = Client()
>>> client.list_resources_simple()
```
