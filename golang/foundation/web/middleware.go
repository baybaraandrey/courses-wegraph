package web

// Middleware ...
type Middleware func(Handler) Handler

func wrapMiddleware(mw []Middleware, handler Handler) Handler {
	i := len(mw) - 1
	for ; i >= 0; i-- {
		h := mw[i]
		if h != nil {
			handler = h(handler)
		}
	}

	return handler
}
