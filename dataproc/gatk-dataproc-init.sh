#!/bin/bash

set -exo pipefail

readonly ROLE="$(/usr/share/google/get_metadata_value attributes/dataproc-role)"
readonly PROJECT="$(/usr/share/google/get_metadata_value ../project/project-id)"

SERVICE_ACCOUNT=$(/usr/share/google/get_metadata_value attributes/service_account)
JSON_LOCATION=$(/usr/share/google/get_metadata_value attributes/json_location)
FAIR_SCHEDULER=$(/usr/share/google/get_metadata_value attributes/scheduler)
SCHEDULE_LOCATION=$(/usr/share/google/get_metadata_value attributes/fair_location)

if [[ "${ROLE}" == 'Master' ]]; then
    mkdir /app
    gsutil cp $SERVICE_ACCOUNT $JSON_LOCATION
    gsutil cp $FAIR_SCHEDULER $SCHEDULE_LOCATION
    # Env variables necessary for GCS hadoop connector to be configured properly
    echo 'export HELLBENDER_TEST_PROJECT=$PROJECT' | tee -a /etc/profile
    echo 'export HELLBENDER_JSON_SERVICE_ACCOUNT_KEY=$JSON_LOCATION' | tee -a /etc/profile
    source /etc/profile
    systemctl restart hadoop-yarn-resourcemanager.service
fi

# Download and run the Stackdriver installation script
curl -sSO https://dl.google.com/cloudagents/install-monitoring-agent.sh
sudo bash install-monitoring-agent.sh
