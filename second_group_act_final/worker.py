import os
import time

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

votes_processed = 0
duplicates_skipped = 0


def process_vote(vote_message):

    global votes_processed
    global duplicates_skipped

    # unique id para iwas duplicate save
    document_id = f"{vote_message['user_id']}_{vote_message['poll_id']}"

    try:

        save_data = {
            "id": document_id,
            "user_id": vote_message["user_id"],
            "poll_id": vote_message["poll_id"],
            "choice": vote_message["choice"],
            "timestamp": vote_message["timestamp"],
            "node_id": vote_message.get("node_id", "unknown"),
        }

        # upsert para safe maskin duplicate ma receive
        supabase.table("votes").upsert(save_data).execute()

        # mark as processed
        supabase.table("vote_queue").update({"status": "processed"}).eq(
            "id", vote_message["queue_id"]
        ).execute()

        votes_processed += 1

        print(
            f"[WORKER] Processed vote {vote_message['user_id']} "
            f"Choice: {vote_message['choice']}"
        )

    except Exception as err:

        # if fail, dili sa i processed para ma retry later
        print(f"[WORKER] Error processing vote {document_id}: {err}")


def get_pending_votes(batch_size=10):

    try:

        result = (
            supabase.table("vote_queue")
            .select("*")
            .eq("status", "pending")
            .order("created_at", desc=False)
            .limit(batch_size)
            .execute()
        )

        if result.data:
            return result.data

        return []

    except Exception as err:
        print(f"[WORKER] Error fetching queue data: {err}")
        return []


def run_worker():

    print("[WORKER] Worker started...")
    print("[WORKER] Listening for pending votes...")

    while True:

        pending_votes = get_pending_votes()

        if len(pending_votes) > 0:

            print(f"[WORKER] Found {len(pending_votes)} pending votes")

            for vote in pending_votes:

                # save ang queue row id para ma update later
                vote["queue_id"] = vote["id"]

                process_vote(vote)

        else:
            print(f"[WORKER] No pending votes yet...")

        # polling interval
        time.sleep(2)


if __name__ == "__main__":
    run_worker()
