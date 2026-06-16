# The Zelyonka Club Telegram Bot

Рабочая основа Telegram-бота для клуба Зелёнки.

## Что внутри

- приветствие клуба;
- главное меню;
- выбор бокса;
- памятки по уходу;
- плейлисты;
- ростомер для CHERRY-MARRY, RED FLAG и VERY BERRY;
- раздел "Это нормально?";
- зелёная страховка;
- маленькие победы;
- "Полей себя тоже";
- привилегии клуба.

Бот написан без внешних библиотек, только на стандартном Python.

## Как запустить

1. Установи Python 3.10+.
2. Получи токен у BotFather.
3. В PowerShell запусти:

```powershell
$env:TELEGRAM_BOT_TOKEN="твой_токен_от_BotFather"
python bot.py
```

Если команда `python` открывает Microsoft Store, установи Python с python.org и перезапусти терминал.

Чтобы бот присылал тебе заявки по зелёной страховке и фото побед, можно добавить свой Telegram chat id:

```powershell
$env:ADMIN_CHAT_ID="твой_chat_id"
```

Проще всего узнать chat id через бота `@userinfobot` в Telegram.

## Что написать в BotFather

### About

Зелёнка — закрытый клуб для тех, кто выращивает дома томаты, травы, землянику и маленькие победы.

### Description

✨ The Zelyonka Club

Рада приветствовать тебя в закрытом клубе Зелёнки 🌱

Место, где растут томаты, травы, земляника и маленькие победы.

Выбери свой бокс, а я подскажу, что делать дальше.

Выращено тобой.

### Commands

```text
start - открыть клуб Зелёнки
menu - главное меню
box - выбрать свой бокс
help - помощь
```

## Важное

Плейлисты сейчас стоят как заглушки. Замени ссылки `https://example.com/...` в файле `bot.py` на свои реальные ссылки.

Заявки по зелёной страховке и фото маленьких побед бот пока сохраняет в файл `zelyonka_data.json` рядом с кодом.

## Бесплатный запуск на Render

На Render выбирай не Background Worker, а Web Service.

Настройки:

- Language: Python 3
- Build Command: оставить пустым или поставить `pip install -r requirements.txt`
- Start Command: `python bot.py`
- Instance Type: Free, если доступен
- Environment Variables:
  - `TELEGRAM_BOT_TOKEN` = токен от BotFather
  - `ADMIN_CHAT_ID` = твой chat id, если хочешь получать заявки себе

Бот внутри запускает маленькую health-страницу для Render и параллельно отвечает в Telegram.
