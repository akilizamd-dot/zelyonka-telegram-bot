import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "").strip()
API_URL = f"https://api.telegram.org/bot{TOKEN}"
DATA_PATH = Path(__file__).with_name("zelyonka_data.json")


BOXES = {
    "micro": {
        "title": "🌱 ПОЖАЛУЙСТА, ЖИВИ",
        "subtitle": "Мы верим в вас обоих.",
        "composition": "Кресс-салат • Горчица • Микрозелень редиса",
        "playlist": "https://example.com/playlist-micro",
        "has_growth": False,
        "has_transplant": False,
        "care": """🌱 ПОЖАЛУЙСТА, ЖИВИ

Мы верим в вас обоих.

1. Смочи коврики водой.
2. Слей лишнюю воду: коврик влажный, не мокрый.
3. Равномерно рассыпь семена.
4. Слегка опрыскай водой.
5. Накрой крышкой или плёнкой.

Первые всходы: 1-3 дня.
Сбор: через 5-10 дней.

Не переливай. Микрозелень любит заботу, но не бассейн.""",
    },
    "tea": {
        "title": "☕ ЧАЙНАЯ ТЕРАПИЯ",
        "subtitle": "Сначала вырастить. Потом заварить.",
        "composition": "Мелисса • Чабрец • Монарда",
        "playlist": "https://example.com/playlist-tea",
        "has_growth": False,
        "has_transplant": True,
        "care": """☕ ЧАЙНАЯ ТЕРАПИЯ

Сначала вырастить. Потом заварить.

1. На дно кашпо насыпь керамзит 1-2 см.
2. Добавь грунт.
3. Слегка смешай верхний слой с удобрением.
4. Увлажни землю.
5. Раздели горшок на 3 зоны.
6. Тимьян прижми, мелиссу и монарду слегка присыпь.
7. Опрыскай водой и накрой плёнкой.

Всходы: 7-21 день.
Полив: умеренно, когда верхний слой подсох.""",
    },
    "bella": {
        "title": "🍝 BELLA CIAO",
        "subtitle": "Для пасты, пиццы и красивой жизни.",
        "composition": "Орегано • Тимьян • Майоран",
        "playlist": "https://example.com/playlist-bella",
        "has_growth": False,
        "has_transplant": True,
        "care": """🍝 BELLA CIAO

Для пасты, пиццы и красивой жизни.

1. Керамзит на дно кашпо.
2. Добавь грунт.
3. Увлажни землю.
4. Смешай верхний слой с удобрением.
5. Тимьян прижми, орегано и майоран слегка присыпь.
6. Опрыскай водой.
7. Накрой плёнкой.

Всходы: 7-14 дней.
Полив: когда верх подсох.

Buon appetito. Маленькая Италия начинается на подоконнике.""",
    },
    "cherry": {
        "title": "🍅 CHERRY-MARRY",
        "subtitle": "Спойлер: будут помидоры.",
        "composition": "Томат черри",
        "playlist": "https://example.com/playlist-cherry",
        "has_growth": True,
        "has_transplant": True,
        "care": """🍅 CHERRY-MARRY

Спойлер: будут помидоры.

1. Керамзит на дно.
2. Добавь грунт.
3. Увлажни землю.
4. Сделай лунки 2-3 мм.
5. Посади семена.
6. Присыпь, опрыскай и накрой.

Всходы: 5-10 дней.
После всходов: убери крышку и поставь на свет.
Полив: когда верх подсох. Без перелива.""",
    },
    "pepper": {
        "title": "🌶️ RED FLAG",
        "subtitle": "Но на этот раз это хорошо.",
        "composition": "Красный острый перец",
        "playlist": "https://example.com/playlist-pepper",
        "has_growth": True,
        "has_transplant": True,
        "care": """🌶️ RED FLAG

Но на этот раз это хорошо.

1. Керамзит на дно 1-2 см.
2. Добавь грунт, оставив 1 см до края.
3. Смешай верхний слой с удобрением.
4. Увлажни землю.
5. Сделай 3-4 лунки 0,5-1 см.
6. Посади семена, присыпь, опрыскай.
7. Накрой плёнкой.

Всходы: 7-14 дней.
Полив: когда верх подсох.
Оставь одно сильное растение, остальные аккуратно срежь.""",
    },
    "berry": {
        "title": "🍓 VERY BERRY",
        "subtitle": "Самая сладкая победа.",
        "composition": "Земляника Александрия",
        "playlist": "https://example.com/playlist-berry",
        "has_growth": True,
        "has_transplant": True,
        "care": """🍓 VERY BERRY

Твоя сладкая победа.

1. Керамзит 1-2 см на дно.
2. Добавь грунт, оставив 1 см до края.
3. Увлажни землю.
4. Семена положи по поверхности. Не закапывать.
5. Прижми и накрой плёнкой.

Всходы: 10-30 дней.
Полив: пульверизатор, слегка влажная почва.
После всходов: убери укрытие и поставь на свет.""",
    },
}


SELF_CARE_CARDS = [
    "☕ Полей себя тоже.\n\nСделай чай, открой окно на 5 минут и не требуй от себя быть продуктивной каждую секунду.",
    "🌿 Сегодня можно медленно.\n\nРастения не торопятся и всё равно растут. Попробуем взять с них пример.",
    "💚 Маленькая забота считается.\n\nВода растению. Вода тебе. Уже неплохо.",
    "✨ Если день странный, это не значит, что ты странная.\n\nИногда всем нужен свет, воздух и чуть меньше давления.",
]


def load_data():
    if not DATA_PATH.exists():
        return {"users": {}, "insurance": [], "wins": []}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_data(data):
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def api(method, payload=None, files=None):
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is empty. Add the token from BotFather first.")
    payload = payload or {}
    url = f"{API_URL}/{method}"
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def keyboard(rows):
    return json.dumps({"inline_keyboard": rows}, ensure_ascii=False)


def btn(text, callback_data):
    return {"text": text, "callback_data": callback_data}


def url_btn(text, url):
    return {"text": text, "url": url}


def send(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api("sendMessage", payload)


def send_photo(chat_id, photo_file_id, caption=""):
    payload = {"chat_id": chat_id, "photo": photo_file_id, "caption": caption}
    return api("sendPhoto", payload)


def notify_admin(text):
    if ADMIN_CHAT_ID:
        send(ADMIN_CHAT_ID, text)


def notify_admin_photo(photo_file_id, caption):
    if ADMIN_CHAT_ID:
        send_photo(ADMIN_CHAT_ID, photo_file_id, caption)


def answer_callback(callback_id):
    api("answerCallbackQuery", {"callback_query_id": callback_id})


def main_menu():
    return keyboard([
        [btn("🌿 Мой бокс", "menu:boxes")],
        [btn("💚 Зелёная страховка", "menu:insurance")],
        [btn("🌱 Маленькие победы", "menu:wins")],
        [btn("🆘 Это нормально?", "menu:normal")],
        [btn("☕ Полей себя тоже", "menu:selfcare")],
        [btn("✨ Привилегии клуба", "menu:perks")],
    ])


def boxes_menu():
    return keyboard([
        [btn("🌱 ПОЖАЛУЙСТА, ЖИВИ", "box:micro")],
        [btn("☕ ЧАЙНАЯ ТЕРАПИЯ", "box:tea")],
        [btn("🍝 BELLA CIAO", "box:bella")],
        [btn("🍅 CHERRY-MARRY", "box:cherry")],
        [btn("🌶️ RED FLAG", "box:pepper")],
        [btn("🍓 VERY BERRY", "box:berry")],
        [btn("⬅️ Главное меню", "menu:main")],
    ])


def box_menu(box_id):
    box = BOXES[box_id]
    rows = [
        [btn("📖 Памятка по уходу", f"care:{box_id}")],
        [url_btn("🎵 Плейлист", box["playlist"])],
    ]
    if box["has_growth"]:
        rows.append([btn("🌱 Ростомер", f"growth:{box_id}")])
    if box["has_transplant"]:
        rows.append([btn("🪴 Помощь с пересадкой", f"transplant:{box_id}")])
    rows.extend([
        [btn("🆘 Это нормально?", "menu:normal")],
        [btn("⬅️ Выбрать другой бокс", "menu:boxes")],
    ])
    return keyboard(rows)


def start_text():
    return """✨ <b>The Zelyonka Club</b>

Рада приветствовать тебя в закрытом клубе Зелёнки 🌱

Место, где растут томаты, травы, земляника и маленькие победы.

Выбери свой бокс, а я подскажу, что делать дальше.

Выращено тобой."""


def box_text(box_id):
    box = BOXES[box_id]
    return f"""<b>{box["title"]}</b>

{box["subtitle"]}

{box["composition"]}

Выбери, что нужно сейчас. Я рядом."""


def normal_menu():
    return keyboard([
        [btn("🌱 Ничего не взошло", "normal:no_sprouts")],
        [btn("📏 Росток слишком высокий", "normal:tall")],
        [btn("🍃 Листья желтеют", "normal:yellow")],
        [btn("😱 Всё выглядит странно", "normal:strange")],
        [btn("⬅️ Главное меню", "menu:main")],
    ])


def set_user_state(chat_id, **updates):
    data = load_data()
    user = data["users"].setdefault(str(chat_id), {})
    user.update(updates)
    save_data(data)


def get_user(chat_id):
    return load_data()["users"].get(str(chat_id), {})


def handle_start(chat_id):
    send(chat_id, start_text(), main_menu())


def handle_menu(chat_id, item):
    if item == "main":
        send(chat_id, start_text(), main_menu())
    elif item == "boxes":
        send(chat_id, "🌿 Какой бокс у тебя дома?", boxes_menu())
    elif item == "insurance":
        set_user_state(chat_id, waiting_for="insurance")
        send(chat_id, """💚 <b>Зелёная страховка</b>

Иногда семена тоже переживают сложный период.

Если сроки всходов прошли, а ничего не появилось — напиши мне одним сообщением:

📦 какой у тебя бокс
📅 дату посадки
📸 что случилось

Можно приложить фото следующим сообщением. Посмотрим вместе.

Если дело действительно в семенах — отправим новые.""", keyboard([[btn("⬅️ Главное меню", "menu:main")]]))
    elif item == "wins":
        set_user_state(chat_id, waiting_for="win")
        send(chat_id, """🌱 <b>Маленькие победы</b>

Если у тебя что-то выросло — покажи.

Отправь фото или сообщение про свой росток. Порадуемся вместе.""", keyboard([[btn("⬅️ Главное меню", "menu:main")]]))
    elif item == "normal":
        send(chat_id, "🆘 Не паникуем. Сначала проверим, сталкивался ли кто-то с этим до тебя 🌱", normal_menu())
    elif item == "selfcare":
        card = SELF_CARE_CARDS[int(time.time()) % len(SELF_CARE_CARDS)]
        send(chat_id, card, keyboard([[btn("☕ Ещё карточку", "menu:selfcare")], [btn("⬅️ Главное меню", "menu:main")]]))
    elif item == "perks":
        send(chat_id, """✨ <b>Привилегии клуба</b>

Некоторые вещи доступны только участникам The Zelyonka Club 🌱

🎁 подарок на следующий набор
🌿 ранний доступ к новинкам
🌱 секретное семечко
🤫 кое-что готовится

Когда следующий секретный выпуск будет готов — я обязательно сообщу.""", keyboard([[btn("⬅️ Главное меню", "menu:main")]]))


def handle_box(chat_id, box_id):
    set_user_state(chat_id, selected_box=box_id, waiting_for=None)
    send(chat_id, box_text(box_id), box_menu(box_id))


def handle_care(chat_id, box_id):
    send(chat_id, BOXES[box_id]["care"], keyboard([[btn("⬅️ Назад к боксу", f"box:{box_id}")]]))


def handle_growth(chat_id, box_id):
    set_user_state(chat_id, selected_box=box_id, waiting_for="growth_date")
    send(chat_id, """🌱 Когда ты посадил(а) семена?

Напиши дату в формате:

ДД.ММ.ГГГГ

Например: 16.06.2026""", keyboard([[btn("⬅️ Назад к боксу", f"box:{box_id}")]]))


def growth_message(days):
    if days < 0:
        return "Кажется, эта дата ещё впереди. Растение пока только в планах, но мы одобряем."
    if days < 3:
        return "Пока просто ждём. Самая сложная часть — не раскопать всё из любопытства."
    if days < 7:
        return "Пока ничего не видно. Но под землёй уже идёт работа."
    if days < 14:
        return "🌱 Уже целая неделя. Неплохо идёте."
    if days < 30:
        return "🌿 Две недели позади. Кажется, у вас получается."
    if days < 60:
        return "🌱 Уже месяц. Если честно, это повод собой гордиться."
    return "🌿 Уже два месяца. Кажется, вы отлично сработались."


def parse_date(text):
    match = re.fullmatch(r"\s*(\d{2})\.(\d{2})\.(\d{4})\s*", text or "")
    if not match:
        return None
    day, month, year = map(int, match.groups())
    try:
        return date(year, month, day)
    except ValueError:
        return None


def handle_transplant(chat_id, box_id):
    send(chat_id, """🪴 <b>Помощь с пересадкой</b>

Когда растение окрепнет и ему станет тесно, пора подумать о горшке побольше.

Обычно сигнал такой:
• корням тесно;
• растение вытягивается;
• земля быстро пересыхает;
• стало понятно: малыш вырос.

Пересаживай аккуратно, с комом земли. После пересадки — светлое место и немного спокойствия.

Если сомневаешься, пришли фото в раздел «Это нормально?».""", keyboard([[btn("⬅️ Назад к боксу", f"box:{box_id}")]]))


def handle_normal(chat_id, topic):
    texts = {
        "no_sprouts": """🌱 <b>Ничего не взошло</b>

Не переживай. У всех растений свой характер.

Примерные сроки:
• микрозелень — 1-3 дня
• томат — 5-10 дней
• перец — 7-14 дней
• земляника — 10-30 дней
• чайные и итальянские травы — 7-21 день

Если сроки уже прошли — воспользуйся Зелёной страховкой 💚""",
        "tall": """📏 <b>Росток слишком высокий</b>

Спокойно 🌱

Скорее всего, ему просто не хватает света.

Что сделать:
☀️ поставить на самое светлое окно
🔄 иногда поворачивать кашпо
💡 при необходимости добавить подсветку

Лампу лучше располагать примерно в 15-30 см от растения.""",
        "yellow": """🍃 <b>Листья желтеют</b>

Жёлтые листья — один из самых частых сигналов.

Обычно причины такие:
💧 слишком много воды
☀️ мало света
🌱 старые листья просто решили уйти на пенсию

Проверь полив и свет. Если всё равно тревожно — пришли фото.""",
        "strange": """😱 <b>Всё выглядит странно</b>

Отправь фотографию растения.

Я посмотрю и постараюсь ответить в течение 48 часов 🌿""",
    }
    send(chat_id, texts[topic], keyboard([[btn("💚 Зелёная страховка", "menu:insurance")], [btn("⬅️ Назад", "menu:normal")]]))


def handle_text(chat_id, text):
    user = get_user(chat_id)
    waiting_for = user.get("waiting_for")

    if text in ("/start", "/menu"):
        handle_start(chat_id)
        return
    if text == "/box":
        handle_menu(chat_id, "boxes")
        return
    if text == "/help":
        send(chat_id, "Напиши /menu, чтобы открыть главное меню Зелёнки 🌱")
        return

    if waiting_for == "growth_date":
        planted = parse_date(text)
        if not planted:
            send(chat_id, "Не смогла понять дату. Напиши в формате ДД.ММ.ГГГГ, например 16.06.2026.")
            return
        box_id = user.get("selected_box", "cherry")
        days = (date.today() - planted).days
        set_user_state(chat_id, planted_at=planted.isoformat(), waiting_for=None)
        send(chat_id, f"""🌱 Готово.

Теперь у твоего растения есть собственный ростомер.

Сегодня день: <b>{days}</b>.

{growth_message(days)}""", keyboard([[btn("🌱 Проверить ростомер", f"check_growth:{box_id}")], [btn("⬅️ Назад к боксу", f"box:{box_id}")]]))
        return

    if waiting_for in ("insurance", "win"):
        data = load_data()
        item = {
            "chat_id": chat_id,
            "text": text,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        if waiting_for == "insurance":
            data["insurance"].append(item)
            save_data(data)
            set_user_state(chat_id, waiting_for="insurance_photo")
            notify_admin(f"💚 Новая заявка по зелёной страховке\n\nchat_id: {chat_id}\n\n{text}")
            send(chat_id, "💚 Приняла. Посмотрим вместе. Если есть фото — отправь его следующим сообщением.")
        else:
            data["wins"].append(item)
            save_data(data)
            set_user_state(chat_id, waiting_for=None)
            notify_admin(f"🌱 Новая маленькая победа\n\nchat_id: {chat_id}\n\n{text}")
            send(chat_id, "🌱 Маленькая, но важная победа зафиксирована. Поздравляю 🤍")
        return

    send(chat_id, "Я рядом 🌱 Выбери раздел в меню.", main_menu())


def handle_photo(chat_id, message):
    user = get_user(chat_id)
    waiting_for = user.get("waiting_for")
    data = load_data()
    item = {
        "chat_id": chat_id,
        "caption": message.get("caption", ""),
        "photo_file_id": message["photo"][-1]["file_id"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    if waiting_for in ("insurance", "insurance_photo"):
        data["insurance"].append(item)
        save_data(data)
        set_user_state(chat_id, waiting_for=None)
        notify_admin_photo(message["photo"][-1]["file_id"], f"💚 Фото для зелёной страховки\nchat_id: {chat_id}\n\n{message.get('caption', '')}")
        send(chat_id, "💚 Фото получила. Посмотрим вместе и решим, что делать дальше.")
    else:
        data["wins"].append(item)
        save_data(data)
        set_user_state(chat_id, waiting_for=None)
        notify_admin_photo(message["photo"][-1]["file_id"], f"🌱 Маленькая победа\nchat_id: {chat_id}\n\n{message.get('caption', '')}")
        send(chat_id, "🌱 Маленькая, но важная победа зафиксирована. Поздравляю 🤍")


def handle_callback(callback):
    chat_id = callback["message"]["chat"]["id"]
    data = callback["data"]
    answer_callback(callback["id"])

    if data.startswith("menu:"):
        handle_menu(chat_id, data.split(":", 1)[1])
    elif data.startswith("box:"):
        handle_box(chat_id, data.split(":", 1)[1])
    elif data.startswith("care:"):
        handle_care(chat_id, data.split(":", 1)[1])
    elif data.startswith("growth:"):
        handle_growth(chat_id, data.split(":", 1)[1])
    elif data.startswith("transplant:"):
        handle_transplant(chat_id, data.split(":", 1)[1])
    elif data.startswith("normal:"):
        handle_normal(chat_id, data.split(":", 1)[1])
    elif data.startswith("check_growth:"):
        box_id = data.split(":", 1)[1]
        user = get_user(chat_id)
        planted_at = user.get("planted_at")
        if not planted_at:
            handle_growth(chat_id, box_id)
            return
        planted = date.fromisoformat(planted_at)
        days = (date.today() - planted).days
        send(chat_id, f"🌱 Сегодня день <b>{days}</b>.\n\n{growth_message(days)}", keyboard([[btn("⬅️ Назад к боксу", f"box:{box_id}")]]))


def handle_update(update):
    if "callback_query" in update:
        handle_callback(update["callback_query"])
        return
    message = update.get("message")
    if not message:
        return
    chat_id = message["chat"]["id"]
    if "photo" in message:
        handle_photo(chat_id, message)
        return
    handle_text(chat_id, message.get("text", ""))


def run():
    if not TOKEN:
        print("Add TELEGRAM_BOT_TOKEN first.")
        return

    print("The Zelyonka Club bot is running.")
    offset = None
    while True:
        try:
            payload = {"timeout": 30}
            if offset is not None:
                payload["offset"] = offset
            response = api("getUpdates", payload)
            for update in response.get("result", []):
                offset = update["update_id"] + 1
                handle_update(update)
        except urllib.error.URLError as exc:
            print(f"Network error: {exc}. Retrying...")
            time.sleep(5)
        except Exception as exc:
            print(f"Error: {exc}")
            time.sleep(2)


if __name__ == "__main__":
    run()
