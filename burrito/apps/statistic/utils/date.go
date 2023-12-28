package utils

import "time"

func IsValidDate(stringDate string) bool {
	_, err := time.Parse("2006-01-02", stringDate)
	return err == nil
}
