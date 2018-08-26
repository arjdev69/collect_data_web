docker build \
    --build-arg HOST_UID=$(id -u) \
    --build-arg HOST_GID=$(id -g) \
    -t arjaraujo/collect-data-crawlers:data .

docker commit $(docker ps -l -q) arjaraujo/collect-data-crawlers:data
