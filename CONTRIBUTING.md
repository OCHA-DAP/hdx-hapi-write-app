# Contributing 

The HAPI Write App (HWA) is being developed by a team from the [Centre for Humanitarian Data](https://centre.humdata.org/).

HDX developers are using [VS Code](https://code.visualstudio.com/) as a standard IDE for this project with development taking place inside Docker containers.

## Notes:
For **development purposes** the project assumes that the HAPI stack is running. Or more precisely the HAPI db container.
One can see that the [Docker Compose configuration](https://github.com/OCHA-DAP/hdx-hapi-write-app/blob/cc75b0c567fd40016e37a4599942e8c8769bdb24/docker/docker-compose.yml#L40) 
refers to the network `hapi_stack_hapi`. 
In this way, any change to the database will be reflected in the locally running HAPI API endpoints.

For **testing purposes** there is a test database container that can be started. 
It's only meant to start under the [testing profile](https://github.com/OCHA-DAP/hdx-hapi-write-app/blob/cc75b0c567fd40016e37a4599942e8c8769bdb24/docker/docker-compose.yml#L35).
`docker-compose --profile=testing up -d`


## Starting the project:
First start the HAPI project. So run the following in the HAPI project folder:

```shell
cd docker
docker-compose start
```
Then spin up the HWA project. So run the following in the HWA project folder:

```shell
cd docker
docker-compose up -d
docker-compose exec -T hwa sh -c "apk add git"
docker-compose exec -T hwa sh -c "pip install --upgrade -r requirements.txt"
docker-compose exec -T hwa sh -c "pip install --upgrade -r dev-requirements.txt"
cd ..
```

In order to run the project, which populates the HAPI database from the patches on GitHub, the environment variables `HWA_PATCH_REPO_URL`, `HWA_PATCH_BRANCH_NAME` and `HWA_PATCH_TOKEN` need to be defined. These are specified in `launch.json` for Visual Code users. `HWA_PATCH_TOKEN` should be acquired from GitHub. 
```shell
cd docker
docker-compose exec -T hwa sh -c "python start.py"
cd ..
```

If one also wants to run the tests:
```shell
./initialize_test_db.sh
cd docker
docker-compose exec -T hwa sh -c "pytest --log-level=INFO"
cd ..
```

## Project structure
-  `hdx_hwa.config` - everything to do with runtime configuration
-  `hdx_hwa.db` - data access layer
   -  `hdx_hwa.db.services` - functions, objects that need to be used outside of `hdx_hwa.db`
-  `hdx_hwa.engine` - execution engine for a JSON patch
   -  `hdx_hwa.engine.services` - functions, objects that need to be used outside of `hdx_hwa.engine`
-  `hdx_hwa.patch_repo` - new patch discovery, communication with the patch repo
   -  `hdx_hwa.patch_repo.services` - functions, objects that need to be used outside of `hdx_hwa.patch_repo`