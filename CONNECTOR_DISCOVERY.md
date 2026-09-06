# Harness Cloud Cost Management Connector — Connector Discovery

**Vendor API Baseline:** https://harness.io

## Архитектура API
- **Базовый адрес:** `https://app.harness.io/gateway/ccm/api`
- **Протокол:** REST / HTTPS (JSON)
- **Аутентификация:** Harness API Key (x-api-key header)
- **Ключевые эндпоинты:**
  - бюджеты (/budgets)
  - рекомендации по автоскейлингу (/recommendations)
  - аномалии (/anomalies)
  - кластеры Kubernetes
- **Тестовая точка проверки подключения:** `GET /gateway/ccm/api/budgets`.
