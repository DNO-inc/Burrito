package utils

import (
	"fmt"
	"sync"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var dsn string = "%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local"
var db *gorm.DB = nil
var mysqlOnce sync.Once

func GetDatabase() *gorm.DB {
	mysqlOnce.Do(func() {
		db, _ = gorm.Open(
			mysql.Open(
				fmt.Sprintf(
					dsn,
					GetConfig().DB_USER,
					GetConfig().DB_PASSWORD,
					GetConfig().DB_HOST,
					GetConfig().DB_PORT,
					GetConfig().DB_NAME,
				),
			),
			&gorm.Config{},
		)

		sqlDB, _ := db.DB()
		sqlDB.SetMaxIdleConns(10)
		sqlDB.SetMaxOpenConns(50)
	})
	return db
}

func CheckForAdmin(user_id int) bool {
	var priority int
	GetDatabase().Raw("SELECT priority FROM roles r JOIN users u USING(role_id) WHERE user_id = ?", user_id).Scan(&priority)
	return priority >= 90
}
