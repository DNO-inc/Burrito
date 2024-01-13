package models

type PeriodStatisticRequest struct {
	From string `json:"from"`
	To   string `json:"to"`
}

type PeriodStatisticModel struct {
	ByStatuses []struct {
		Date         string `json:"date"`
		StatusID     int    `json:"status_id"`
		StatusName   string `json:"status_name"`
		TicketsCount int64  `json:"tickets_count"`
	} `json:"statuses"`

	ByScopes []struct {
		Date         string `json:"date"`
		Scope        string `json:"scope"`
		TicketsCount int64  `json:"tickets_count"`
	} `json:"scopes"`
}
