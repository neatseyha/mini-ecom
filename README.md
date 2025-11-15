# Mini E-Commerce with Telegram Bot Integration

A Flask-based e-commerce web application that sends order notifications to Telegram.

## Features

- 🏠 **Home Page**: Featured products and store information
- 🛍️ **Shop Page**: Browse all available products
- 🛒 **Shopping Cart**: Add, update, and remove items
- 💳 **Checkout**: Complete order with customer information
- 📱 **Telegram Integration**: Automatic order notifications sent to Telegram
- 📧 **Contact Form**: Customer inquiries sent via Telegram
- ℹ️ **About Us**: Store information and features

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Telegram Chat ID

## Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the **Bot Token** provided

### 2. Get Your Chat ID

1. Search for `@userinfobot` in Telegram
2. Start a chat with it
3. It will send you your Chat ID
4. Copy this ID

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   SECRET_KEY=your_secret_key_here
   ```

### 5. Run the Application

```powershell
python app.py
```

The application will start at `http://127.0.0.1:5000`

## Project Structure

```
bos ke/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── telegram_bot.py        # Telegram bot integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── script.js     # JavaScript functionality
└── templates/
    ├── base.html         # Base template
    ├── home.html         # Home page
    ├── shop.html         # Shop page
    ├── cart.html         # Shopping cart
    ├── checkout.html     # Checkout page
    ├── order_success.html # Order confirmation
    ├── about.html        # About us page
    └── contact.html      # Contact page
```

## How It Works

1. **Shopping**: Customers browse products and add them to their cart
2. **Cart Management**: Adjust quantities or remove items from cart
3. **Checkout**: Enter shipping information
4. **Order Notification**: Order details are automatically sent to your Telegram chat
5. **Confirmation**: Customer sees a success page

## Telegram Notifications

When an order is placed, you'll receive a Telegram message with:

- Customer name, email, phone, and address
- List of ordered items with quantities
- Total order amount

## Customization

### Add More Products

Edit the `PRODUCTS` list in `app.py`:

```python
PRODUCTS = [
    {
        'id': 7,
        'name': 'New Product',
        'price': 99.99,
        'image': 'https://example.com/image.jpg',
        'description': 'Product description'
    },
    # ... more products
]
```

### Change Styling

Modify `static/css/style.css` to customize colors, fonts, and layout.

### Add Payment Gateway

To add real payment processing:

1. Choose a payment provider (Stripe, PayPal, etc.)
2. Install their Python library
3. Add payment processing in the checkout route
4. Update the checkout form with payment fields

## Security Notes

- Never commit `.env` file to version control
- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Validate and sanitize all user inputs
- Add CSRF protection for production use

## Troubleshooting

**Issue**: Telegram notifications not working

- Check that your bot token is correct
- Verify your chat ID is correct
- Make sure you've started a chat with your bot first

**Issue**: Import errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Session not persisting

- Ensure `SECRET_KEY` is set in your `.env` file

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, use the contact form in the application or check the code comments.
