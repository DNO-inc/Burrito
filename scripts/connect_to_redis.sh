sed -E -n 's/[^#]+/export &/ p' .env > /dev/null

burrito_redis_container_name="burrito_redis"
burrito_redis_container=$(docker ps | grep $burrito_redis_container_name | awk '{print($1)}')

if [ -z "$burrito_redis_container" ]
then
      echo $'\n'
      echo "docker container ($burrito_redis_container_name) is not running"
      echo $'\n'
else
    clear; docker exec -it $burrito_redis_container redis-cli
fi
