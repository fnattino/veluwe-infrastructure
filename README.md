# Veluwe Metadata Portal - Infrastructure

Test infrastructure repository for the Veluwe Metadata Portal. It contains materials to deploy a metadata catalogue using [pyscw](https://pycsw.org/) from [metadata control files (MCFs)](https://geopython.github.io/pygeometa/reference/mcf/) hosted in a [a GitHub repository][veluwe-metadata-repo].

In order to get started, clone and access this repository:

```shell
git clone git@github.com:fnattino/veluwe-infrastructure.git
cd veluwe-infrastructure
```

## Local deployment

### Retrieve metadata records

The metadata control files (MCFs) are hosted in a separate GitHub repository (see [veluwe-metadata][veluwe-metadata-repo]), which is a submodule of the current repository. Make sure to fetch the data:

```shell
git submodule update --recursive --remote
```

The MCF files have to be converted to XML (ISO19139 standard) in order to be ingested into the metadata catalogue. This can be done using the provided Python script ([`generate-xml-records.py`](./metadata/generate-xml-records.py), based on [`pygeometa`](https://geopython.github.io/pygeometa/)). Create an environment with the required dependencies and run the script at once using [`uv`](https://docs.astral.sh/uv/):
```shell
uv run ./metadata/generate-xml-records.py -i ./metadata/veluwe-metadata/datasets/ -o metadata/records
```

### Start the metadata catalogue

The metadata catalogue is backed by a PostGIS database. The database credentials and a few other parameters should be defined in a `.env` file, which can be setup by copying and editing the provided template:
```shell
cp .env.template .env
# edit the .env file
```

Start the metadata catalogue using the provided [`docker-compose.yml`](./docker-compose.yml) file:
```shell
docker compose up --detatch
```

The metadata catalogue should be reachable at http://localhost:8000/ .

Import the XML records in the metadata catalog:
```shell
docker exec -it pycsw pycsw-admin.py load-records --config /etc/pycsw/pycsw.yaml --path /metadata --recursive --yes -v DEBUG
```

### Clean up

To remove the running services and destroy the database docker volume:
```shell
docker compose rm
docker volume prune --all
```

## Resources

- [EJPSoil Datahub overview](https://ejpsoil.github.io/ejpsoildatahub/) by Paul van Genuchten
- [EJPSoil Project WIKI](https://ejpsoil.github.io/soildata-assimilation-guidance/) by Paul van Genuchten, in particular:
    - [Overview Metadata & discovery](https://ejpsoil.github.io/soildata-assimilation-guidance/metadata.html);
    - [A pythonic & participatory metadata workflow](https://ejpsoil.github.io/soildata-assimilation-guidance/cookbook/pygeometa.html);

[veluwe-metadata-repo]: https://github.com/fnattino/veluwe-metadata

