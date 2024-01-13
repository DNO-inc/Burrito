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
	app.Get("/statistic/activity_summary", views.ActivitySummaryView)
	app.Get("/statistic/faculties", views.FacultyStatisticView)
	app.Get("/statistic/docs/*", swagger.HandlerDefault)
}
