package models

type TicketStatusCount struct {
	StatusID int `json:"status_id"`
	Count    int `json:"count"`
}

type GeneralStatisticModel struct {
	TicketsCount int64               `json:"tickets_count"`
	Statuses     []TicketStatusCount `json:"statuses"`
}
