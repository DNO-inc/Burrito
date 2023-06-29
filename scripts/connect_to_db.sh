sed -E -n 's/[^#]+/export &/ p' .env > /dev/null

burrito_db_container_name="burrito_db"
burrito_db_container=$(docker ps | grep $burrito_db_container_name | awk '{print($1)}')

if [ -z "$burrito_db_container" ]
then
      echo $'\n'
      echo "docker container ($burrito_db_container_name) is not running"
      echo $'\n'
else
    clear; docker exec -it $burrito_db_container mysql -u $BURRITO_DB_USER -h$BURRITO_DB_HOST -p$BURRITO_DB_PASSWORD $BURRITO_DB_NAME
fi
