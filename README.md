# Second-hand Listing Planner CLI

A simple and powerful terminal CLI tool written in Python that helps you prepare listing details, pricing strategies, photography guides, and ready-to-use advertisement drafts for items you want to sell second-hand. 

It leverages the **Gemini API** with **Google Search Grounding** to research real-time market data in Europe (specifically Germany/EU) on platforms like eBay, Vinted, and Kleinanzeigen.

## Features

- 🔍 **Real-Time Market Search:** Automatically searches the web for current prices and similar active listings.
- 💶 **Pricing Strategy:** Recommends minimum, maximum, average, and realistic starting prices in Euros (€).
- 📋 **Listing Checklist:** Identifies specific fields, attributes, and specifications you should look up for your item.
- 📸 **Photography Guide:** Suggestions on the angles, close-ups, and labels you should capture to build buyer trust.
- 📝 **Platform-Tailored Copy:** Generates optimized search-friendly titles and a complete listing description draft in either English or German.
- 🎨 **Beautiful CLI Output:** Uses the `rich` library to print a clean, colored, formatted Markdown report right in your terminal.

---

## Installation

1. **Clone or navigate** to the project directory:
   ```bash
   cd google-cloud-serverless-app
   ```

2. **Create a virtual environment** and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

The application requires a Gemini API key. You can get one from the [Google AI Studio](https://aistudio.google.com/).

Set the key as an environment variable in your terminal:

```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

*Tip: Add this line to your `~/.zshrc` or `~/.bashrc` file to make it permanent.*

---

## Usage

Run the script by providing the item name as a positional argument. By default, it will target **Kleinanzeigen** and generate output in **German**.

### Basic Usage (German, Kleinanzeigen)

```bash
python planner.py "iPhone 13 128GB schwarz"
```

### Advanced Usage

You can change the target platform, output language, or underlying model:

```bash
python planner.py [ITEM_NAME] [OPTIONS]
```

#### Options:
- `-p`, `--platform`: Target platform. Choices: `ebay`, `kleinanzeigen`, `vinted`, `facebook`, `generic` (default: `kleinanzeigen`).
- `-l`, `--lang`: Output language. Choices: `de` (German), `en` (English) (default: `de`).
- `-m`, `--model`: Gemini model. (default: `gemini-2.5-flash`).

### Examples

**Sell sneakers on Vinted (in German):**
```bash
python planner.py "Adidas Ultraboost 1.0 Triple Black Size 44" --platform vinted
```

**Sell a chair on Facebook Marketplace (in English):**
```bash
python planner.py "Herman Miller Aeron Chair Size B" --platform facebook --lang en
```

**Sell a camera on eBay (in English):**
```bash
python planner.py "Sony A6400 with 16-50mm kit lens" --platform ebay --lang en
```

---

## Output Structure

The tool outputs a report with five key sections:
1. **Pricing Strategy:** Average, high, and low pricing found from grounding search.
2. **Details Checklist:** Specs to look up (firmware, model numbers, dimensions).
3. **Photography Guide:** Angles and detail shots required to show the item condition.
4. **Optimized Title:** A search-friendly listing title.
5. **Description Draft:** A copy-pasteable draft containing structured headers (Description, Condition, Shipping, etc.) and placeholders for your specific item details

---

Implementation with Antigravity - Google's agentic vibe coding platform for software development.
