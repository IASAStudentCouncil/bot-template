# bot-template

Шаблон Telegram-бота Студради ІПСА: aiogram 3, автодеплой у контейнер `bots` на сервері ІПСА,
сповіщення про деплой у чат IT-відділу.

## Новий бот за 10 хвилин

1. **Створити репо з шаблону.** Зверху на цій сторінці: **Use this template → Create a new repository**.
   Owner — `IASAStudentCouncil`, назва — коротко й латиницею (`merch-bot`, `kyao-bot`).
   Назва репо = назва застосунку на сервері, тож потім її краще не міняти.
2. **Отримати токен** у [@BotFather](https://t.me/BotFather): `/newbot`.
3. **Попросити девопса підключити репо.** Він виконає:
   ```bash
   iasa-infra/scripts/connect-repo.sh <назва-репо> bots
   ```
   і впише токен бота на сервері (`apps env <назва-репо>` → `BOT_TOKEN=...`).
   Токен бота в git не кладемо ніколи.
4. **Писати код** у `bot.py` (або розбити на модулі), залежності — у `requirements.txt`.
5. **Push у `main`** (краще через PR): CI перевірить код і задеплоїть бота, а в гілку *CI BOT*
   прийде 🟩. Якщо бот не стартував, деплой відкотиться на попередню версію, прийде 🟥,
   і в лозі run'а буде причина.

## Локальний запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env        # і вписати свій тестовий токен
python bot.py
```

Для локальних тестів краще завести окремого тестового бота, щоб не конфліктувати з продовим.
Telegram не дозволяє двом процесам одночасно робити polling з одним токеном.

Перед push варто прогнати те саме, що й CI:
```bash
ruff check . && python -c "import bot"
```

## Як це влаштовано

| Файл | Навіщо |
|---|---|
| `bot.py` | сам бот: хендлери і запуск |
| `requirements.txt` | залежності, що ставляться на сервері |
| `requirements-dev.txt` | + інструменти для розробки (ruff, python-dotenv) |
| `deploy/app.conf` | як запускати бота в контейнері (`START`), що зберігати між деплоями (`PERSIST`) |
| `data/` | файли, що переживають деплої: SQLite, JSON… (у git не потрапляють) |
| `.github/workflows/deploy.yml` | CI/CD: lint → деплой → сповіщення |
| `.github/dependabot.yml` | щотижневі PR з оновленнями залежностей |
| `ruff.toml` | правила лінтера, однакові локально і в CI |

Бот працює через **polling**, тому відкривати порти не потрібно. Якщо колись знадобиться webhook,
порти 8000–8003 контейнера `bots` зарезервовані під це. Узгодьте з девопсом, який узяти.

## На сервері

```bash
ssh -p <SSH-порт bots> deploy@<сервер>
apps                        # статус усіх ботів
apps logs <назва> -f        # логи
apps restart <назва>
apps rollback <назва>       # попередня версія
apps env <назва>            # BOT_TOKEN та інші секрети
```

Детальніше — в [iasa-infra](https://github.com/IASAStudentCouncil/iasa-infra).
