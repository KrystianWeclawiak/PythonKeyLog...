# Async Discord Keylogger

**Category:** Educational / Security Tools / Python Scripting  
**Author:** Krystian Węcławiak  
**Language:** Python 3  

---

## Disclaimer
**IMPORTANT: PLEASE READ BEFORE USE**

This software is provided for **educational purposes only**. It is intended to demonstrate how keystroke capturing works, how asynchronous programming in Python handles I/O operations, and how to interact with APIs (Discord Webhooks).

**Do not use this script on any system you do not own or do not have explicit permission to monitor.** Unauthorized interception of data is illegal and punishable by law. The author assumes no liability for any misuse of this software.

---

## Overview

This project is a lightweight, asynchronous keylogger written in Python. It captures keystrokes using the `pynput` library and sends the collected data to a Discord channel via a Webhook.

Unlike simple keyloggers, this script uses **buffering** and **asynchronous execution (`asyncio`)**. This ensures that the key logging process does not block the main thread, and the script sends data in chunks (batches) rather than spamming the Discord API with every single keystroke.

## Features

* **Asynchronous Architecture:** Uses `asyncio` to handle the blocking keyboard listener and network requests concurrently.
* **Buffered Sending:** Captures a specific number of keys (configurable via `max_buffer_size`) before sending, reducing API calls.
* **Smart Editing:** Handles the `Backspace` key logically (removes the last character from the local buffer instead of logging "[Backspace]").
* **Discord Embeds:** Sends data in a clean, formatted Discord Embed structure with timestamps.
* **Customizable:** Easy configuration of colors, titles, author names, and buffer limits.

## Requirements

To run this script, you need Python 3 installed along with the following external libraries:

* `pynput`: For monitoring keyboard input.
* `discord-webhook`: For easy interaction with Discord API.

### Installation

1.  Clone the repository or download the script.
2.  Install the dependencies using pip:

```bash
pip install pynput discord-webhook
````

*(Note: `asyncio` is a standard Python library, so it does not need installation).*

## Configuration

Open the script (e.g., `keylogger.py`) and locate the `if __name__ == "__main__":` block at the bottom. Modify the parameters in the `KeyLogger` class instantiation:

```python
kl = KeyLogger(
    webhook_url="YOUR_DISCORD_WEBHOOK_URL_HERE",  # <--- PASTE YOUR WEBHOOK URL
    max_buffer_size=30,      # Number of keystrokes to collect before sending
    embed_username="KeyLogger",
    embed_title="Log Report",
    embed_color="03b2f8",    # Hex color code for the embed sidebar
    embed_author="Anonymous"
)
```

### How to get a Discord Webhook URL:

1.  Open Discord and go to **Server Settings** \> **Integrations** \> **Webhooks**.
2.  Click **New Webhook**.
3.  Copy the **Webhook URL**.

## Usage

Run the script using Python:

```bash
python keylogger.py
```

The script will now run in the background. As you type, keys are stored in a buffer. Once the buffer reaches `max_buffer_size` (e.g., 30 characters), the data is bundled and sent to your Discord channel.

To stop the script, simply terminate the terminal process (Ctrl+C).

## Code Logic (For Developers)

The script solves the problem of blocking I/O operations by combining `pynput` (which is blocking by nature) with `asyncio`:

1.  **`start_listener`**: Runs the blocking `keyboard.Listener` in a separate thread using `loop.run_in_executor`.
2.  **`on_press`**: This callback runs whenever a key is pressed. It appends keys to a list.
3.  **Thread Safety**: When the buffer is full, `asyncio.run_coroutine_threadsafe` is used to schedule the `send_webhook_async` function back onto the main async loop, ensuring the network request doesn't freeze the keyboard listener.

-----

## License

This project is open-source and available for educational modification.
