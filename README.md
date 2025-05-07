| this project is archived
# discord-winhook
A library to simplify sending information updates from Windows systems through a Discord webhook

## Install
```bash
pip install discord-winhook
```
- you need to specify features you want to use
- currently available features [info, screenshot]

example:
```bash
pip install discord-winhook[screenshot]
```

## Usage
```py
from discord_winhook import SSHook

hook = SSHook(
    "{webhook_url}",
    "Discord"
)
# send every 5 minutes
hook.recurs(every=5*60)
```

