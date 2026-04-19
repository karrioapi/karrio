# karrio.server (consolidated modules)

This package consolidates the three OSS core server modules of the
[karrio](https://pypi.org/project/karrio.server) universal shipping API
into a single namespace-package install:

- `karrio.server.core` (formerly `modules/core`)
- `karrio.server.graph` (formerly `modules/graph`)
- `karrio.server.admin` (formerly `modules/admin`)

The distributions `karrio_server_core`, `karrio_server_graph`, and
`karrio_server_admin` are still published for one release cycle as thin
shim packages that depend on this package. Import paths
(`karrio.server.core.*`, `karrio.server.graph.*`, `karrio.server.admin.*`)
continue to resolve unchanged.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.server.modules
```

Check the [karrio docs](https://docs.karrio.io) to get started.
