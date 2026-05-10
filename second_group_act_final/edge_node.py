import os
import random
import time
import uuid

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:5000")

NODE_ID = "node_1"

votes_sent = 0


def make_vote():
    # random ra nia nga generated vote pang simulate
    vote_info = {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "timestamp": time.time(),
        "node_id": NODE_ID,
    }

    return vote_info


def send_vote(vote_data, retries=3, delay=2):

    current_try = 1

    while current_try <= retries:

        try:
            response = requests.post(f"{API_URL}/vote", json=vote_data, timeout=5)

            if response.status_code == 200:
                print(f"[{NODE_ID}] Vote sent successfully -> {vote_data['choice']}")
                return True

            else:
                print(f"[{NODE_ID}] API returned error: {response.status_code}")

        except requests.exceptions.RequestException as err:
            print(f"[{NODE_ID}] Failed to send vote: {err}")

        # retry gamay if mapalya
        if current_try < retries:
            print(f"[{NODE_ID}] Retrying after {delay} seconds...")
            time.sleep(delay)

        current_try += 1

    print(f"[{NODE_ID}] Max retries reached for vote {vote_data['user_id']}")

    return False


def run_edge_node(duplicate=False):

    global votes_sent

    print(f"[{NODE_ID}] Edge node started...")
    print(f"[{NODE_ID}] Sending data to {API_URL}")

    while True:

        vote_data = make_vote()

        if duplicate:

            # fault injection kunohay hahaha
            print(f"[{NODE_ID}] Sending duplicate votes...")

            for x in range(3):
                send_vote(vote_data)
                votes_sent += 1

        else:
            send_vote(vote_data)
            votes_sent += 1

        print(f"[{NODE_ID}] Total votes sent: {votes_sent}")

        # random sleep para dili tanan sabay2
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)


if __name__ == "__main__":
    run_edge_node(duplicate=False)
