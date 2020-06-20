# SAGEMCOM F@st

I wanted to automate some things at my home but my current router (_Sagemcom F@st 5655v2AC_) does not have any option so I wrote my own python client.

Thanks to [@wuseman](https://github.com/wuseman) for his incredible [wiki](https://github.com/wuseman/SAGEMCOM-FAST-5370e-TELIA) about the sagecom router.

I will be adding methods as I need them, so if you need one and is not yet implemented fell free to collaborate 😉

## How to install

You can install this package using pip
`pip install git+https://github.com/MrMarble/sagemcomclient`

## Usage

```python
from sagemcom.sagemcomclient import Sagemcomclient
client = Sagemcomclient('user','pass')
client.login() # will raise an exception on login failed

custom_query = client.get_values_tree('Device/Hosts/Hosts') # returns a dict with the response from the router
```

### Available methods
   - **login**: Will let you login to the router
   - **get_values_tree**: Will let you make custom requests to the router
   - **get_hosts**: Will show connected devices