package database

import (
	"github.com/go-redis/redis"
	"log"
)

var url, _ = redis.ParseURL("redis://localhost:6379")

// Client -> redis client
var Client = redis.NewClient(&redis.Options{
	Addr:     url.Addr,
	Password: "", // no password set
	DB:       0,  // use default DB
})

// SaveToDB -> Check token from db
func SaveToDB(token string, machID string) {

	err := Client.Set(machID, token, 0).Err()
	if err != nil {
		log.Fatal(err)
	}
	// Output: PONG <nil>
}

// CheckFromDB -> Check token from db
func CheckFromDB(token string, machID string) bool {
	var ret bool
	val, err := Client.Get(machID).Result()
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
