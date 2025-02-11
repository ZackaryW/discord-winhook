
import subprocess
from discord_winhook.base import BaseHook
from discord_webhook import DiscordEmbed

class SubprocessHook(BaseHook):
    def __init__(self, url: str, command: str):
        super().__init__(url)
        self.__command = command

    def construct_embed(self):
        embed = DiscordEmbed(title="Subprocess Output", color="03b2f8")

        output = self.run_subprocess()

        embed.add_embed_field(name="Command", value=self.__command, inline=False)
        embed.add_embed_field(name="Output", value=f"```\n{output}\n```", inline=False)
        return embed

    def run_subprocess(self):
        try:
            result = subprocess.run(self.__command, capture_output=True, text=True, shell=True, timeout=10)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
        except subprocess.TimeoutExpired as e:
            return f"Error: {e}"
