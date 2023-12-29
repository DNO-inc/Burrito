package main

import (
	"BurritoStatistic/app"
)

func main() {
	app := app.GetApp()

	panic(app.Listen(":8080"))
}
