# Contributing 

The HAPI Write App (HWA) is being developed by a team from the [Centre for Humanitarian Data](https://centre.humdata.org/).

HDX developers are using [VS Code](https://code.visualstudio.com/) as a standard IDE for this project with development taking place inside Docker containers.

## One-off container creation activities

There is a test database container that can be started without the HAPI stack which needs to be created in one-off setup. It's only meant to start under the [testing profile](https://github.com/OCHA-DAP/hdx-hapi-write-app/blob/cc75b0c567fd40016e37a4599942e8c8769bdb24/docker/docker-compose.yml#L35)

To create the HWA stack containers in the first instance, including a test database container:

```shell
docker network create -d bridge hapi_stack_hapi
cd docker
docker-compose --profile=testing up -d
docker-compose exec -T hwa sh -c "apk add git"
docker-compose exec -T hwa sh -c "pip install --upgrade -r requirements.txt"
docker-compose exec -T hwa sh -c "pip install --upgrade -r dev-requirements.txt"
cd ..
./initialize_test_db.sh
```

## Working on HWA for testing

Once the one-off container creation activities have been done then future testing sessions are started as follows:

```shell
cd docker
docker-compose --profile=testing up -d
cd ..
./initialize_test_db.sh
```

Tests can be executed using the following commandline or the Visual Code test runner.
```shell
docker-compose exec -T hwa sh -c "pytest --log-level=INFO"
```

## Working on HWA for HAPI

For HAPI development purposes the project assumes that the HAPI stack is running. Or more precisely the HAPI db container.
One can see that the [Docker Compose configuration](https://github.com/OCHA-DAP/hdx-hapi-write-app/blob/cc75b0c567fd40016e37a4599942e8c8769bdb24/docker/docker-compose.yml#L40) 
refers to the network `hapi_stack_hapi`. 
In this way, any change to the database will be reflected in the locally running HAPI API endpoints.

First start the HAPI project. So run the following in the HAPI project folder:

```shell
cd docker
docker-compose start
cd ..
./initialize_db.sh
```
The `./initialize_db.sh` script should be run in the `hdx-hapi` repo. Next spin up the HWA project, assuming that the one-off setup has been done by running the following in the HWA project folder:

```shell
cd docker
docker-compose up -d
cd ..
```

Inside the HWA docker container it may be necessary to run `alembic upgrade head`.

In order to run the project, which populates the HAPI database from the patches on GitHub, the environment variables `HWA_PATCH_REPO_URL`, `HWA_PATCH_BRANCH_NAME` and `HWA_PATCH_TOKEN` need to be defined. These are specified in `launch.json` for Visual Code users. `HWA_PATCH_TOKEN` should be acquired from GitHub. The project can be run with: 
```shell
cd docker
docker-compose exec -T hwa sh -c "python start.py"
cd ..
```
This will discover any new patches in GitHub and apply them to the HAPI database, this can take a number of minutes if the HAPI database is empty.

## Project structure
-  `hdx_hwa.config` - everything to do with runtime configuration
-  `hdx_hwa.db` - data access layer
   -  `hdx_hwa.db.services` - functions, objects that need to be used outside of `hdx_hwa.db`
-  `hdx_hwa.engine` - execution engine for a JSON patch
   -  `hdx_hwa.engine.services` - functions, objects that need to be used outside of `hdx_hwa.engine`
-  `hdx_hwa.patch_repo` - new patch discovery, communication with the patch repo
   -  `hdx_hwa.patch_repo.services` - functions, objects that need to be used outside of `hdx_hwa.patch_repo`