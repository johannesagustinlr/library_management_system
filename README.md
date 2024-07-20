# library_management_system

### Source
```bash
git clone git@github.com:johannesagustinlr/library_management_system.git
cd library_management_system
```

### Setup Environment

```shell
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Run `pytest`:

```shell
pytest```


## Usage
### Dev
```shell
fastapi dev app/main.py```

### Prod
```shell
fastapi run app/main.py```
