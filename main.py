import os
import traceback
from datetime import timedelta

import stripe
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from courses import all_courses, get_course

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.permanent_session_lifetime = timedelta(days=365)
# Secure cookies only in production (HTTPS). Local HTTP needs this off.
_is_production = bool(os.environ.get("PUBLIC_BASE_URL") or os.environ.get("RENDER"))
app.config["SESSION_COOKIE_SECURE"] = _is_production
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
ACCESS_MAX_AGE = 60 * 60 * 24 * 365  # 1 year


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(app.secret_key, salt="course-access")


def grant_course_access(course_id: str) -> None:
    session.permanent = True
    owned = list(session.get("owned_courses", []))
    if course_id not in owned:
        owned.append(course_id)
        session["owned_courses"] = owned


def has_course_access(course_id: str) -> bool:
    return course_id in session.get("owned_courses", [])


def make_access_token(course_id: str) -> str:
    return _serializer().dumps({"course_id": course_id})


def verify_access_token(token: str, course_id: str) -> bool:
    try:
        data = _serializer().loads(token, max_age=ACCESS_MAX_AGE)
        return data.get("course_id") == course_id
    except (BadSignature, SignatureExpired):
        return False


def public_base_url() -> str:
    configured = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
    if configured:
        return configured
    return request.url_root.rstrip("/")


def _session_course_id(checkout_session) -> str | None:
    metadata = checkout_session.get("metadata") or {}
    if hasattr(metadata, "to_dict"):
        metadata = metadata.to_dict()
    course_id = None
    if isinstance(metadata, dict):
        course_id = metadata.get("course_id")
    if not course_id:
        course_id = checkout_session.get("client_reference_id")
    return course_id


def _stripe_error_message(exc: Exception) -> str:
    return getattr(exc, "user_message", None) or str(exc)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/shop")
def shop():
    return render_template("shop.html", courses=all_courses())


@app.route("/shop/<course_id>")
def course_detail(course_id):
    course = get_course(course_id)
    if not course:
        abort(404)
    owned = has_course_access(course_id)
    return render_template("course_detail.html", course=course, owned=owned)


@app.route("/shop/<course_id>/checkout", methods=["POST"])
def create_checkout(course_id):
    course = get_course(course_id)
    if not course:
        abort(404)

    if has_course_access(course_id):
        return redirect(url_for("watch_course", course_id=course_id))

    if not stripe.api_key:
        flash(
            "Stripe is not configured yet. Add STRIPE_SECRET_KEY in Render Environment.",
            "error",
        )
        return redirect(url_for("course_detail", course_id=course_id))

    base = public_base_url()
    try:
        checkout_session = stripe.checkout.Session.create(
            mode="payment",
            client_reference_id=course_id,
            line_items=[
                {
                    "price_data": {
                        "currency": course["currency"],
                        "unit_amount": course["price_cents"],
                        "product_data": {
                            "name": course["title"],
                            "description": course["short_description"][:400],
                        },
                    },
                    "quantity": 1,
                }
            ],
            success_url=(
                f"{base}{url_for('checkout_success')}?session_id={{CHECKOUT_SESSION_ID}}"
            ),
            cancel_url=f"{base}{url_for('course_detail', course_id=course_id)}",
            metadata={"course_id": course_id},
        )
    except Exception as exc:
        app.logger.exception("Stripe checkout create failed")
        flash(f"Checkout could not be started: {_stripe_error_message(exc)}", "error")
        return redirect(url_for("course_detail", course_id=course_id))

    return redirect(checkout_session.url, code=303)


@app.route("/shop/success")
def checkout_success():
    session_id = request.args.get("session_id")
    if not session_id or not stripe.api_key:
        flash("Missing payment confirmation.", "error")
        return redirect(url_for("shop"))

    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        payment_status = checkout_session.get("payment_status")
        status = checkout_session.get("status")

        # Card payments usually become "paid"; accept completed sessions too.
        paid = payment_status == "paid" or (
            status == "complete" and payment_status in ("paid", "no_payment_required")
        )
        if not paid:
            flash("Payment is not complete yet. If you were charged, contact support.", "error")
            return redirect(url_for("shop"))

        course_id = _session_course_id(checkout_session)
        course = get_course(course_id) if course_id else None
        if not course:
            flash("Payment succeeded, but the course could not be found.", "error")
            return redirect(url_for("shop"))

        grant_course_access(course_id)
        access_token = make_access_token(course_id)
        return render_template(
            "checkout_success.html",
            course=course,
            access_token=access_token,
        )
    except Exception:
        app.logger.error("checkout_success failed:\n%s", traceback.format_exc())
        flash(
            "Payment may have succeeded, but unlocking the course failed. "
            "Please contact support with your email/receipt.",
            "error",
        )
        return redirect(url_for("shop"))


@app.route("/my-courses/<course_id>")
def watch_course(course_id):
    course = get_course(course_id)
    if not course:
        abort(404)

    token = request.args.get("access")
    if token and verify_access_token(token, course_id):
        grant_course_access(course_id)

    if not has_course_access(course_id):
        flash("Please purchase this course to watch the lessons.", "error")
        return redirect(url_for("course_detail", course_id=course_id))

    return render_template("watch_course.html", course=course)


if __name__ == "__main__":
    app.config["SESSION_COOKIE_SECURE"] = False
    app.run(debug=True, host="127.0.0.1", port=5001)
