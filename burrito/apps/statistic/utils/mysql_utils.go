package utils

import (
	"fmt"
	"sync"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var dsn string = "%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local"
var db *gorm.DB = nil

func GetDatabase() *gorm.DB {
	var once sync.Once
	once.Do(func() {
		db, _ = gorm.Open(
			mysql.Open(
				fmt.Sprintf(
					dsn,
					GetConfig().MYSQL_USER,
					GetConfig().MYSQL_PASSWORD,
					GetConfig().DB_HOST,
					GetConfig().DB_PORT,
					GetConfig().MYSQL_DATABASE,
				),
			),
			&gorm.Config{},
		)
	})
	return db
}
