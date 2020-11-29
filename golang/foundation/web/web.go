// Package web ...
package web

import (
	"context"
	"net/http"
	"os"
	"syscall"

	"github.com/gorilla/mux"
)

// Handler ...
type Handler func(ctx context.Context, w http.ResponseWriter, r *http.Request) error

// App ...
type App struct {
	*mux.Router
	shutdown chan os.Signal
}

// NewApp ...
func NewApp(shutdown chan os.Signal) *App {
	app := App{
		Router:   mux.NewRouter(),
		shutdown: shutdown,
	}

	return &app
}

// SignalShutdown ...
func (a *App) SignalShutdown() {
	a.shutdown <- syscall.SIGTERM
}

// Handle ...
func (a *App) Handle(method string, path string, handler Handler) {
	h := func(w http.ResponseWriter, r *http.Request) {
		if err := handler(r.Context(), w, r); err != nil {
			a.SignalShutdown()
			return
		}
	}

	a.Router.HandleFunc(path, h).Methods(method)
}