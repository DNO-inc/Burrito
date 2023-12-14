package utils

import (
	"errors"
	"fmt"
	"strings"

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
