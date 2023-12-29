package utils

import (
	"BurritoStatistic/models"
	"encoding/json"
	"errors"
	"fmt"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt"
	"github.com/mitchellh/mapstructure"
)

type AuthTokenPayload struct {
	Iss string `json:"iss"`
	Sub string `json:"sub"`
	Exp int    `json:"exp"`
	Iat int    `json:"jat"`
	Jti string `json:"jti"`

	TokenType   string `json:"token_type" mapstructure:"token_type"`
	UserID      int    `json:"user_id" mapstructure:"user_id"`
	Role        string `json:"role"`
	BurritoSalt string `json:"burrito_salt" mapstructure:"burrito_salt"`
}

func GetClearJWT(rawTokenData []string) (string, error) {
	var accessToken string
	if len(rawTokenData) == 1 {
		accessToken = rawTokenData[0]
	}
	accessToken, _ = strings.CutPrefix(accessToken, "Bearer ")

	if accessToken == "" {
		return "", errors.New("invalid JWT token provided")
	}

	return accessToken, nil
}

func GetTokenPayload(accessToken string) *AuthTokenPayload {
	claims := jwt.MapClaims{}
	accessTokenPayload := AuthTokenPayload{}

	jwt.ParseWithClaims(accessToken, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(GetConfig().JWT_SECRET), nil
	})
	mapstructure.Decode(claims, &accessTokenPayload)

	return &accessTokenPayload
}

func makeJWTRedisKey(data *AuthTokenPayload) string {
	return fmt.Sprintf("%s_%s_%d", data.Jti, data.TokenType, data.UserID)
}

func IsJWTExists(data *AuthTokenPayload) bool {
	value := RedisGetByKey(makeJWTRedisKey(data))
	return value != ""
}

func ValidateJWTAndCheckPermission(ctx *fiber.Ctx) *AuthTokenPayload {
	// get access token or return an error if the token is invalid or was not provided
	accessToken, err := GetClearJWT(ctx.GetReqHeaders()["Authorization"])
	if err != nil {
		responseObject, _ := json.Marshal(models.JsonResponse{Detail: err.Error()})
		ctx.SendStatus(403)
		ctx.JSON(string(responseObject))
		return nil
	}

	// read payload from the token
	accessTokenPayload := GetTokenPayload(accessToken)

	if !IsJWTExists(accessTokenPayload) {
		responseObject, _ := json.Marshal(models.JsonResponse{Detail: "JWT is invalid or expired"})
		ctx.SendStatus(403)
		ctx.JSON(string(responseObject))
		return nil
	}

	// return an error if current user's role is not ADMIN or CHIEF_ADMIN
	if !CheckForAdmin(accessTokenPayload.UserID) {
		responseObject, _ := json.Marshal(models.JsonResponse{Detail: "Is not allowed to interact with this resource"})
		ctx.SendStatus(403)
		ctx.JSON(string(responseObject))
		return nil
	}

	return accessTokenPayload
}
