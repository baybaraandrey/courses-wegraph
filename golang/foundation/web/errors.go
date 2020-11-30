package web

import "github.com/pkg/errors"

// FieldError is used to indicates an error with a specific request field.
type FieldError struct {
	Field string `json:"field"`
	Error string `json:"error"`
}

// ErrorResponse is the form used for API response from failures in the API.
type ErrorResponse struct {
	Error  string       `json:"error"`
	Fields []FieldError `json:"fields,omitempty"`
}

// Error .is used to pass an error during the request throuth the
// application with web specific context.
type Error struct {
	Err    error
	Status int
	Fields []FieldError
}

// NewRequestError ...
func NewRequestError(err error, status int) error {
	return &Error{err, status, nil}
}

// Error ...
func (err *Error) Error() string {
	return err.Err.Error()
}

type shutdown struct {
	Message string
}

// NewRequestError ...
func NewShutdownError(message string) error {
	return &shutdown{message}
}

// Error ...
func (s *shutdown) Error() string {
	return s.Message
}

// IsShutdown ...
func IsShutdown(err error) bool {
	if _, ok := errors.Cause(err).(*shutdown); ok {
		return true
	}
	return false
}
