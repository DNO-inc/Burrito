package main

import (
	"BurritoStatistic/app"
)

func main() {
	app := app.GetApp()

	app.Listen(":8080")
}
