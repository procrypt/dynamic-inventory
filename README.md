# dynamic-inventory
This script is used fill in the variables on in host_vars or group_vars file.
`variables.txt` file contains the variables value.
`OSE.yml` file has the variables defined in `jinja2` format.

#### Test

```
cd jinja
python jinja.py
```
This will create a new `data.yml` just to check that variables have been filled with proper values using `variables.txt` file.
