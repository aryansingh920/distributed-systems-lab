package main

import (
	"os"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/adaptor"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "4003"
	}

	app := fiber.New()

	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"ok": true, "service": "worker-gofiber"})
	})

	// Prometheus handler is net/http, so adapt it for Fiber
	app.Get("/metrics", adaptor.HTTPHandler(promhttp.Handler()))

	_ = app.Listen(":" + port)
}
