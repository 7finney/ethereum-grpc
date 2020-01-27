package controllers

import (
	"errors"
	"fmt"
	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
	"grpc-auth-api/server/database"
	"grpc-auth-api/server/types"
)

var jwtKey = []byte("qwerty")

// GetToken -> To get token with machine id
func GetToken(c *gin.Context) {
	machineID := c.Param("machineID")
	// expirationTime := time.Now().Add(5 * time.Minute)

	claims := &types.Claims{
		MachineID:      machineID,
		StandardClaims: jwt.StandardClaims{},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(jwtKey)
	database.SaveToDB(tokenString, machineID)

	if err != nil {
		// If there is an error in creating the JWT return an internal server error
		fmt.Println("err")
	}

	c.JSON(200, gin.H{
		"token": tokenString,
	})

}

// VerifyToken -> To verify token
func VerifyToken(c *gin.Context) {
	token := c.Param("token")
	fmt.Println(token)
	var msg string
	var code int

	tokenString, err := jwt.Parse(token, func(token *jwt.Token) (interface{}, error) {
		// Don't forget to validate the alg is what you expect:
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])

		}
		return jwtKey, nil

	})

	if err != nil {
		fmt.Println(err)
	}

	if claims, ok := tokenString.Claims.(jwt.MapClaims); ok && tokenString.Valid {
		machineID := claims["machineID"].(string)
		resp := database.CheckFromDB(token, machineID)
		if resp {
			msg = "Verified"
			code = 200
		} else {
			msg = "Token Invalid"
			code = 403
			err = errors.New("Invalid Machine id")
		}
	} else {
		msg = "Token Invalid"
		code = 403
		err = errors.New("Invalid JWT Token")
	}

	c.JSON(code, gin.H{
		"msg": msg,
	})

}
