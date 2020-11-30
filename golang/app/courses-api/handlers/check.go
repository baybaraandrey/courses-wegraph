package handlers

import (
	"context"
	"log"
	"net/http"

	"github.com/baybaraandrey/courses-wegraph/golang/foundation/web"
)

type check struct {
	log *log.Logger
}

func (c check) readiness(ctx context.Context, w http.ResponseWriter, r *http.Request) error {
	status := struct {
		Status string
	}{
		Status: "OK",
	}
	c.log.Println(r, status)

	return web.Respond(ctx, w, status, http.StatusOK)
}
