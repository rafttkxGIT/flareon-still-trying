import threading
import app
import bot

def run_flask():
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

def run_bot():
    bot.main()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    run_bot()
