package app

import (
	"BurritoStatistic/utils"
	"encoding/json"

	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// show statistic related to determined profile
func GetProfileStatistic(ctx *fiber.Ctx) error {
	payload := UserIDSchema{}
	if err := ctx.BodyParser(&payload); err != nil {
		return err
	}

	// setup mongo context and client
	mongoCtx, cancel := utils.MongoCreateContext()
	defer cancel()
	client := utils.MongoCreateClient(&mongoCtx)

	// get data from mongodb
	commentsFilter := bson.D{
		primitive.E{Key: "user_id", Value: payload.UserID},
		primitive.E{Key: "type_", Value: "comment"},
	}
	collection := client.Database("burrito").Collection("ticket_history")
	commentsCount, err := collection.CountDocuments(mongoCtx, commentsFilter)
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
