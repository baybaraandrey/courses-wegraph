package web

import (
	"context"
	"encoding/json"
	"net/http"
)

// Respond convert a go value to JSON and sends it to the client.
func Respond(ctx context.Context, w http.ResponseWriter, data interface{}, statusCode int) error {
	v, ok := ctx.Value(KeyValues).(*Values)
	if !ok {
		return NewShutdownError("web value missing from context")
	}
	v.StatusCode = statusCode

	if statusCode == http.StatusNoContent {
		w.WriteHeader(statusCode)
		return nil
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}

	// Set content type once we know marshaling has succeeded.
	w.Header().Set("Content-Type", "application/json")

	// Write the status code to response.
	w.WriteHeader(statusCode)

	// Send result back to the client.
	if _, err := w.Write(jsonData); err != nil {
		return err
	}

	return nil
}
