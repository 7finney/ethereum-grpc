package main

import (
	// "context"
	// "errors"
	"fmt"
	"github.com/gin-gonic/gin"
	"grpc-auth-api/server/controllers"
	"grpc-auth-api/server/database"
	// "log"
	// "net"
)

// type server struct{}

// var jwtKey = []byte("qwerty")

// type Claims struct {
// 	Id string `json:"Id"`
// 	jwt.StandardClaims
// }

// var url, _ = redis.ParseURL("redis://redis:6379")
// var client = redis.NewClient(&redis.Options{
// 	Addr:     url.Addr,
// 	Password: "", // no password set
// 	DB:       0,  // use default DB
// })

// func (s *server) GenToken(ctx context.Context, request *protos.Request) (*protos.Response, error) {
// 	machineID := request.GetMachineId()
// 	claims := &Claims{
// 		Id:             machineID,
// 		StandardClaims: jwt.StandardClaims{},
// 	}
// 	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
// 	tokenString, err := token.SignedString(jwtKey)
// SaveToDB(tokenString, machineID)

// 	return &protos.Response{Token: tokenString}, err
// }

// func (s *server) VerifyToken(ctx context.Context, request *protos.VerifyRequest) (*protos.VerifyResponse, error) {
// 	var msg string
// 	var err error
// 	Token := request.GetToken()
// 	tokenString, err := jwt.Parse(Token, func(token *jwt.Token) (interface{}, error) {
// 		// Don't forget to validate the alg is what you expect:
// 		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
// 			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
// 		} else {
// 			return jwtKey, nil
// 		}
// 	})
// 	if claims, ok := tokenString.Claims.(jwt.MapClaims); ok && tokenString.Valid {
// 		machineID := claims["Id"].(string)
// 		resp := CheckFromDB(Token, machineID)
// 		if resp {
// 			msg = "Verified!!!"
// 		} else {
// 			msg = "Token Invalid!!!"
// 			err = errors.New("Invalid Machine id")
// 		}
// 	} else {
// 		msg = "Token Invalid!!!"
// 		err = errors.New("Invalid JWT Token")
// 	}
// 	return &protos.VerifyResponse{Msg: msg}, err
// }

// func main() {
// 	listener, err := net.Listen("tcp", ":4040")
// 	if err != nil {
// 		panic(err)
// 	}

// 	srv := grpc.NewServer()
// 	fmt.Println("GRPC Server Started")
// 	protos.RegisterGenJWTTokenServer(srv, &server{})
// 	reflection.Register(srv)
// 	if e := srv.Serve(listener); e != nil {
// 		panic(err)
// 	}
// }
func main() {
	r := gin.Default()

	pong, err := database.Client.Ping().Result()

	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(pong)

	r.GET("/getToken/:machineID", controllers.GetToken)
	r.GET("/verifyToken/:token", controllers.VerifyToken)

	r.Run()
}
