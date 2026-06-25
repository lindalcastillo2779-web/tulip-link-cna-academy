from functools import lru_cache
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CHAPTER_VIDEO_URL = "https://www.youtube.com/watch?v=qTQ5YGQ5wE8"

ICON_RULES = [
    (("infection",), "\U0001f9fc"),
    (("legal", "ethical", "rights"), "\u2696\ufe0f"),
    (("communication", "culture"), "\U0001f4ac"),
    (("safety", "mechanics"), "\U0001f9ba"),
    (("hygiene", "grooming"), "\U0001f6c1"),
    (("elimination", "catheter"), "\U0001f6bd"),
    (("nutrition", "hydration"), "\U0001f34e"),
    (("vital",), "\U0001f4c8"),
    (("sleep", "rest"), "\U0001f319"),
    (("transfer", "mobility"), "\U0001f9bd"),
    (("behavioral", "emotional"), "\U0001f9e0"),
    (("dying", "postmortem"), "\U0001f54a\ufe0f"),
    (("elderly", "dementia"), "\U0001f475"),
    (("illness",), "\U0001fa79"),
]

THUMBNAIL_RULES = [
    (("infection",), "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=1200&q=80"),
    (("legal", "ethical", "rights"), "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80"),
    (("communication", "culture"), "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1200&q=80"),
    (("safety", "mechanics"), "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=1200&q=80"),
    (("hygiene", "grooming"), "https://images.unsplash.com/photo-1628771065518-0d82f1938462?auto=format&fit=crop&w=1200&q=80"),
    (("nutrition", "hydration"), "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=1200&q=80"),
    (("dementia", "elderly"), "https://images.unsplash.com/photo-1516307365426-bea591f05011?auto=format&fit=crop&w=1200&q=80"),
    (("vital", "clinical"), "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80"),
    (("behavioral", "emotional"), "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80"),
    (("rest", "sleep"), "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80"),
]

DEFAULT_CHAPTER_VIDEOS = {
    1: "https://www.youtube.com/watch?v=qTQ5YGQ5wE8",
    2: "https://www.youtube.com/watch?v=HAnw168huqA",
    3: "https://www.youtube.com/watch?v=HAnw168huqA",
    4: "https://www.youtube.com/watch?v=3PmVJQUCm4E",
    5: "https://www.youtube.com/watch?v=2fYf2b6YfFM",
    6: "https://www.youtube.com/watch?v=3PmVJQUCm4E",
    7: "https://www.youtube.com/watch?v=2fYf2b6YfFM",
    8: "https://www.youtube.com/watch?v=9p5Bf2J9Q4I",
    9: "https://www.youtube.com/watch?v=qTQ5YGQ5wE8",
    10: "https://www.youtube.com/watch?v=qTQ5YGQ5wE8",
    11: "https://www.youtube.com/watch?v=2fYf2b6YfFM",
    12: "https://www.youtube.com/watch?v=2fYf2b6YfFM",
    13: "https://www.youtube.com/watch?v=U6sLOH4xQWQ",
    14: "https://www.youtube.com/watch?v=qTQ5YGQ5wE8",
    15: "https://www.youtube.com/watch?v=U6sLOH4xQWQ",
    16: "https://www.youtube.com/watch?v=U6sLOH4xQWQ",
    17: "https://www.youtube.com/watch?v=2fYf2b6YfFM",
    18: "https://www.youtube.com/watch?v=qTQ5YGQ5wE8",
}


def _lookup_by_keywords(text, rules, default_value):
    lowered = text.lower()
    for keywords, value in rules:
        if any(keyword in lowered for keyword in keywords):
            return value
    return default_value


@lru_cache(maxsize=1)
def load_chapter_video_overrides():
    config_path = BASE_DIR / "chapter_videos.json"
    if not config_path.exists():
        return {}

    overrides = {}
    try:
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return overrides

    for key, value in loaded.items():
        try:
            key_int = int(key)
        except (TypeError, ValueError):
            continue
        if isinstance(value, str) and value.strip():
            overrides[key_int] = value.strip()
    return overrides


def lesson_icon_from_title(title):
    return _lookup_by_keywords(title, ICON_RULES, "\U0001f4d8")


def chapter_thumbnail_from_title(title):
    return _lookup_by_keywords(
        title,
        THUMBNAIL_RULES,
        "https://images.unsplash.com/photo-1519494080410-f9aa8f52f12e?auto=format&fit=crop&w=1200&q=80",
    )


def chapter_video_from_module(chapter_number):
    videos = DEFAULT_CHAPTER_VIDEOS.copy()
    videos.update(load_chapter_video_overrides())
    return videos.get(int(chapter_number), DEFAULT_CHAPTER_VIDEO_URL)
