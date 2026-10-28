ShopBondhu + Telegram bot starter

Files:
- index.html: ShopBondhu mobile storefront with Premium Package (৳100) and Special Package (৳200) cards added.
- bot.py: Telegram bot code, kept separate because Python cannot run directly inside an HTML file.

Run the Telegram bot:
1. Install Python 3.10+.
2. In a terminal, install the dependency:
   pip install "python-telegram-bot>=20,<23"
3. Set your bot token as an environment variable named BOT_TOKEN.
   Linux/macOS: export BOT_TOKEN="YOUR_BOT_TOKEN"
   Windows PowerShell: $env:BOT_TOKEN="YOUR_BOT_TOKEN"
4. Optional admin order alerts: set ADMIN_CHAT_ID to the admin's numeric Telegram chat ID.
   Linux/macOS: export ADMIN_CHAT_ID="123456789"
   Windows PowerShell: $env:ADMIN_CHAT_ID="123456789"
5. Run: python bot.py

Important:
- Do not put BOT_TOKEN in index.html or any public frontend code.
- The HTML storefront is a frontend demo. Its checkout is not connected to the Telegram bot/backend yet; a hosted backend/API is needed for web orders to reach Telegram.
- No real payment is processed by this demo. Verify payments manually and securely.
