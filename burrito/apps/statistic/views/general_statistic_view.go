package views

import (
	"BurritoStatistic/models"
	"BurritoStatistic/utils"
	"encoding/json"
	"time"

	"github.com/gofiber/fiber/v2"
)

// @Summary		get general statistic
// @Description	get general statistic
// @Accept			json
// @Produce		json
// @Param			payload	body		models.GeneralStatisticRequest	true	"GeneralStatisticRequest"
// @Success 200 {object} models.GeneralStatisticModel
// @Router /statistic/general [post]
func GetGeneralStatistic(ctx *fiber.Ctx) error {
	tokenPayload := utils.ValidateJWTAndCheckPermission(ctx)
	if tokenPayload == nil {
		return nil
	}

	requestBody := models.GeneralStatisticRequest{}
	ctx.BodyParser(&requestBody)

	if !utils.IsValidGeneralStatisticRequest(&requestBody) {
		requestBody.From = time.Now().Format("2006-01-02")
		requestBody.To = time.Now().AddDate(0, 0, -7).Format("2006-01-02")
	}

	db := utils.GetDatabase()

	var generalStatisticInstance = models.GeneralStatisticModel{}

	db.Table("tickets").Select("COUNT(*)").Count(&generalStatisticInstance.Global.TicketsCount)
	db.Table("tickets t").Select(
		"s.status_id, s.name status_name, COUNT(*) AS count",
	).Joins("JOIN statuses s ON t.status_id = s.status_id").Group("status_id").Find(
		&generalStatisticInstance.Global.Statuses,
	)

	db.Table("tickets t").Select(
		"DATE(t.created) date, s.status_id, s.name status_name, COUNT(*) tickets_count",
	).Joins("JOIN statuses s ON t.status_id = s.status_id").Group("t.status_id, date").Find(
		&generalStatisticInstance.Period,
	)

	statisticResponse, _ := json.Marshal(generalStatisticInstance)
	return ctx.JSON(string(statisticResponse))
}
