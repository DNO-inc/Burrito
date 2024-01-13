package models

type FacultyData struct {
	FacultyID             int64   `json:"faculty_id"`
	Name                  string  `json:"name"`
	RegisteredUsers       int     `json:"registered_users"`
	CreatedTicketsPercent float32 `json:"created_tickets_percent"`
}

type FacultyStatisticModel struct {
	FacultiesData []FacultyData `json:"faculties_data"`
}
