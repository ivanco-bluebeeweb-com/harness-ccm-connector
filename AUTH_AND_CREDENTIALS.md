# Harness Cloud Cost Management Connector — Auth & Credentials Standard

**Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Схема аутентификации
- **Метод:** Harness API Key (x-api-key header)
- **Хранение:** Секреты сохраняются изолированно в хранилище секретов платформы Imperal.
- **Валидация:** При сохранении ключа выполняется тестовый запрос `GET /gateway/ccm/api/budgets`.
- **Отключение:** Удаление локальных ключей без воздействия на аккаунт вендора.
