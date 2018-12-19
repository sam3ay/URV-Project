#!/bin/bash

set -exo pipefail

readonly ROLE="$(/usr/share/google/get_metadata_value attributes/dataproc-role)"
readonly PROJECT="$(/usr/share/google/get_metadata_value ../project/project-id)"

SERVICE_ACCOUNT=$(/usr/share/google/get_metadata_value attributes/service_account)
JSON_LOCATION=$(/usr/share/google/get_metadata_value attributes/json_location)
FAIR_SCHEDULER=$(/usr/share/google/get_metadata_value attributes/scheduler)
SCHEDULER_LOCATION=$(/usr/share/google/get_metadata_value attributes/schedule_location)

if [[ "${ROLE}" == 'Master' ]]; then
    # edit the yarn-site.xml to point to fair scheduler location
    mkdir -p ${JSON_LOCATION%/*}
    mkdir -p ${SCHEDULER_LOCATION%/*}
    gsutil cp $SERVICE_ACCOUNT $JSON_LOCATION
    gsutil cp $FAIR_SCHEDULER $SCHEDULER_LOCATION
    # Env variables necessary for GCS hadoop connector to be configured properly
    echo 'export HELLBENDER_TEST_PROJECT=$PROJECT' | tee -a /etc/profile
    echo 'export HELLBENDER_JSON_SERVICE_ACCOUNT_KEY=$JSON_LOCATION' | tee -a /etc/profile
    # Necessary for correct settings on cluster configuration
    #echo 'export HADOOP_CONF_DIR=${SCHEDULER_LOCATION%/*}' | tee -a /etc/profile
    source /etc/profile

    sed -i '$ d' /etc/hadoop/conf/yarn-site.xml

    echo "  <property>" >> /etc/hadoop/conf/yarn-site.xml
    echo "    <name>yarn.scheduler.fair.allocation.file</name>" >> /etc/hadoop/conf/yarn-site.xml
    echo "    <value>${SCHEDULER_LOCATION}</value>" >> /etc/hadoop/conf/yarn-site.xml
    echo "  </property>" >> /etc/hadoop/conf/yarn-site.xml
    echo "</configuration>" >> /etc/hadoop/conf/yarn-site.xml
    systemctl restart hadoop-yarn-resourcemanager.service
fi

# Download and run the Stackdriver installation script
curl -sSO https://dl.google.com/cloudagents/install-monitoring-agent.sh
sudo bash install-monitoring-agent.sh
