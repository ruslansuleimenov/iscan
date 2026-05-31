# iscan

`iscan` is a local-first CLI application for finding duplicate and near-duplicate photos on macOS Apple Silicon.

Point it at a folder from a shooting day and get a local HTML report with groups of visually similar images, thumbnails, metadata, and similarity scores.

## Why iscan

Photographers often come back from a shoot with hundreds or thousands of similar frames. Finding duplicates, near-duplicates, bursts, and almost-identical shots by hand is slow and repetitive.

`iscan` helps with the first pass:

- scans local photo folders;
- finds duplicate and near-duplicate images;
- groups similar frames;
- shows metadata and previews;
- keeps the final decision manual and safe.

The first workflow targets a local review session of around 1000 photos from a camera or iPhone.

## MVP

The MVP is intentionally focused:

- Python CLI application;
- macOS Apple Silicon as the primary platform;
- MLX as the compute backend;
- local disk scanning;
- JPEG/JPG, HEIC/HEIF, and RAW camera files;
- exact top-k nearest-neighbor search;
- static HTML report;
- JSON scan session output;
- no cloud processing;
- no automatic deletion.

## CLI

Default scan command:

```bash
iscan /path/to/photos --report-html report.html
```

Explicit scan command:

```bash
iscan scan /path/to/photos --report-html report.html
```

The short form is the main user experience. The explicit `scan` form is kept for scripts and future subcommands.

## Development

This project uses `uv`.

```bash
uv sync
uv run iscan --help
uv run iscan --version
uv run ruff check .
uv run mypy src
```

## How It Works

The MVP pipeline:

1. Discover image files in one or more local paths.
2. Decode supported image formats, including camera RAW where possible.
3. Extract image metadata such as format, size, resolution, capture time, and location when available.
4. Build a compact image feature vector.
5. Use MLX to run exact top-k nearest-neighbor search.
6. Group likely duplicate or near-duplicate photos.
7. Generate a local HTML report and a machine-readable JSON scan session.

## Image Features

The first image extractor is `image-basic-v1`.

It is designed as a fast candidate retrieval vector, not as a full image-quality model:

- decode image or RAW preview;
- apply EXIF orientation when available;
- convert to RGB;
- resize to `64x64`;
- normalize pixel values;
- flatten to a vector;
- L2-normalize for cosine similarity.

`64x64` means a resized image of 64 pixels by 64 pixels. With RGB channels, the feature vector has `64 * 64 * 3 = 12288` values.

This deliberately loses fine detail, but it is fast and useful for finding visually similar frames in a homogeneous shooting session. Future extractors can use larger sizes, multi-scale features, patch/tiled features, perceptual hashes, or computer-vision embeddings.

## Similarity Search

The MVP uses exact top-k nearest-neighbor search over feature vectors.

Defaults:

- `top-k = 5`;
- cosine similarity by default;
- L2 distance as an alternative metric;
- MLX matrix operations for comparison;
- batched or blockwise computation when needed to control memory.

Approximate nearest-neighbor search with HNSW is reserved for larger collections.

## Reports

The MVP report is a static local HTML file.

It includes:

- groups of similar photos;
- thumbnails;
- file paths;
- file size and format;
- resolution;
- similarity scores;
- capture time and location when available;
- metadata details;
- warnings for skipped or unreadable files.

The report is for manual review. Deletion and file actions belong to a later worker-based version.

## Safety

The MVP does not delete, move, or rename files.

Destructive actions must be explicit, confirmed by the user, and preferably use the system Trash rather than permanent deletion.

## Architecture

`iscan` is a reusable core engine with thin adapters around it.

Core layers:

- core engine;
- feature extractor layer;
- compute backend layer;
- nearest-neighbor layer;
- scan session storage;
- report generation;
- CLI adapter;
- worker/control plane;
- MCP adapter.

The core engine does not depend on the CLI, HTML report, Swift UI, or MCP server.

## Roadmap

### MVP

- MLX-first CLI for macOS Apple Silicon.
- Local photo scanning.
- `image-basic-v1` feature extraction.
- Exact top-k nearest-neighbor search.
- HTML report and JSON scan session.

### v1

- PCA preprocessing.
- CPU fallback with NumPy/scikit-learn/SciPy-like tools.
- Automatic backend selection without a normal user-facing backend flag.

### v2

- Worker mode.
- Action layer for opening and deleting files.
- HTML actions with explicit confirmation.
- Swift/SwiftUI UI over the same engine.
- User interaction events for ranking algorithms.

### v3

- Local MCP server.
- Initial MCP tool: `scan`.
- MCP server communicates with the worker instead of duplicating engine logic.

## Future Ideas

- HNSW approximate nearest-neighbor search for large collections;
- patch/tiled image features for preserving more local detail;
- representative frame ranking with similarity PageRank;
- attention ranking from user navigation events;
- local personal preference ranking trained from user choices;
- video and audio similarity extractors.

## Privacy

`iscan` is local-first.

- Photos stay on the user's machine.
- Reports are generated locally.
- Preference learning is local by default.
- No cloud processing is part of the MVP.

## Status

This repository is in the pre-implementation phase. The public README describes the product direction; internal requirements and planning notes are kept locally and excluded from git.

## License

License is not selected yet.
