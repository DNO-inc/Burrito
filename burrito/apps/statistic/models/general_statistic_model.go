package models

type TicketStatusCount struct {
	StatusID   int    `json:"status_id"`
	StatusName string `json:"status_name"`
	Count      int    `json:"count"`
}

type GeneralStatisticModel struct {
	Global struct {
		TicketsCount int64               `json:"tickets_count"`
		Statuses     []TicketStatusCount `json:"statuses"`
	} `json:"global"`

	Period []struct {
		Date         string `json:"date"`
		StatusID     int    `json:"status_id"`
		StatusName   string `json:"status_name"`
		TicketsCount int64  `json:"tickets_count"`
	} `json:"period"`
}
