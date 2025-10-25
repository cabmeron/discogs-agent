# 🎵 Discogs Marketplace Assistant

An AI-powered agent built with Google's Agent Development Kit (ADK) that helps you search the Discogs database, get marketplace pricing information, and analyze music releases. Features a command-line interface

--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------

User: What's the cheapest Nirvana album on Discogs?

Agent: I searched for Nirvana albums and found several options with marketplace pricing:

1. **Nevermind** (1991)
   - Lowest Price: $12.99 USD
   - Active Listings: 2,847
   - Format: Various (CD, Vinyl, Cassette)

2. **Bleach** (1989)
   - Lowest Price: $15.50 USD
   - Active Listings: 1,234
   - Format: Various

3. **In Utero** (1993)
   - Lowest Price: $14.25 USD
   - Active Listings: 1,892
   - Format: Various

The cheapest option is currently a copy of Nevermind at $12.99 USD. Note that prices 
vary based on format, condition, and edition. Would you like more details about a 
specific release?

--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange.svg)

## ✨ Features

- **🔍 Search Discogs Database**: Find albums, releases, and artists across the entire Discogs catalog
- **💰 Marketplace Pricing**: Get real-time lowest prices and listing counts from Discogs marketplace
- **📊 Release Details**: Retrieve comprehensive information including tracklists, formats, and metadata
- **🤖 AI-Powered Chat**: Natural language interface powered by Google Gemini

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google AI API key ([Get one here](https://aistudio.google.com/apikey))
- Discogs API token ([Get one here](https://www.discogs.com/settings/developers))

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/cabmeron/discogs-agent.git](https://github.com/cabmeron/discogs-agent.git)
   ```

   ```bash
   cd discogs-agent
   ```
   
2. **Add Api Keys**

   ```bash
   touch .env
   ```

   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   DISCOGS_API_KEY=your_discogs_token_here
   ```
3. **Install Dependencies**
   ```bash
   pip install rquirements.txt
   ```
4. **Run Agent**

  ```bash
  adk run discogs-agent
  ```

