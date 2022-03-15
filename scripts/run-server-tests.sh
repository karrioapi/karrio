#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

echo 'run server tests...'
karrio test --failfast karrio.server.proxy.tests &&
karrio test --failfast karrio.server.pricing.tests &&
karrio test --failfast karrio.server.manager.tests &&
karrio test --failfast karrio.server.events.tests &&
karrio test --failfast karrio.server.graph.tests &&

if [[ "$*" != *--insiders* ]];
then
    echo "done..."
else
    karrio test --failfast karrio.server.orgs.tests &&
    karrio test --failfast karrio.server.orders.tests
fi
