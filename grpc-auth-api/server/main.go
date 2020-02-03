package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"grpc-auth-api/server/controllers"
	"grpc-auth-api/server/database"
)

func main() {
	r := gin.Default()

	pong, err := database.Client.Ping().Result()

	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(pong)

	r.GET("/getToken/:machineID", controllers.GetToken)
	r.GET("/verifyToken/:token", controllers.VerifyToken)

	r.Run(":4040")
}
