package app

import "github.com/gofiber/fiber/v2"

// this routes created without subapps or groups cause this app is aimed to be simple
// it will contain less than 10 endpoints
func ConnectRoutes(app *fiber.App) {
	app.Post("/statistic/profile", GetProfileStatistic)
	app.Get("/statistic/ticket", GetTicketStatistic)
}
