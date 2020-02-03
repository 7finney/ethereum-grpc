package types

import (
	"github.com/dgrijalva/jwt-go"
)

// Claims JWT Type
type Claims struct {
	MachineID string `json:"machineID"`
	jwt.StandardClaims
}
