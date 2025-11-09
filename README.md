# Scarfagnone

I'm using the amazin [pyinfra](https://pyinfra.com/)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

git clone git@github.com:alessio-perugini/scarfagnone.git
cd scarfagnone

uv venv
source .venv/bin/activate

pyinfra @local deploy.py
```
