package views

import (
	"BurritoStatistic/models"
	"BurritoStatistic/utils"
	"encoding/json"

	"github.com/gofiber/fiber/v2"
)

const facultyStatisticQuery = `
SELECT 
    u.faculty_id faculty_id
    , f.name name
    , COUNT(u.user_id) registered_users
    , (SELECT FORMAT((COUNT(*) * 100 / (SELECT COUNT(*) FROM tickets)), 2) FROM tickets WHERE faculty_id = f.faculty_id GROUP BY faculty_id) created_tickets_percent
FROM users u
JOIN faculties f ON u.faculty_id = f.faculty_id
GROUP BY u.faculty_id
`

// @Summary		get faculty statistic
// @Description	get faculty statistic
// @Produce		json
// @Success 200 {object} models.FacultyStatisticModel
// @Router /statistic/faculty [get]
func FacultyStatisticView(ctx *fiber.Ctx) error {
	tokenPayload := utils.ValidateJWTAndCheckPermission(ctx)
	if tokenPayload == nil {
		return nil
	}

	db := utils.GetDatabase()

	var facultyStatisticInstance = models.FacultyStatisticModel{}

	db.Raw(facultyStatisticQuery).Scan(&facultyStatisticInstance.FacultiesData)

	response, _ := json.Marshal(facultyStatisticInstance)
	return ctx.SendString(string(response))
}
