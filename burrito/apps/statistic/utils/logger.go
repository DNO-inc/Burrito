package utils

import (
	"log"
	"os"
	"sync"
)

const LOGGER_FLAGS = log.Ldate | log.Ltime | log.Lmsgprefix

type BurritoLogger struct {
}

func (bLogger *BurritoLogger) Debug(message ...any) {
	log.New(os.Stderr, "DEBUG: ", LOGGER_FLAGS).Println(message...)
}

func (bLogger *BurritoLogger) Info(message ...any) {
	log.New(os.Stderr, "Info: ", LOGGER_FLAGS).Println(message...)
}

func (bLogger *BurritoLogger) Warning(message ...any) {
	log.New(os.Stderr, "Warning: ", LOGGER_FLAGS).Println(message...)
}

func (bLogger *BurritoLogger) Error(message ...any) {
	log.New(os.Stderr, "Error: ", LOGGER_FLAGS).Println(message...)
}

func (bLogger *BurritoLogger) Critical(message ...any) {
	log.New(os.Stderr, "Critical: ", LOGGER_FLAGS).Println(message...)
}

var loggerInstance *BurritoLogger = nil
var once sync.Once

func GetLogger() *BurritoLogger {
	once.Do(
		func() {
			loggerInstance = &BurritoLogger{}
		},
	)
	return loggerInstance
}
