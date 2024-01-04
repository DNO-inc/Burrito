package app

import (
	"BurritoStatistic/utils"
	"sync"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
)

var appInstance *fiber.App
var once sync.Once

func configureApp() *fiber.App {
	app := fiber.New()

	app.Use(logger.New(logger.Config{
		Format: "[${time}] | [${ip}]:${port} ${status} - ${method} ${path}\n",
	}))

	app.Use(cors.New(cors.Config{
		AllowHeaders:     "Origin,Content-Type,Accept,Content-Length,Accept-Language,Accept-Encoding,Connection,Access-Control-Allow-Origin",
		AllowOrigins:     "*",
		AllowCredentials: true,
		AllowMethods:     "GET,POST,HEAD,PUT,DELETE,OPTIONS",
	}))

	app.Use(cors.New(cors.Config{
		AllowHeaders:     "Origin,Content-Type,Accept,Content-Length,Accept-Language,Accept-Encoding,Connection,Access-Control-Allow-Origin",
		AllowOrigins:     "*",
		AllowCredentials: true,
		AllowMethods:     "GET,POST,HEAD,PUT,DELETE,OPTIONS",
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
