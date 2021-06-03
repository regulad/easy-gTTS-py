# py-easygTTS

Asynchronous interface to an [easy-gtts](https://github.com/regulad/easy-gTTS-API) server written with `aiohttp`.  

## Examples

```python
import asyncio
from easygTTS import AsyncEasyGTTSSession


async def main():
    async with AsyncEasyGTTSSession("https://easy-gtts-api.dingus-server.regulad.xyz/") as text_to_speech:
        audio_bytes = await text_to_speech.synthesize("Hello, stinky world!")

    with open("Hello_world.mp3", "wb") as f:
        f.write(audio_bytes)
asyncio.run(main())
```