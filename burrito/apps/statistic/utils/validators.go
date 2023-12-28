package utils

import "BurritoStatistic/models"

func IsValidGeneralStatisticRequest(data *models.GeneralStatisticRequest) bool {
	return IsValidDate(data.From) && IsValidDate(data.To)
}
