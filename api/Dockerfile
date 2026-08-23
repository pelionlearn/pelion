# syntax=docker/dockerfile:1.22

FROM ubuntu:26.10 AS builder-image
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y curl ca-certificates && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV UV_PYTHON_INSTALL_DIR=/home/myuser/.uvpython
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN useradd --create-home myuser
USER myuser
WORKDIR /home/myuser

ADD --chown=myuser https://astral.sh/uv/install.sh uv-installer.sh
RUN sh uv-installer.sh && rm uv-installer.sh
ENV PATH="/home/myuser/.local/bin:$PATH"

RUN uv python install 3.13
RUN uv python pin 3.13

COPY .python-version .
COPY uv.lock .
COPY pyproject.toml .

RUN uv sync --frozen

FROM ubuntu:26.10 AS runner-image

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home myuser
RUN mkdir -p /storage && chown -R myuser:myuser /storage
USER myuser
WORKDIR /home/myuser

COPY --from=builder-image --chown=myuser:myuser /home/myuser/.uvpython /home/myuser/.uvpython
COPY --from=builder-image --chown=myuser:myuser /home/myuser/.venv /home/myuser/.venv
COPY --from=builder-image --chown=myuser:myuser /home/myuser/pyproject.toml /home/myuser/uv.lock ./

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/home/myuser/.venv
ENV PATH="/home/myuser/.venv/bin:$PATH"

COPY --chown=myuser:myuser . .

# use this for alembic migrations
# RUN chmod +x /home/myuser/entrypoint.sh
# ENTRYPOINT [ "/home/myuser/entrypoint.sh" ]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
