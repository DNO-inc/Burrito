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
// @Param			payload	body		models.PeriodStatisticRequest	true	"PeriodStatisticRequest"
// @Success 200 {object} models.PeriodStatisticModel
// @Router /statistic/period [post]
func PeriodStatisticView(ctx *fiber.Ctx) error {
	tokenPayload := utils.ValidateJWTAndCheckPermission(ctx)
	if tokenPayload == nil {
		return nil
	}

	requestBody := models.PeriodStatisticRequest{}
	ctx.BodyParser(&requestBody)

	if !utils.IsValidPeriodStatisticRequest(&requestBody) {
		requestBody.From = time.Now().Format("2006-01-02")
		requestBody.To = time.Now().AddDate(0, 0, -7).Format("2006-01-02")
	}

	db := utils.GetDatabase()

	var periodStatisticInstance = models.PeriodStatisticModel{}

	db.Raw(`
		SELECT 
			DATE(t.created) date, s.status_id, s.name status_name, COUNT(*) tickets_count
		FROM tickets t 
		JOIN statuses s ON t.status_id = s.status_id
		GROUP BY t.status_id, date
	`).Scan(&periodStatisticInstance.ByStatuses)

	db.Raw(`
		SELECT 
			DATE(t.created) date, q.scope scope, COUNT(*) tickets_count
		FROM tickets t 
		JOIN queues q ON t.queue_id  = q.queue_id 
		GROUP BY q.scope, date
	`).Scan(&periodStatisticInstance.ByScopes)

	statisticResponse, _ := json.Marshal(periodStatisticInstance)
	return ctx.SendString(string(statisticResponse))
}
