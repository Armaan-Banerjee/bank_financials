package main

import (
	"flag"
	"log"
	"net/http"
	"path/filepath"
)

func main() {
	addr := flag.String("addr", "0.0.0.0:8008", "address to listen on")
	dir := flag.String("dir", "../deliverable", "path to the deliverable directory to serve")
	flag.Parse()

	deliverableDir, err := filepath.Abs(*dir)
	if err != nil {
		log.Fatalf("resolving deliverable dir: %v", err)
	}

	mux := http.NewServeMux()
	mux.Handle("/", http.FileServer(http.Dir(deliverableDir)))
	mux.HandleFunc("/{$}", func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, "/comparison.html", http.StatusFound)
	})

	log.Printf("serving %s on http://%s", deliverableDir, *addr)
	log.Fatal(http.ListenAndServe(*addr, mux))
}
