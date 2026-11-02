"""Public guides. Each one answers a search question and points to a course."""

ARTICLES = [
    {
        "slug": "what-to-eat-for-fat-loss",
        "title": "What should I eat to lose fat?",
        "description": (
            "A simple way to eat for fat loss: protein, fiber, fats, and water, "
            "without a crash diet. From certified nutritionist HN Fathima."
        ),
        "course_id": "easiest-way-to-lose-weight",
        "sections": [
            {
                "heading": "Start with the foods that keep you full",
                "paragraphs": [
                    "Fat loss gets easier when meals keep you full. Build each plate around protein, vegetables or other high-fiber foods, and a source of fat. Protein and fiber are the two things most people under-eat when they are trying to lose weight.",
                    "You do not need a new diet name every Monday. You need meals you can repeat. HN Fathima's course The Easiest Way to Lose Weight starts with carbs, fiber, protein, fats, vitamins, minerals, and water, then shows how those pieces fit into a normal day.",
                ],
            },
            {
                "heading": "What a simple plate looks like",
                "paragraphs": [
                    "Fill half the plate with vegetables or another high-fiber food. Add a palm-sized portion of protein such as eggs, fish, chicken, yogurt, lentils, or beans. Add a thumb-sized portion of fat such as olive oil, nuts, or avocado. Use a fist-sized portion of starch such as rice, potato, or fruit if you want it.",
                    "Drink water through the day. Sleep and stress change hunger, so food is only one part of the plan. The course also covers exercise, sleep, stress, and the habits that make the plate stick.",
                ],
            },
            {
                "heading": "Where to get the meals",
                "paragraphs": [
                    "The course includes breakfast, lunch, dinner, and snack recipes, plus grocery lists, so you are not left guessing after the lesson ends. Buy it once on this website and watch it here. There is no Udemy subscription.",
                ],
            },
        ],
    },
    {
        "slug": "course-vs-a-diet",
        "title": "How is this course different from a diet?",
        "description": (
            "A diet ends. HN Fathima's weight loss course teaches the meals, "
            "habits, sleep, and stress skills you keep using."
        ),
        "course_id": "easiest-way-to-lose-weight",
        "sections": [
            {
                "heading": "A diet gives you rules for a few weeks",
                "paragraphs": [
                    "Most diets hand you a food list and a deadline. When the deadline ends, the old meals come back and the weight often comes back with them. That is the cycle HN Fathima went through before she lost 20kg and trained as a nutritionist.",
                    "The Easiest Way to Lose Weight is not a 7-day menu. It is a set of lessons you can replay: what to eat, how to train, how to sleep, how stress changes eating, and how to set up your kitchen so you stop sabotaging the plan.",
                ],
            },
            {
                "heading": "You buy it once",
                "paragraphs": [
                    "On this website the course is a one-time payment with lifetime access. You watch it here. You do not create a Udemy account or pay a platform subscription to keep the lessons.",
                    "If you want a shorter start, the 3-Day Gut Health Challenge is three videos, one focus a day. Obesity the New Pandemic is a single lesson on three practical ways to deal with weight gain. The full course is the one to choose when you want the meals and the habits together.",
                ],
            },
        ],
    },
    {
        "slug": "can-exercise-alone-lose-weight",
        "title": "Can I lose weight with exercise alone?",
        "description": (
            "Exercise helps, but it rarely beats a food pattern that stays the same. "
            "HN Fathima explains what to change first."
        ),
        "course_id": "easiest-way-to-lose-weight",
        "sections": [
            {
                "heading": "Workouts help. They are not the whole plan.",
                "paragraphs": [
                    "A hard workout can burn a few hundred calories. A usual dinner can put those calories back. People who add exercise and leave meals unchanged often feel fitter and still see the same number on the scale.",
                    "Use exercise to keep muscle, which helps your metabolism, and to feel better. Use food to create the deficit. That is the order inside The Easiest Way to Lose Weight: nutrition first, then exercise, sleep, and stress.",
                ],
            },
            {
                "heading": "What to change this week",
                "paragraphs": [
                    "Keep the walks or the workouts you already do. Change one meal so it has more protein and more vegetables, and stop drinking calories you do not notice, such as juice, sweet coffee, and alcohol on weeknights.",
                    "If you want the full sequence, including recipes and the lessons on metabolism, sleep, and mindset, start with the course on this site. The obesity lesson is the short version if you only want the top three actions.",
                ],
            },
        ],
    },
]


def all_articles() -> list[dict]:
    return list(ARTICLES)


def get_article(slug: str) -> dict | None:
    for article in ARTICLES:
        if article["slug"] == slug:
            return article
    return None
