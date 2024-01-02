package main

import (
	"BurritoStatistic/app"
	_ "BurritoStatistic/docs"
)

// @title BurritoStatistic
// @version 1.0
// @description This is an app to provide with a statistic information
func main() {
	app := app.GetApp()

	panic(app.Listen(":8080"))
}
