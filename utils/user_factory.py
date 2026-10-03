import uuid


def build_user() -> dict:
    suffix = uuid.uuid4().hex[:10]
    return {
        "first_name": "QA",
        "last_name": "Portfolio",
        "address": {
            "street": "Eckertplatz 42",
            "house_number": "42",
            "city": "Heidenheim an der Brenz",
            "state": "Rheinland-Pfalz",
            "country": "DE",
            "postal_code": "10115",
        },
        "phone": "0123456789",
        "dob": "1995-05-20",
        "password": f"Qa-Portfolio-{suffix}!",
        "email": f"qa.{suffix}@example.com",
    }