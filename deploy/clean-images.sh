docker images | grep '<none>' |  awk '{ print $3 }' | xargs -r docker rmi
