# Docker

Purplship's preferred deployment method is using Docker.

## Purplship Server Image

A Purplship Server Image is pushed on dockerhub for each release. 

```bash
docker pull purplship/purplship-server:[version]
```


## Updating Purplship

All you need to do to upgrade Purplship is to restart your Docker server with a new image tag.

We actively maintain the two most recent monthly releases of Purplship.

> The Docker server image tags follow CalVer semantics, so version 2021.5 can be found at purplship/purplship-server:2021.5.
> You can see the full list of tags on our [Docker Hub page](https://hub.docker.com/r/purplship/purplship-server/tags).
