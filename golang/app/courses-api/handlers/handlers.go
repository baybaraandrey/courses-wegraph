// Package handlers contains the full set of handler functions and routes
// supported by the web api.
package handlers

import (
	"log"
	"os"

	"github.com/baybaraandrey/courses-wegraph/golang/foundation/web"
)

// API ...
func API(build string, shutdown chan os.Signal, log *log.Logger) *web.App {
	router := web.NewApp(shutdown)
	check := check{
		log: log,
	}
	router.Handle("get", "/readiness", check.readiness)

	return router
}