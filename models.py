def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
    }
