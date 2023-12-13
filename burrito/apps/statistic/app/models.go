package app

type UserIDSchema struct {
	UserID int `json:"user_id"`
}

type TicketIDSchema struct {
	TicketID int `json:"ticket_id"`
}

type TicketStatusCount struct {
	StatusID int `json:"status_id"`
	Count    int `json:"count"`
}

type ProfileStatisticOutput struct {
	UserID          int                 `json:"user_id"`
	Statuses        []TicketStatusCount `json:"statuses"`
	TicketsCreated  int                 `json:"tickets_created"`
	CommentsCreated int                 `json:"comments_created"`
}
