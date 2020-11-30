// Package web ...
package web

import (
	"context"
	"net/http"
	"os"
	"syscall"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/mux"
)

type ctxKey int

// KeyValues ...
const KeyValues ctxKey = 1

// Values ...
type Values struct {
	TraceID    string
	Now        time.Time
	StatusCode int
}

// Handler ...
type Handler func(ctx context.Context, w http.ResponseWriter, r *http.Request) error

// App ...
type App struct {
	*mux.Router
	shutdown chan os.Signal
	mw       []Middleware
}

// NewApp ...
func NewApp(shutdown chan os.Signal, mw ...Middleware) *App {
	app := App{
		Router:   mux.NewRouter(),
		shutdown: shutdown,
		mw:       mw,
	}

	return &app
}

// SignalShutdown ...
func (a *App) SignalShutdown() {
	a.shutdown <- syscall.SIGTERM
}

// Handle ...
func (a *App) Handle(method string, path string, handler Handler, mw ...Middleware) {

	handler = wrapMiddleware(mw, handler)
	handler = wrapMiddleware(a.mw, handler)

	h := func(w http.ResponseWriter, r *http.Request) {
		v := Values{
			TraceID: uuid.New().String(),
			Now:     time.Now(),
		}
		ctx := context.WithValue(r.Context(), KeyValues, &v)
		if err := handler(ctx, w, r); err != nil {
			a.SignalShutdown()
			return
		}
	}

	a.Router.HandleFunc(path, h).Methods(method)
}
