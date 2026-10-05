# Contributing

The HAPI Write App (HWA) is being developed by a team from the [Centre for Humanitarian Data](https://centre.humdata.org/).

HDX developers are using [VS Code](https://code.visualstudio.com/) as a standard IDE for this project with development taking place inside Docker containers.

## One-off container creation activities

There is a test database container that can be started without the HAPI stack and which needs to be created as part of the one-off setup. It's only meant to start under the [testing profile](https://github.com/OCHA-DAP/hdx-hapi-write-app/blob/8ea5e7c47e8572be422d87e58b85c16dc415138d/docker/docker-compose.yml#L35-L36).

First copy `docker/.env.tpl` to `docker/.env` (it is git-ignored) and fill in the values. `HWA_PATCH_TOKEN` is a GitHub token with read access to the patch repo. `BASEDIR` is the host folder where the test database keeps its data, and `POSTGRES_PASSWORD` is the password of its `postgres` user.

The `hwa` container runs the published image `public.ecr.aws/unocha/hdx-hapi-write-app:main`, not one built from the local `Dockerfile`. To use another tag, set `HWA_IMAGE_TAG` in `docker/.env`. The repo is mounted at `/srv/hwa` in the container, so code changes don't need a rebuild.

To create the HWA stack containers in the first instance, including a test database container:

```shell
docker network create -d bridge hapi_stack_hapi
cd docker
docker-compose --profile=testing up -d
docker-compose exec -T hwa sh -c "apk add git build-base"
docker-compose exec -T hwa sh -c "pip install --upgrade -r requirements.txt"
docker-compose exec -T hwa sh -c "pip install --upgrade -r dev-requirements.txt"
cd ..
./initialize_test_db.sh
```

The image removes its build tools after installing its own requirements. `git` is needed to install `hapi-schema` from GitHub (an editable install in `src/hapi-schema`), and `build-base` provides the compiler needed to build `psycopg2`. The image keeps the Python headers (Python is installed under `/usr/local`) and the PostgreSQL headers (`postgresql-dev`), so nothing else is needed. Alpine's `python3-dev` only has headers for Alpine's own `/usr/bin/python3`. CI (`.github/workflows/run-tests.yml`) runs the same steps.

Notes:

- If the `hapi_stack_hapi` network already exists, for example because the HAPI stack created it, `docker network create` fails. That is harmless.
- The `apk` and `pip` installs live inside the container. If it is recreated, for example after pulling a new image or changing `docker/.env`, repeat them.
- With Compose v2 only, use `docker compose` instead of `docker-compose`, and run the scripts as `DCOMPOSE="docker compose" ./initialize_test_db.sh`, as CI does.

## Working on HWA for testing

Once the one-off container creation activities have been done then future testing sessions are started as follows:

```shell
cd docker
docker-compose --profile=testing up -d
cd ..
./initialize_test_db.sh
```

On later runs `./initialize_test_db.sh` reports that the database and user already exist. That is harmless.

Tests can be executed using the following command line or the VS Code test runner:

```shell
cd docker
docker-compose exec -T hwa sh -c "pytest --log-level=INFO"
cd ..
```

The tests always use the `hwa_test` database (`tests/conftest.py` sets `HAPI_DB_NAME`). Each run starts by dropping all its tables and recreating them from the hapi-schema models, without alembic. Some tests download patch files from GitHub. The tests in `tests/test_patch_repo` also call the GitHub API with `HWA_PATCH_TOKEN`, so they fail with 401 if the token in `docker/.env` is missing or invalid.

## Linting

CI (`.github/workflows/run-linter.yml`) installs `dev-requirements.txt` and runs `ruff check` with the settings in `pyproject.toml`. To run it locally:

```shell
cd docker
docker-compose exec -T hwa sh -c "ruff check"
cd ..
```

VS Code applies ruff fixes and formatting on save (`.vscode/settings.json`). CI doesn't run `ruff format`, and some existing files aren't formatted yet, so saving one of them can bring in unrelated formatting changes.

## Working on HWA for HAPI

For HAPI development purposes the project assumes that the HAPI stack is running, or more precisely the HAPI db container.
One can see that the [Docker Compose configuration](https://github.com/OCHA-DAP/hdx-hapi-write-app/blob/8ea5e7c47e8572be422d87e58b85c16dc415138d/docker/docker-compose.yml#L40)
refers to the network `hapi_stack_hapi`.
In this way, any change to the database will be reflected in the locally running HAPI API endpoints.

The HAPI db container and the HWA test database container both publish port `127.0.0.1:45432` and use the host name `db` on that network, so only run one of them at a time. To stop the test database, run `docker-compose --profile=testing stop db` in the HWA `docker` folder.

First start the HAPI project. So run the following in the HAPI project folder:

```shell
cd docker
docker-compose up -d
cd ..
./initialize_db.sh
```

The `./initialize_db.sh` script should be run in the `hdx-hapi` repo. Next spin up the HWA project, assuming that the one-off setup has been done by running the following in the HWA project folder:

```shell
cd docker
docker-compose up -d
cd ..
```

On a new, empty HAPI database, and after pulling HWA changes that add migrations, run `alembic upgrade head` in the HWA container before running the project (see [Database migrations (alembic)](#database-migrations-alembic)):

```shell
cd docker
docker-compose exec -T hwa sh -c "alembic upgrade head"
cd ..
```

In order to run the project, which populates the HAPI database from the patches on GitHub, the environment variables `HWA_PATCH_REPO_URL`, `HWA_PATCH_BRANCH_NAME` and `HWA_PATCH_TOKEN` need to be defined. These are specified in `.vscode/launch.json` for VS Code users, which points at `OCHA-DAP/hapi-pipelines`. Its `HWA_PATCH_TOKEN` is empty, so fill it in locally and don't commit it. `HWA_PATCH_TOKEN` should be acquired from GitHub. The project can be run with:

```shell
cd docker
docker-compose exec -T hwa sh -c "python start.py"
cd ..
```

From the command line, `HWA_PATCH_TOKEN` comes from `docker/.env`. `docker-compose.yml` doesn't set `HWA_PATCH_REPO_URL` or `HWA_PATCH_BRANCH_NAME`, so the defaults in `hdx_hwa/config/config.py` apply unless you pass them: the `database/csv` folder (`HWA_PATCH_FOLDER`) on the `db-export` branch of `OCHA-DAP/hdx-hapi-write-app-patches`, a different repo from the one in `launch.json`. To pass them, use for example `docker-compose exec -T -e HWA_PATCH_REPO_URL=<url> -e HWA_PATCH_BRANCH_NAME=<branch> hwa sh -c "python start.py"`. Slack notifications are only sent when `HAPI_SLACK_CENTRE_ACCESS_TOKEN` is set; otherwise they are only logged.

This will discover any new patches in GitHub and apply them to the HAPI database. This can take a number of minutes if the HAPI database is empty.

## Database migrations (alembic)

The migrations in `alembic/versions` create and update the tables defined in hapi-schema. `alembic/env.py` connects to:

- the URL passed with `-x sqlalchemy.url=postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>`, or otherwise
- a URL built from `HAPI_DB_USER`, `HAPI_DB_PASS`, `HAPI_DB_HOST`, `HAPI_DB_PORT` and `HAPI_DB_NAME` (defaults `hapi:hapi@db:5432/hapi`), which `docker-compose.yml` sets in the `hwa` container.

`sqlalchemy.url` in `alembic.ini` is not used.

Don't run `alembic upgrade` or `alembic stamp` against a database that has tables but no `alembic_version` table, such as a HAPI database restored from the hapi-pipelines dump with `restore_database.sh` in `hdx-hapi`. Alembic treats such a database as empty and runs every migration from the start, and stamping records a revision the tables may not match.

When deploying a new HWA version, run `alembic upgrade head` against the HAPI database before the new version processes any patches. The image's `ENTRYPOINT` is in shell form and ignores arguments, so use `docker run --entrypoint alembic <image> upgrade head` with the `HAPI_DB_*` variables set, or `docker exec` into a running container.

## Upgrading dependencies

`pip install --upgrade -r requirements.txt` upgrades the packages that `requirements.txt` lists, but leaves an installed dependency alone while it still meets the requirement. A newly built image installs the latest version of every dependency instead. So a dependency that nothing pins can be older in your container and in CI than in the next image. SQLAlchemy is one: hapi-schema only requires `sqlalchemy`, with no version. To install what a new image would get, add `--upgrade-strategy eager`:

```shell
cd docker
docker-compose exec -T hwa sh -c "pip install --upgrade --upgrade-strategy eager -r requirements.txt"
cd ..
```

## Changing the Dockerfile

CI and the local setup both run the published `:main` image, so CI doesn't build or test a `Dockerfile` change on a branch. `build.yml` first builds it when the change reaches `main`, and pushes it as `:main` straight away. To test it before merging, build the image from the repo root:

```shell
docker build -t public.ecr.aws/unocha/hdx-hapi-write-app:local .
```

Then set `HWA_IMAGE_TAG=local` in `docker/.env`, run `docker-compose --profile=testing up -d` in the `docker` folder to recreate the `hwa` container, and repeat the `apk` and `pip` steps of the one-off setup before running the tests. Remove `HWA_IMAGE_TAG` afterwards to go back to `:main`.

There is no `.dockerignore`, so a local build copies the whole folder into the image, including `docker/.env` with your token and any test database data under `docker/postgres-data`. Don't push a locally built image.

Instead of building locally, you can run the **Create image** workflow (`build.yml`) manually on the branch. It pushes `public.ecr.aws/unocha/hdx-hapi-write-app:<commit SHA>` to the public registry. Use the full commit SHA as `HWA_IMAGE_TAG`.

## Upgrading hapi-schema

1. Change the tag in the `hapi-schema` line of `requirements.txt`. If `requirements.txt` pins `SQLAlchemy`, keep that pin on the same minor version as the one locked in `src/hapi-schema/uv.lock`.
2. Reinstall the requirements in the `hwa` container with `--upgrade-strategy eager` (see [Upgrading dependencies](#upgrading-dependencies)), so that SQLAlchemy is at the version a new image will install. Check the installed version with `git -C src/hapi-schema describe --tags` from the repo root; `pip show hapi-schema` can report an old version for the editable install.
3. Read the new entries in `src/hapi-schema/changelog.md`.
4. Generate the migration against a database at the previous head. Don't use `hwa_test`, because the tests recreate its tables without alembic. For example, with the test database running:

   ```shell
   HAPI_DB_NAME=hwa_migrate ./initialize_db.sh
   cd docker
   docker-compose exec -T hwa sh -c "alembic -x sqlalchemy.url=postgresql+psycopg2://hapi:hapi@db:5432/hwa_migrate upgrade head"
   docker-compose exec -T hwa sh -c "alembic -x sqlalchemy.url=postgresql+psycopg2://hapi:hapi@db:5432/hwa_migrate revision --autogenerate -m 'migrate schema from X to Y'"
   cd ..
   ```

   Always pass `--autogenerate`; without it alembic creates an empty migration.
5. Review the generated `upgrade()` and `downgrade()`. Autogenerate doesn't detect new enum values, so add them by hand with `op.execute("ALTER TYPE ... ADD VALUE ...")` (see `0d68c20a0946_migrate_schema_from_0_8_17_to_0_9_0.py`). A `downgrade()` that re-adds a `NOT NULL` column needs a `server_default`, or it fails on tables that have rows.
6. On the same database, run `alembic -x sqlalchemy.url=... upgrade head` and then `alembic -x sqlalchemy.url=... check`. The check should report `No new upgrade operations detected.`
7. Run the tests and the linter.
8. Bump `HWA_VERSION` in `hdx_hwa/config/version.py`.
9. After merging to `main`, tag that commit with `HWA_VERSION`: a lightweight tag without a `v` prefix (`git tag <version> && git push origin <version>`). `.github/workflows/build.yml` then builds and pushes `public.ecr.aws/unocha/hdx-hapi-write-app:<version>`.

## Continuous integration

- `run-tests.yml` runs on every push. It does the setup and tests above in the published `:main` image with `docker compose`, and uploads coverage to Codecov. It doesn't build the `Dockerfile` (see [Changing the Dockerfile](#changing-the-dockerfile)).
- `run-linter.yml` runs on every push. It installs `dev-requirements.txt` and runs `ruff check`.
- `build.yml` builds and pushes the image on pushes to `dev`, `main` and `prod` (tagged with the branch name), on tags (tagged with the tag), and on manual runs (tagged with the commit SHA).
- The tests need the `HWA_PATCH_TOKEN` secret. Workflows triggered by Dependabot don't get Actions secrets, so set it both under **Settings → Secrets and variables → Actions** and under **Settings → Secrets and variables → Dependabot**.

## Project structure

- `hdx_hwa.config` - everything to do with runtime configuration
- `hdx_hwa.db` - data access layer
  - `hdx_hwa.db.services` - functions, objects that need to be used outside of `hdx_hwa.db`
- `hdx_hwa.engine` - execution engine for a JSON patch
  - `hdx_hwa.engine.services` - functions, objects that need to be used outside of `hdx_hwa.engine`
- `hdx_hwa.patch_repo` - new patch discovery, communication with the patch repo
  - `hdx_hwa.patch_repo.services` - functions, objects that need to be used outside of `hdx_hwa.patch_repo`
- `hdx_hwa.util` - Slack notifications and timing helpers
