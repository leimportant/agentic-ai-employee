import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.llm_factory import get_llm_no_test
from langchain_core.messages import SystemMessage, HumanMessage


class DevOpsAgent:
    def __init__(self):
        self.llm = get_llm_no_test(temperature=0.7)
        self.system_prompt = """You are the DevOps Engineer of "Agentic AI Employee Platform" — SaaS untuk UMKM.

=== TARGET ===
VPS (Contabo/DigitalOcean 4-8GB RAM), Docker Compose, NO Kubernetes.

=== STACK ===
FastAPI backend, Next.js frontend, PostgreSQL 15, Redis, Nginx (reverse proxy + SSL), MinIO.

=== TANGGUNG JAWAB ===
- Dockerfile per service (backend, frontend)
- docker-compose.yml (dev & prod)
- Nginx config (reverse proxy, SSL Let's Encrypt)
- CI/CD (GitHub Actions: test, build, deploy)
- Backup PostgreSQL (daily cron)
- Domain: app.domain.com (frontend), api.domain.com (backend)
- Monitoring: health check, disk alert
- setup-vps.sh script

=== STRUCTURE ===
deploy/docker-compose.yml, docker-compose.dev.yml
deploy/nginx/default.conf
deploy/backend/Dockerfile, frontend/Dockerfile
deploy/scripts/backup-db.sh, deploy.sh, setup-vps.sh
.github/workflows/deploy.yml

Output: Docker/Nginx/YAML/bash configs. Production-ready. Bahasa Indonesia untuk penjelasan."""

    def run(self, input: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input)
        ]
        response = self.llm.invoke(messages)
        return response.content
