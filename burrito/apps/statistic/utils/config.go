package utils

import (
	"sync"

	"github.com/caarlos0/env"
	"github.com/joho/godotenv"
)

type Config struct {
	DB_HOST string `env:"BURRITO_DB_HOST,required"`
	DB_PORT int    `env:"BURRITO_DB_PORT,required"`

	MYSQL_ROOT_PASSWORD string `env:"MYSQL_ROOT_PASSWORD,required"`
	MYSQL_DATABASE      string `env:"MYSQL_DATABASE,required"`
	MYSQL_USER          string `env:"MYSQL_USER,required"`
	MYSQL_PASSWORD      string `env:"MYSQL_PASSWORD,required"`

	REDIS_HOST     string `env:"BURRITO_REDIS_HOST,required"`
	REDIS_PORT     int    `env:"BURRITO_REDIS_PORT,required"`
	REDIS_USER     string `env:"BURRITO_REDIS_USER,required"`
	REDIS_PASSWORD string `env:"BURRITO_REDIS_PASSWORD,required"`

	MONGO_HOST     string `env:"BURRITO_MONGO_HOST,required"`
	MONGO_PORT     int    `env:"BURRITO_MONGO_PORT,required"`
	MONGO_DB       string `env:"BURRITO_MONGO_DB,required"`
	MONGO_USER     string `env:"BURRITO_MONGO_USER,required"`
	MONGO_PASSWORD string `env:"BURRITO_MONGO_PASSWORD,required"`

	MONGO_INITDB_ROOT_USERNAME string `env:"MONGO_INITDB_ROOT_USERNAME,required"`
	MONGO_INITDB_ROOT_PASSWORD string `env:"MONGO_INITDB_ROOT_PASSWORD,required"`

	JWT_SECRET string `env:"BURRITO_JWT_SECRET,required"`
}

var config *Config = nil
var configOnce sync.Once

func GetConfig() *Config {
	configOnce.Do(func() {
		err := godotenv.Load()
		if err != nil {
			GetLogger().Error(err)
		}

		config = &Config{}
		if err := env.Parse(config); err != nil {
			GetLogger().Error(err)
		}
	})
	return config
}
