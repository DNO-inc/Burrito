package utils

import "BurritoStatistic/models"

func IsValidPeriodStatisticRequest(data *models.PeriodStatisticRequest) bool {
	return IsValidDate(data.From) && IsValidDate(data.To)
}
