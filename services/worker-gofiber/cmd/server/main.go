// """
// Created on 04/01/2026

// @author: Aryan

// Filename: main.go

// Relative Path: services/worker-gofiber/cmd/server/main.go
// """

package main

import (
	"os"

	"encoding/json"
	"github.com/gofiber/fiber/v2"
	"worker-gofiber/internal/redisclient"
	"github.com/gofiber/fiber/v2/middleware/adaptor"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "4003"
	}

	redisclient.Init()
	if err := redisclient.Rdb.Ping(redisclient.Ctx).Err(); err != nil {
		panic(err)
	}

	app := fiber.New()

	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"ok": true, "service": "worker-gofiber"})
	})

	// Prometheus handler is net/http, so adapt it for Fiber
	app.Get("/metrics", adaptor.HTTPHandler(promhttp.Handler()))



	type RecentItem map[string]any

	app.Get("/orders/recent", func(c *fiber.Ctx) error {
		vals, err := redisclient.Rdb.LRange(redisclient.Ctx, redisclient.KeyLast2, 0, 1).Result()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"ok": false, "error": err.Error()})
		}

		out := make([]RecentItem, 0, len(vals))
		for _, s := range vals {
			var obj RecentItem
			if err := json.Unmarshal([]byte(s), &obj); err != nil {
				// if one entry is malformed, still return raw
				out = append(out, RecentItem{"raw": s})
				continue
			}
			out = append(out, obj)
		}

		return c.JSON(fiber.Map{"ok": true, "items": out})
	})
	_ = app.Listen(":" + port)
}
