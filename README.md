<div align="center">

# <3 gif thang (discord bot)

discord bot that posts random tenor gifs.  
token + api key are kept out of the repo.

![python](https://img.shields.io/badge/python-3.x-ff78c8?style=for-the-badge)
![discord](https://img.shields.io/badge/bot-discord-0b0b0b?style=for-the-badge)
![vibe](https://img.shields.io/badge/vibe-terminal--core-ff4db8?style=for-the-badge)

</div>

---

## setup

```bash
pip install -r requirements.txt
```

set these env vars (see `.env.example`):

- `DISCORD_BOT_TOKEN`
- `TENOR_API_KEY`
- `TARGET_CHANNEL_ID`

## run

```bash
python .\src\gif_thangalang.py
```

## security note

never commit your discord token. if it ever leaks, regenerate it immediately.
