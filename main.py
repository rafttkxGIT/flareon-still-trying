# Replace the contents of your main.py file on GitHub with this code:

import os
import threading
import app
import bot

def run_flask():
    # Railway passes the correct port via environment variable
    port = int(os.environ.get("PORT", 8080))
    app.app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot():
    bot.main()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    run_bot()
