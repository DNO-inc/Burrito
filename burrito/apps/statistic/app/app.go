package app

import (
	"BurritoStatistic/utils"
	"sync"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
)

var appInstance *fiber.App
var once sync.Once

func configureApp() *fiber.App {
	app := fiber.New()

	app.Use(logger.New(logger.Config{
		Format: "[${ip}]:${port} ${status} - ${method} ${path}\n",
	}))

	ConnectRoutes(app)

	return app
}

func GetApp() *fiber.App {
	once.Do(
		func() {
			appInstance = configureApp()
		},
	)

	if appInstance == nil {
		utils.GetLogger().Critical("App creation failed...")
		return nil
	}
	utils.GetLogger().Info("App has been created successfully")

	return appInstance
}
