# Reproducible environments for the katalysis bank-financials project.
#
# This is a data project, not a service, so the image you want depends on the
# job. Three build targets, smallest to largest:
#
#   serve     Go static-file server + the pre-built deliverable. No Python, no
#             browser, no OCR. ~20MB. This is what you deploy.
#   pipeline  Python + OCR toolchain. Runs every scripts/build_<bank>.py, the
#             47-test unit suite, and refresh_all.py except its final PDF step.
#             No browser.
#   full      pipeline + Chromium. Adds the client-PDF export and test_pipeline.py.
#
# Build and run:
#   docker build --target serve    -t katalysis:serve .
#   docker run --rm -p 8008:8008 katalysis:serve
#
#   docker build --target pipeline -t katalysis:pipeline .
#   docker run --rm -v "$PWD:/app" katalysis:pipeline \
#       python3 -m unittest discover -s scripts/insights -p 'test_*.py'
#
#   docker build --target full     -t katalysis:full .
#   docker run --rm -v "$PWD:/app" katalysis:full python3 scripts/insights/refresh_all.py
#
# Mount the repo (-v) for pipeline/full: banks/*.xlsx, research/insights.db and
# deliverable/ are the project's real outputs and must land on the host, not in
# a discarded container layer.


# ---------------------------------------------------------------------------
# serve - static file server for the pre-built deliverable
# ---------------------------------------------------------------------------
# Deliberately does NOT read the database at runtime. deliverable/ is ~308
# pre-rendered HTML files produced by build_deliverable.py; the database is a
# build-time input, not a serving dependency. Keeping it that way is why this
# image needs no Python and no interpreter at all.
#
# server/go.mod declares go 1.26.5, and server/main.go uses the Go 1.22+ "/{$}"
# routing pattern, so the toolchain must be at least that new. Override with
# --build-arg GO_VERSION=... if your registry lacks this tag.
ARG GO_VERSION=1.26-alpine

FROM golang:${GO_VERSION} AS server-build
WORKDIR /src/server
# No third-party imports (net/http only), so there is nothing to `go mod
# download` - copying the source is the whole dependency step.
COPY server/go.mod server/main.go ./
# Static binary: CGO off so it runs in a scratch/alpine image with no libc.
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/katalysis-server .

FROM alpine:3.20 AS serve
# curl is here only so the HEALTHCHECK below has something to call; drop both
# if you'd rather keep the image to just the binary and the HTML.
RUN apk add --no-cache ca-certificates curl \
    && adduser -D -u 10001 katalysis
WORKDIR /app
COPY --from=server-build /out/katalysis-server /usr/local/bin/katalysis-server
# The pre-built site. Rebuild it with the `full` (or `pipeline`) image before
# building this target, or you will ship a stale deliverable.
COPY deliverable/ /app/deliverable/
USER katalysis
EXPOSE 8008
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD curl -fsS http://127.0.0.1:8008/comparison.html -o /dev/null || exit 1
# -dir must be absolute here; the binary's own default is a relative
# "../deliverable" that assumes you're running from server/.
CMD ["katalysis-server", "-addr", "0.0.0.0:8008", "-dir", "/app/deliverable"]


# ---------------------------------------------------------------------------
# pipeline - Python + OCR, no browser
# ---------------------------------------------------------------------------
# 3.11 rather than the 3.9 on the current dev machine (3.9 is end-of-life), and
# not 3.12+, because scripts/insights/fetch_market_data.py uses
# datetime.utcfromtimestamp(), which 3.12 deprecates noisily.
FROM python:3.11-slim-bookworm AS pipeline

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# poppler-utils and tesseract are load-bearing, not conveniences. A large share
# of Companies House filings are scanned, image-only PDFs, and the established
# workflow is "pdftotext returns nothing -> pdftoppm -> tesseract". Several
# banks' figures (Close Brothers, KEXIM, Monument, DB UK Bank) exist ONLY behind
# OCR; without it, research silently degrades to text-only extraction and
# reproduces exactly the wrong "not publicly disclosed" claims this project has
# repeatedly had to fix.
RUN apt-get update && apt-get install -y --no-install-recommends \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-eng \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies before source, so editing a build script doesn't invalidate this
# layer. requirements.txt excludes playwright; the `full` stage adds it.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fail the build loudly if the OCR toolchain is missing, rather than shipping an
# image that quietly produces wrong results.
RUN python3 -c "import openpyxl, numpy, fitz; print('python deps OK')" \
    && pdftotext -v \
    && tesseract --version

# No pipeline CMD: refreshing writes to banks/, research/ and deliverable/, so
# it should always be an explicit invocation.
CMD ["bash"]


# ---------------------------------------------------------------------------
# full - pipeline + Chromium for PDF export and browser tests
# ---------------------------------------------------------------------------
FROM pipeline AS full

# Keep the browser inside the image rather than under a $HOME that a bind mount
# could shadow at runtime.
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# playwright is the only dependency that differs from the pipeline stage. It is
# needed by scripts/insights/build_in006_pdf.py (step 22 of refresh_all.py, the
# client PDF render) and by scripts/insights/test_pipeline.py. Note this is NOT
# merely a test dependency: without this stage, refresh_all.py stops at step 21.
RUN pip install --no-cache-dir "playwright==1.60.0" \
    && playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -c "import playwright; print('playwright OK')"

CMD ["bash"]
