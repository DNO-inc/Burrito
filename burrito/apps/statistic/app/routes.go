package app

import (
	"BurritoStatistic/views"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/swagger"
)

// this routes created without sub-apps or groups cause this app is aimed to be simple
// it will contain less than 10 endpoints
func ConnectRoutes(app *fiber.App) {
	app.Post("/statistic/general", views.GetGeneralStatistic)
	app.Get("/docs/*", swagger.HandlerDefault)
}
