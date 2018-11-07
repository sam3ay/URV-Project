#!/bin/bash

set -euxo pipefail

readonly PROJECT="$(/usr/share/google/get_metadata_value ../project/project-id)"

SERVICE_ACCOUNT=$(/usr/share/google/get_metadata_value attributes)

# Env variables necessary for GCS hadoop connector to be configured properly
# Run on 'Master' and 'Worker' nodes
# readonly ROLE="$(/usr/share/google/get_metadata_value attributes/dataproc-role)"
echo 'export HELLBENDER_TEST_PROJECT=$PROJECT' | tee -a /etc/*bashrc
echo 'export HELLBENDER_JSON_SERVICE_ACCOUNT_KEY=$SERVICE_ACCOUNT' | tee -a /etc/*bashrc
