package models

type ActivitySummaryModel struct {
	AverageProcessTime float32 `json:"average_process_time"`
	TicketsProcessed   int64   `json:"tickets_processed"`
	UsersRegistered    int64   `json:"users_registered"`
}
