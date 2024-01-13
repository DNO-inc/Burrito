package views

import (
	"BurritoStatistic/models"
	"BurritoStatistic/utils"
	"encoding/json"

	"github.com/gofiber/fiber/v2"
)

// @Summary		get period statistic
// @Description	get period statistic
// @Produce		json
// @Success 200 {object} models.ActivitySummaryModel
// @Router /statistic/activity_summary [get]
func ActivitySummaryView(ctx *fiber.Ctx) error {
	tokenPayload := utils.ValidateJWTAndCheckPermission(ctx)
	if tokenPayload == nil {
		return nil
	}

	db := utils.GetDatabase()

	var activityStatisticInstance = models.ActivitySummaryModel{}

	//TODO: add query to mongodb to receive data about ticket status changing

	db.Raw("SELECT COUNT(*) FROM tickets").Scan(&activityStatisticInstance.TicketsProcessed)
	db.Raw("SELECT COUNT(*) FROM users").Scan(&activityStatisticInstance.UsersRegistered)

	response, _ := json.Marshal(activityStatisticInstance)
	return ctx.JSON(string(response))
}
