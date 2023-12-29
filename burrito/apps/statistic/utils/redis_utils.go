package utils

import (
	"context"
	"fmt"
	"sync"

	"github.com/redis/go-redis/v9"
)

var redisOptions *redis.Options
var redisOnce sync.Once

func getRedisOptions() *redis.Options {
	redisOnce.Do(func() {
		var redisURL = "redis://%s:%d/0" //"redis://%s:%s@%s:%d/0"
		options, err := redis.ParseURL(
			fmt.Sprintf(
				redisURL,
				//				GetConfig().REDIS_USER,
				//				GetConfig().REDIS_PASSWORD,
				GetConfig().REDIS_HOST,
				GetConfig().REDIS_PORT,
			),
		)
		if err != nil {
			GetLogger().Critical("Failed to connect to redis")
		}
		redisOptions = options
	})

	return redisOptions
}

func GetRedisClient() *redis.Client {
	client := redis.NewClient(getRedisOptions())
	return client
}

func RedisGetByKey(key string) string {
	ctx := context.Background()
	value, err := GetRedisClient().Get(ctx, key).Result()
	if err != nil {
		return ""
	}
	return value
}
