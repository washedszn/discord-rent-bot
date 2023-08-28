# Discord Property Bot

A Discord bot that fetches property listings from estate agents based on the specified city and notifies a specific channel with details of the property.

**Currently supported Estate Agents:**

 - Nederwoon

## Setup

1. **Clone the repository**:

   ```
   git clone [URL of your repository]
   ```

2. **Setup your environment**:

   Rename `.env.example` to `.env` and replace the placeholders with your actual Discord bot token.

   ```env
   DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
   ```

3. **Setup the bot's configuration**:

   Rename `config.json.example` to `config.json`. 

   The file contains the following fields:
   - `CHANNEL_ID`: The ID of the Discord channel where the bot will send property notifications.
   - `CHECK_INTERVAL_SECONDS`: How often the bot will check for new properties.
   - `CITY`: The city you want to search for properties in.

   Fill in these fields as per your requirements.

4. **Run the bot**:

   ```
   python bot.py
   ```

## Discord Commands

- `set-channel`: Set the channel which will receive the property notifications.
- `set-city [city name]`: Set the desired city for scraping.
- `set-interval [interval in seconds]`: Set the interval for checking listings (Minimum is 60 seconds).

## Note

Ensure you have the necessary Python packages installed. You can install them using:

```
pip install -r requirements.txt
```
