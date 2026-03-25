import os, json, datetime
from app.core.config import NOTEBOOK_DIR


def save_chat(user_id, question, answer):
    user_dir = os.path.join(NOTEBOOK_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)

    entry = {
        "time": datetime.datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }

    with open(os.path.join(user_dir, "chat.json"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
