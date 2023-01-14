#!/usr/bin/env bash

# Source environment variables
source "bin/_env.sh"

echo 'run server tests...'
karrio test --failfast karrio.server.proxy.tests &&
karrio test --failfast karrio.server.pricing.tests &&
karrio test --failfast karrio.server.manager.tests &&
karrio test --failfast karrio.server.events.tests &&
karrio test --failfast karrio.server.graph.tests &&
karrio test --failfast karrio.server.orders.tests &&

if [[ "$*" != *--cloud* ]];
then
    echo "done..."
else
    karrio test --failfast karrio.server.orgs.tests
fi
