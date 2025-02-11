from discord_webhook import DiscordEmbed
import platform
from discord_winhook.base import BaseHook
from datetime import datetime

class OSInfoHook(BaseHook):
    def construct_embed(self):
        embed = DiscordEmbed(title="OS Info", color="03b2f8")

        status = {
            "os": platform.system(),
            "os version": platform.version(),
            
        }

        try:
            import psutil
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

            status.update({
                "cpu usage": f"{cpu_usage}%",
                "memory total": f"{memory.total / (1024 ** 3):.2f} GB",
                "memory used": f"{memory.used / (1024 ** 3):.2f} GB",
                "memory percent": f"{memory.percent}%",
                "disk total": f"{disk.total / (1024 ** 3):.2f} GB",
                "disk used": f"{disk.used / (1024 ** 3):.2f} GB",
                "disk percent": f"{disk.percent}%",
                "boot time": boot_time
            })
            
        except ImportError:
            pass
        
        for key, value in status.items():
            embed.add_embed_field(name=key.title(), value=value, inline=True)

        return embed
