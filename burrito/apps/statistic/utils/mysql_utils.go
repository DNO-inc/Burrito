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

var adminRoles = []any{9, 10}

type userAdminData struct {
	RoleID int `json:"role_id"`
}

func CheckForAdmin(user_id int) bool {
	var userMetaData userAdminData
	userMetaData.RoleID = -1
	GetDatabase().Table("users").Select("role_id").Where("user_id = ?", user_id).Find(&userMetaData)
	fmt.Println(user_id, userMetaData.RoleID)
	return Contains(adminRoles, userMetaData.RoleID)
}
