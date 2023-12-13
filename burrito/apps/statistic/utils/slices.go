package utils

func Contains(data []any, targetItem any) bool {
	for _, item := range data {
		if item == targetItem {
			return true
		}
	}

	return false
}
