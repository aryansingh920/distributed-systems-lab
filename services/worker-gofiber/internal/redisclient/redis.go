// """
// Created on 04/01/2026

// @author: Aryan

// Filename: redis.go

// Relative Path: services/worker-gofiber/internal/redisclient/redis.go
// """

package redisclient

import (
	"context"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

var (
	Ctx  = context.Background()
	Rdb  *redis.Client
	KeyLast2 = "orders:last2"
)

func Init() {
	addr := os.Getenv("REDIS_ADDR")
	if addr == "" {
		addr = "redis:6379"
	}

	Rdb = redis.NewClient(&redis.Options{
		Addr:        addr,
		DialTimeout: 3 * time.Second,
		ReadTimeout: 3 * time.Second,
		WriteTimeout: 3 * time.Second,
	})
}
