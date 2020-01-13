package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net"

	"grpc-auth-api/services"
	"github.com/dgrijalva/jwt-go"
	"github.com/go-redis/redis"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

type server struct{}

var jwtKey = []byte("qwerty")

type Claims struct {
	Id string `json:"Id"`
	jwt.StandardClaims
}

var url, _ = redis.ParseURL("redis://redis:6379")
var client = redis.NewClient(&redis.Options{
	Addr:     url.Addr,
	Password: "", // no password set
	DB:       0,  // use default DB
})

func SaveToDB(token string, machId string) {

	pong, err := client.Ping().Result()
	fmt.Println(pong, err)
	client.Set(machId, token, 0)
	if err != nil {
		log.Fatal(err)
	}
	// Output: PONG <nil>
}

func CheckFromDB(token string, machId string) bool {
	var ret bool
	// client := redis.NewClient(&redis.Options{
	// 	Addr:     "redis:6379",
	// 	Password: "", // no password set
	// 	DB:       0,  // use default DB
	// })
	val, err := client.Get(machId).Result()
	if err != nil {
		ret = false
	}
	if val == token {
		ret = true
	} else {
		ret = false
	}
	return ret
}

func (s *server) GenToken(ctx context.Context, request *protos.Request) (*protos.Response, error) {
	machineID := request.GetMachineId()
	claims := &Claims{
		Id:             machineID,
		StandardClaims: jwt.StandardClaims{},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(jwtKey)
	SaveToDB(tokenString, machineID)

	return &protos.Response{Token: tokenString}, err
}

func (s *server) VerifyToken(ctx context.Context, request *protos.VerifyRequest) (*protos.VerifyResponse, error) {
	var msg string
	var err error
	Token := request.GetToken()
	tokenString, err := jwt.Parse(Token, func(token *jwt.Token) (interface{}, error) {
		// Don't forget to validate the alg is what you expect:
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		} else {
			return jwtKey, nil
		}
	})
	if claims, ok := tokenString.Claims.(jwt.MapClaims); ok && tokenString.Valid {
		machineID := claims["Id"].(string)
		resp := CheckFromDB(Token, machineID)
		if resp {
			msg = "Verified!!!"
		} else {
			msg = "Token Invalid!!!"
			err = errors.New("Invalid Machine id")
		}
	} else {
		msg = "Token Invalid!!!"
		err = errors.New("Invalid JWT Token")
	}
	return &protos.VerifyResponse{Msg: msg}, err
}

func main() {
	listener, err := net.Listen("tcp", ":4040")
	if err != nil {
		panic(err)
	}

	srv := grpc.NewServer()
	protos.RegisterGenJWTTokenServer(srv, &server{})
	reflection.Register(srv)
	if e := srv.Serve(listener); e != nil {
		panic(err)
	}
}
