STANDARD_EXTENSIONS = frozenset(
    {
        ".jpg",
        ".jpeg",
        ".heic",
        ".heif",
    }
)

RAW_EXTENSIONS = frozenset(
    {
        ".dng",
        ".cr2",
        ".cr3",
        ".nef",
        ".arw",
        ".raf",
    }
)

SUPPORTED_EXTENSIONS = STANDARD_EXTENSIONS | RAW_EXTENSIONS
