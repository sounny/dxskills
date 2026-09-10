# DxSkills Cognitive Scaffolding Gateway
# Multi-arch lightweight container image

FROM python:3.11-slim

LABEL maintainer="Dr. Moulay Anwar Sounny-Slitine <sounny@gmail.com>"
LABEL description="Self-hosted DxSkills D-Mode Cognitive Scaffolding Gateway"

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Copy skills, templates, prompts, and server code
COPY server/ /app/server/
COPY skills/ /app/skills/
COPY prompts/ /app/prompts/
COPY scripts/ /app/scripts/

EXPOSE 8080

# Native healthcheck using python standard library (no curl dependency required)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/health').getcode() == 200 else 1)"

CMD ["python", "server/gateway.py"]
