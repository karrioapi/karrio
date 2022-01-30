#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

echo 'run server tests...'
purplship test --failfast purplship.server.proxy.tests &&
purplship test --failfast purplship.server.pricing.tests &&
purplship test --failfast purplship.server.manager.tests &&
purplship test --failfast purplship.server.events.tests &&
purplship test --failfast purplship.server.graph.tests &&

if [[ "$*" != *--insiders* ]];
then
    echo "done..."
else
    purplship test --failfast purplship.server.orgs.tests &&
    purplship test --failfast purplship.server.orders.tests
fi
