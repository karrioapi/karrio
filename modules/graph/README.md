# karrio.server.graph (shim)

Starting with 2026.5.0 the source code previously packaged as
`karrio_server_graph` lives in `karrio_server_modules` (directory
`modules/server/`). This package is now a thin shim that depends on
`karrio_server_modules` to preserve backwards compatibility for pinned
installs (`pip install karrio-server-graph==...`) for one release cycle.

Import paths are unchanged: `karrio.server.graph.*` continues to resolve
from the consolidated `modules/server/karrio/server/graph/` tree.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.server.graph
```

Check the [karrio docs](https://docs.karrio.io) to get started.
