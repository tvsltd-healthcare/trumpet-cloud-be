# Use the latest stable Python 3.12 slim image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl


# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./
COPY ./pyproject.toml ./

# Install dependencies without development dependencies and without installing the current project
RUN poetry install --only main --no-root

# RUN poetry install --no-dev --no-root \
#     && poetry add git+https://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@github.com/tvsltd/wrap_restify.git#develop \
#     && poetry add git+https://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@github.com/tvsltd/wrap_validate.git#develop \
#     && poetry install --no-root 

# mountpoint of our code
WORKDIR /home/code

# COPY ./entrypoint.sh .
COPY . .

# RUN chmod +x /home/code/entrypoint.sh

EXPOSE 8080

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app_layer_entrypoint:launch_app_layer", "--host", "0.0.0.0", "--port", "8080"]
