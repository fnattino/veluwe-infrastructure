# Veluwe Metadata Catalogue Service for the Web (CSW) - Infrastructure

> [!WARNING]
> At the current stage, the material in this repository is purely explorative.

This is the infrastructure repository hosting material to deploy a metadata catalogue for the [Veluwe Metadata Portal](https://lter-life-experience.org/veluwesearch/) using [pyscw](https://pycsw.org/). The catalogue uses records stored as [metadata control files (MCFs)](https://geopython.github.io/pygeometa/reference/mcf/) in a separate [GitHub repository][veluwe-metadata-repo].

In order to get started, clone and access this repository:

```shell
git clone git@github.com:fnattino/veluwe-infrastructure.git
cd veluwe-infrastructure
```

## Local deployment

### Retrieve metadata records

The metadata control files (MCFs) are hosted in a separate GitHub repository (see [veluwe-metadata][veluwe-metadata-repo]), which is a submodule of the current repository. Make sure to fetch its data:

```shell
git submodule update --init --recursive --remote
```

The MCF files have to be converted to XML (ISO19139 standard) in order to be ingested into the metadata catalogue. This can be done using the provided Python script ([`generate-xml-records.py`](./metadata/scripts/generate-xml-records.py), based on [`pygeometa`](https://geopython.github.io/pygeometa/)). Create an environment with the required dependencies and run the script at once using [`uv`](https://docs.astral.sh/uv/):
```shell
uv run ./metadata/scripts/generate-xml-records.py -i ./metadata/veluwe-metadata/datasets/ -o metadata/records
```

### Start the metadata catalogue

The metadata catalogue is backed by a PostGIS database. The database credentials and a few other parameters should be defined in a `.env` file, which can be set up by copying and editing the provided template:
```shell
cp .env.template .env
# edit the .env file
```

Start the metadata catalogue using the provided [`docker-compose.yml`](./docker-compose.yml) file:
```shell
docker compose up --detach
```

The metadata catalogue should be reachable at http://localhost:8000/ .

### Ingest metadata records

Import the XML records in the metadata catalogue:
```shell
docker exec -it pycsw pycsw-admin.py load-records --config /etc/pycsw/pycsw.yaml --path /metadata --recursive --yes -v DEBUG
```

### Clean up

To remove the running services and destroy the database docker volume:
```shell
docker compose rm --stop --force
docker volume prune --all --force
```

## Resources

- [EJPSoil Datahub overview](https://ejpsoil.github.io/ejpsoildatahub/) by Paul van Genuchten
- [EJPSoil Project WIKI](https://ejpsoil.github.io/soildata-assimilation-guidance/) by Paul van Genuchten, in particular:
    - [Overview Metadata & discovery](https://ejpsoil.github.io/soildata-assimilation-guidance/metadata.html);
    - [A pythonic & participatory metadata workflow](https://ejpsoil.github.io/soildata-assimilation-guidance/cookbook/pygeometa.html);

[veluwe-metadata-repo]: https://github.com/fnattino/veluwe-metadata

