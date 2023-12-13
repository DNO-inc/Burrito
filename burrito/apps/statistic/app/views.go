package app

import (
	"BurritoStatistic/utils"
	"encoding/json"

	"github.com/gofiber/fiber/v2"
)

// show statistic related to determined profile
func GetProfileStatistic(ctx *fiber.Ctx) error {
	// get access token or return an error if the token is invalid or was not provided
	accessToken, err := utils.GetClearJWT(ctx.GetReqHeaders()["Authorization"])
	if err != nil {
		responseObject, _ := json.Marshal(JsonResponse{Detail: err.Error()})

		ctx.SendStatus(403)
		return ctx.SendString(string(responseObject))
	}

	// read payload from the token
	accessTokenPayload := utils.GetTokenPayload(accessToken)

	// return an error if current user's role is not ADMIN or CHIEF_ADMIN
	if !utils.CheckForAdmin(accessTokenPayload.UserID) {
		responseObject, _ := json.Marshal(JsonResponse{Detail: "Is not allowed to interact with this resource"})
		ctx.SendStatus(403)
		return ctx.SendString(string(responseObject))
	}

	payload := UserIDSchema{}
	if err := ctx.BodyParser(&payload); err != nil {
		return err
	}

	// setup mongo context and client
	mongoCtx, cancel := utils.MongoCreateContext()
	defer cancel()
	client := utils.MongoCreateClient(&mongoCtx)

	// get data from mongodb
	collection := client.Database("burrito").Collection("ticket_history")
	commentsCount, err := collection.CountDocuments(mongoCtx, utils.MapToMongoFilters(
		map[string]any{
			"user_id": payload.UserID,
			"type_":   "comment",
		},
	))
	if err != nil {
		utils.GetLogger().Critical(err)
	}

	// setup MySQL client
	db := utils.GetDatabase()

	var ticketStatuses []TicketStatusCount
	db.Table("tickets").Select("status_id, COUNT(*) count").Where("creator_id = ?", payload.UserID).Group("status_id").Find(&ticketStatuses)

	var ticketsCreated int
	for _, item := range ticketStatuses {
		ticketsCreated += item.Count
	}

	resultJson, _ := json.Marshal(
		ProfileStatisticOutput{
			UserID:          payload.UserID,
			Statuses:        ticketStatuses,
			TicketsCreated:  ticketsCreated,
			CommentsCreated: int(commentsCount),
		},
	)

	return ctx.JSON(string(resultJson))
}

// show statistic related to determined ticket
func GetTicketStatistic(ctx *fiber.Ctx) error {
	payload := TicketIDSchema{}
	if err := ctx.BodyParser(&payload); err != nil {
		return err
	}

	return ctx.SendString("ticket statistic")
}
