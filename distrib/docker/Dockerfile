# syntax=docker/dockerfile:1
FROM python:3.13.2-slim-bookworm

LABEL authors="Andrey Ryabtsev"

RUN useradd -U llm-text-processor -m
WORKDIR /home/llm-text-processor
USER llm-text-processor
COPY --chown=llm-text-processor:llm-text-processor app ./app
COPY --chown=llm-text-processor:llm-text-processor pyproject.toml ./
COPY --chown=llm-text-processor:llm-text-processor distrib/docker/entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

RUN python -m pip install --upgrade pip
RUN pip install hatch
RUN python -m hatch env create prod

EXPOSE 8080
ENTRYPOINT ["/home/llm-text-processor/entrypoint.sh"]