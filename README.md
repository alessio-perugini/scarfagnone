# Scarfagnone

I'm using the amazin [pyinfra](https://pyinfra.com/)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv venv
source .venv/bin/activate

pyinfra @local deploy.py
```
