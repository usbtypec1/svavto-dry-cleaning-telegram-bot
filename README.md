# Бот для рассмотрения запросов на химчистку

---

## 📝 Описание

В этот бот будут приходить запросы на химчистку. Админы могут рассмотреть и
либо одобрить, либо отклонить заявку.

---

## 🔧 Конфигурация

Для работы бота необходимо создать файл `config.toml` в корне проекта и
заполнить его

```toml
[telegram_bot]
token = "Токен бота"
whitelist_user_ids = [123456789, 987654321]

[web_app]
msk_base_url = "базовый url web app для Москвы"
spb_base_url = "базовый url web app для Санкт-Петербурга"

[api]
msk_base_url = "базовый url API для Москвы"
spb_base_url = "базовый url API для Санкт-Петербурга"

```

Так же нужно настроить логгирование.
Для этого сделайте копию файла `logging_config.example.json` и переименуйте его
в `logging_config.json`.

---

## 🚀 Запуск проекта

```shell
uv venv
source .venv/bin/activate
uv sync
python src/main.py
```
