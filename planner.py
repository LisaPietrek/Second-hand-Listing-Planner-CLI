#!/usr/bin/env python3
import os
import sys
import argparse
from google import genai
from google.genai import types
from google.genai.errors import APIError
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Initialize rich console for beautiful terminal output
console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Second-hand Listing Planner - Search market prices and generate listing drafts."
    )
    parser.add_argument(
        "item",
        type=str,
        help="The description of the item you want to sell (e.g., 'iPhone 13 Pro 128GB Space Gray')."
    )
    parser.add_argument(
        "-p", "--platform",
        type=str,
        default="kleinanzeigen",
        choices=["ebay", "kleinanzeigen", "vinted", "facebook", "generic"],
        help="The target platform for your listing (default: kleinanzeigen)."
    )
    parser.add_argument(
        "-l", "--lang",
        type=str,
        default="de",
        choices=["de", "en"],
        help="Language for the generated listing and report (de for German, en for English, default: de)."
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="gemini-2.5-flash",
        help="Gemini model to use (default: gemini-2.5-flash)."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # 1. Check API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        console.print(
            Panel(
                "[bold red]Error: GEMINI_API_KEY environment variable is not set.[/bold red]\n\n"
                "Please set your Gemini API key in your terminal before running this script:\n"
                "[bold yellow]export GEMINI_API_KEY=\"your_api_key_here\"[/bold yellow]\n\n"
                "To get an API key, visit: https://aistudio.google.com/",
                title="Missing Configuration",
                border_style="red"
            )
        )
        sys.exit(1)
        
    console.print(f"[bold blue]Starting Second-hand Planner for:[/bold blue] '{args.item}'")
    console.print(f"[bold blue]Target Platform:[/bold blue] {args.platform.capitalize()}")
    console.print(f"[bold blue]Language:[/bold blue] {'German' if args.lang == 'de' else 'English'}")
    console.print(f"[bold blue]Using Model:[/bold blue] {args.model}")
    console.print("[cyan]Searching the web for current market pricing and details in Europe/Germany...[/cyan]")
    
    # 2. Initialize Gemini Client
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        console.print(f"[bold red]Failed to initialize Gemini Client:[/bold red] {e}")
        sys.exit(1)
        
    # Translate language code to full name for the prompt
    lang_name = "German" if args.lang == "de" else "English"
    
    # Define platform context
    platform_details = {
        "ebay": "eBay (Auction or Buy It Now, fee structure, detailed specifications, shipping options)",
        "kleinanzeigen": "Kleinanzeigen / eBay Kleinanzeigen (local pickup, cash or bank transfer/secure payment, friendly but concise description, negotiable price)",
        "vinted": "Vinted (clothing / fashion / small items, buyer protection fee, shipping via package shop, tag-heavy description)",
        "facebook": "Facebook Marketplace (local pickup or direct shipping, target local community, simplified description)",
        "generic": "General Classifieds"
    }
    
    platform_context = platform_details.get(args.platform.lower(), "General Classifieds")
    
    # 3. Construct prompt with search grounding instruction
    system_instruction = (
        "You are an expert second-hand selling assistant specializing in the European market (especially Germany). "
        "Your goal is to help users sell items by providing a highly detailed price analysis, data checklist, "
        "photography guide, and a high-quality listing title and description draft tailored to their target platform."
    )
    
    prompt = f"""
We want to prepare a second-hand listing for the following item:
Item: {args.item}
Target Platform: {args.platform} ({platform_context})
Target Market Area: Europe (specifically Germany)
Language of Output: {lang_name}

Please execute these steps:
1. Search the web for current second-hand listings, completed listings, and listings in progress of similar items in Germany and Europe (e.g. on eBay, Kleinanzeigen, Vinted).
2. Pricing Strategy:
   - Estimate the low, high, and average selling price in Euros (€).
   - Recommend a realistic listing price and whether the user should select "VB" (Verhandlungsbasis / negotiable) or fixed price.
3. Details Checklist:
   - Identify which exact technical specifications, model numbers, dimensions, or configuration details the seller MUST look up and state (e.g. battery health, storage capacity, fabric type, exact measurements).
4. Photography Guide:
   - Suggest which specific photos to take to build trust and show all necessary details (e.g. serial number label, close-ups of common wear areas, screen turned on showing stats, proof of authenticity).
5. Listing Copy:
   - Generate an optimized, catchy Listing Title (include keywords buyers search for).
   - Generate a complete, ready-to-copy listing Description Draft in {lang_name} tailored to the platform conventions. Use placeholders like [Insert condition details/flaws here] or [Insert battery state here] where appropriate, and structure it with sections like 'Specifications', 'Condition', 'Scope of Delivery', and 'Shipping/Pickup info'.

Please output the entire report as a single, beautifully structured Markdown document. Use tables for pricing comparison if possible. Do not output any chat meta-commentary, just begin with the Markdown.
"""

    # 4. Invoke API with Google Search grounding enabled
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                # Lower temperature for more analytical synthesis
                temperature=0.3,
            )
        )
    except APIError as api_err:
        console.print(f"[bold red]API Error from Gemini:[/bold red] {api_err}")
        console.print("[yellow]Please verify your API key is valid and you have access to the specified model.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error calling Gemini API:[/bold red] {e}")
        sys.exit(1)

    # 5. Extract grounding details (if any) to show the user the searches done
    try:
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.web_search_queries:
            console.print("\n[bold green]Web Searches Performed:[/bold green]")
            for query in metadata.web_search_queries:
                console.print(f"  • [cyan]{query}[/cyan]")
    except Exception:
        # Grounding metadata parsing is optional, skip if not present/accessible
        pass

    # 6. Render the Markdown output
    console.print("\n" + "="*80)
    if response.text:
        # Print a styled Markdown report using rich
        md = Markdown(response.text)
        console.print(md)
    else:
        console.print("[red]The model did not return any text response.[/red]")
    console.print("="*80 + "\n")

if __name__ == "__main__":
    main()
