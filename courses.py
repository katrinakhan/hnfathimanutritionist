"""Course catalog for the shop. Embed URLs use Bunny Stream."""

COURSES = {
    "3-day-gut-health": {
        "id": "3-day-gut-health",
        "title": "3-Day Gut Health Challenge",
        "price_cents": 1000,  # $10.00 USD
        "currency": "usd",
        "short_description": (
            "A simple 3-day video challenge to support gut health — "
            "watch one lesson each day and take action."
        ),
        "description": (
            "Join this short challenge with three focused video lessons. "
            "Complete Day 1, Day 2, and Day 3 at your own pace — lifetime "
            "access after purchase."
        ),
        "lessons": [
            {
                "title": "Day 1 — Gut Health Challenge",
                "duration": "19:28",
                "embed_url": (
                    "https://player.mediadelivery.net/embed/705527/"
                    "aa9e8f57-6535-4e08-8c19-2bd18b8a5170"
                ),
            },
            {
                "title": "Day 2 — Gut Health Challenge",
                "duration": "13:59",
                "embed_url": (
                    "https://player.mediadelivery.net/embed/705527/"
                    "e7fb8558-c144-40ea-9bd2-bb9612640827"
                ),
            },
            {
                "title": "Day 3 — Gut Health Challenge",
                "duration": "08:58",
                "embed_url": (
                    "https://player.mediadelivery.net/embed/705527/"
                    "5ac8c762-6ddf-40b6-99a4-9fa1813567e2"
                ),
            },
        ],
    },
}


def get_course(course_id: str) -> dict | None:
    return COURSES.get(course_id)


def all_courses() -> list[dict]:
    return list(COURSES.values())
