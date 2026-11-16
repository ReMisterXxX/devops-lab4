# Lab4 – Automatyzacja deploymentu

Prosta aplikacja webowa (REST API do zarządzania zadaniami) w Pythonie (Flask) z bazą PostgreSQL.
Deployment jest zautomatyzowany z użyciem Dockera, docker-compose, GitHub Actions oraz Kubernetes.

## Struktura
| Plik / folder | Opis |
|---|---|
| `app/` | kod aplikacji (`/`, `/health`, `/tasks`) |
| `Dockerfile` | obraz aplikacji |
| `docker-compose.yml` | aplikacja + baza PostgreSQL |
| `tests/unit` | testy jednostkowe (bez bazy danych) |
| `tests/integration` | testy integracyjne na działającym środowisku |
| `k8s/` | manifesty Kubernetes: Namespace, ConfigMap, Secret, Deployment, Service |
| `.github/workflows/ci-cd.yml` | pipeline CI/CD |

## Uruchomienie lokalne
```
docker compose up -d --build
curl http://localhost:5000/health
```

## Pipeline CI/CD (GitHub Actions)
Pipeline uruchamia się automatycznie po każdym pushu do gałęzi `main`:
1. **Build** – budowanie obrazu Docker,
2. **Test** – testy jednostkowe (pytest),
3. **Testy integracyjne** – uruchomienie aplikacji z bazą przez docker compose i testy API,
4. **Deploy** – wdrożenie na środowisko testowe w klastrze Kubernetes (kind) ze strategią rolling update,
5. **Powiadomienie** – podsumowanie statusu wdrożenia (opcjonalnie Slack, jeśli ustawiono sekret `SLACK_WEBHOOK_URL`).
