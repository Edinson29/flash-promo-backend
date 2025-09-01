import os
import firebase_admin
from firebase_admin import credentials, messaging

# path file firebase.json
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "../firebase.json")


class FirebaseService:
    """
    Firebase Service class
    """

    def __init__(self):
        """
        Init method class
        """
        try:
            firebase_admin.get_app()
            firebase_admin.delete_app(firebase_admin.get_app())
        except ValueError:
            pass
        self.firebase_cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        self.firebase_app = firebase_admin.initialize_app(self.firebase_cred)

    def send_notifications_in_batches(self, device_tokens, title, body):
        """
        Send notifications in batches of 500
        """

        # Firebase allows a maximum of 500 tokens per batch
        BATCH_SIZE = 500
        for i in range(0, len(device_tokens), BATCH_SIZE):
            batch_tokens = device_tokens[i : i + BATCH_SIZE]
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=str(body)),
                tokens=batch_tokens,
            )
            response = messaging.send_each_for_multicast(message)
            for idx, resp in enumerate(response.responses):
                if resp.success:
                    print(f"✅ Notificación enviada a {batch_tokens[idx]}")
                else:
                    print(f"❌ Error con {batch_tokens[idx]}: {resp.exception}")
