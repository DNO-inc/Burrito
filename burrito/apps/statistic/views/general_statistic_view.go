package views

import (
	"BurritoStatistic/models"
	"BurritoStatistic/utils"
	"encoding/json"

	"github.com/gofiber/fiber/v2"
)

func GetGeneralStatistic(ctx *fiber.Ctx) error {
	tokenPayload := utils.ValidateJWTAndCheckPermission(ctx)
	if tokenPayload == nil {
		return nil
	}

	db := utils.GetDatabase()

	var generalStatisticInstance = models.GeneralStatisticModel{}

	db.Table("tickets").Select("COUNT(*)").Count(&generalStatisticInstance.TicketsCount)
	db.Table("tickets").Select("status_id, COUNT(*) AS count").Group("status_id").Find(&generalStatisticInstance.Statuses)

	statisticResponse, _ := json.Marshal(generalStatisticInstance)
	return ctx.JSON(string(statisticResponse))
}
