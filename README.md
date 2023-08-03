# c2a-pytest-gaia

c2a-pytest-gaia is the [Gaia(tmtc-c2a)](https://github.com/arkedge/gaia) version of python-wings-interface.

## How to use

Replace your `utils/wings_utils.py` with following code:
```
import json
from c2a_pytest_gaia import wings_compat

def get_wings_operation():
    tlmcmddb = json.load(open("../../../tlmcmddb.json"))
    return wings_compat.Operation(tlmcmddb)
```
