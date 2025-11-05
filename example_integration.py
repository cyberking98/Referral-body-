"""
Exempel på integration mellan Gmailnator och Playwright
Visar hur man använder temporär e-post för automatisk kontoregistrering
"""

import asyncio
import os
from gmailnator_service import GmailnatorService, extract_verification_link


async def example_registration_flow():
    """
    Exempel på komplett registreringsflöde med temporär e-post.
    
    Detta exempel visar:
    1. Generera temporär e-post
    2. Fyll i registreringsformulär (Playwright)
    3. Vänta på verifieringsmail
    4. Extrahera och besök verifieringslänk
    5. Rensa upp meddelanden
    """
    
    # Initialisera Gmailnator service
    # API-nyckel hämtas från miljövariabel RAPIDAPI_KEY
    gmail_service = GmailnatorService()
    
    print("=== Steg 1: Generera temporär e-post ===")
    temp_email = gmail_service.generate_email(options=[1])
    print(f"Genererad e-post: {temp_email}")
    
    # Här skulle Playwright-kod komma för att:
    # - Navigera till registreringssidan
    # - Fylla i formulär med temp_email
    # - Klicka på registrera
    
    print("\n=== Steg 2: Simulerar formulärifyllning med Playwright ===")
    print("# OBS: Detta kräver Playwright installation och konfiguration")
    print("# Exempel (kommenterad kod):")
    print("""
    # from playwright.async_api import async_playwright
    # 
    # async with async_playwright() as p:
    #     browser = await p.chromium.launch(headless=False)
    #     page = await browser.new_page()
    #     
    #     # Navigera till registreringssida
    #     await page.goto('https://example.com/register')
    #     
    #     # Fyll i formulär
    #     await page.fill('input[name="email"]', temp_email)
    #     await page.fill('input[name="password"]', 'SecurePass123!')
    #     await page.click('button[type="submit"]')
    #     
    #     # Vänta på bekräftelse
    #     await page.wait_for_selector('.success-message')
    """)
    
    print("\n=== Steg 3: Vänta på verifieringsmail ===")
    print("Väntar 10 sekunder på att mail ska komma...")
    await asyncio.sleep(10)
    
    print("\n=== Steg 4: Hämta inbox och leta efter verifieringsmail ===")
    try:
        messages = gmail_service.get_inbox(temp_email, limit=5)
        print(f"Antal meddelanden i inbox: {len(messages)}")
        
        if messages:
            print("\n=== Steg 5: Hämta första meddelandet ===")
            first_message = messages[0]
            print(f"Meddelande ID: {first_message.get('messageID', 'N/A')}")
            
            # Hämta fullständigt meddelandeinnehåll
            message_id = first_message.get('messageID')
            if message_id:
                full_message = gmail_service.get_message(message_id)
                print(f"Meddelandeämne: {full_message.get('subject', 'N/A')}")
                
                # Extrahera verifieringslänk
                verification_link = extract_verification_link(full_message)
                
                if verification_link:
                    print(f"\n=== Steg 6: Verifieringslänk hittad ===")
                    print(f"Länk: {verification_link}")
                    
                    # Här skulle Playwright navigera till verifieringslänken
                    print("\n# Playwright kod för att besöka verifieringslänken:")
                    print(f"# await page.goto('{verification_link}')")
                    
                    # Radera meddelandet efter användning
                    print("\n=== Steg 7: Rensa upp - radera meddelande ===")
                    result = gmail_service.delete_message(message_id)
                    print(f"Meddelande raderat: {result}")
                else:
                    print("⚠️ Ingen verifieringslänk hittades i meddelandet")
        else:
            print("⚠️ Inga meddelanden hittades i inbox")
            print("Detta kan bero på:")
            print("- Mailet har inte kommit än (öka väntetiden)")
            print("- E-postadressen är inte giltig")
            print("- Registreringen misslyckades")
    
    except Exception as e:
        print(f"❌ Fel vid hämtning av meddelanden: {e}")
    
    print("\n=== Exempel slutfört ===")


async def example_bulk_email_generation():
    """Exempel på att generera flera e-postadresser samtidigt."""
    
    gmail_service = GmailnatorService()
    
    print("=== Generera 5 temporära e-postadresser ===")
    emails = gmail_service.generate_bulk_emails(limit=5, options=[1, 2])
    
    print(f"Genererade {len(emails)} e-postadresser:")
    for i, email in enumerate(emails, 1):
        print(f"{i}. {email}")


def example_simple_usage():
    """Enkelt synkront exempel."""
    
    # Sätt API-nyckel (i praktiken använd miljövariabel)
    # os.environ['RAPIDAPI_KEY'] = 'your_key_here'
    
    print("=== Enkel användning av Gmailnator Service ===\n")
    
    try:
        service = GmailnatorService()
        
        # Generera en e-post
        email = service.generate_email(options=[1])
        print(f"✅ Genererad e-post: {email}")
        
        # Tips för vidare användning
        print("\nNästa steg:")
        print("1. Använd denna e-post i ditt registreringsformulär")
        print("2. Vänta några sekunder")
        print("3. Hämta inbox med: service.get_inbox(email)")
        print("4. Extrahera verifieringslänk från meddelandet")
        print("5. Navigera till länken med Playwright")
        
    except ValueError as e:
        print(f"❌ Konfigurationsfel: {e}")
        print("\nFör att använda detta exempel:")
        print("1. Hämta API-nyckel från: https://rapidapi.com/Privatix/api/gmailnator")
        print("2. Sätt miljövariabel: export RAPIDAPI_KEY='your_key_here'")
        print("3. Eller skapa .env fil med: RAPIDAPI_KEY=your_key_here")
    except Exception as e:
        print(f"❌ Fel: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("GMAILNATOR + PLAYWRIGHT INTEGRATION EXEMPEL")
    print("=" * 60)
    print()
    
    # Kör enkelt synkront exempel
    example_simple_usage()
    
    print("\n" + "=" * 60 + "\n")
    
    # För att köra async exemplen, avkommentera:
    # asyncio.run(example_registration_flow())
    # asyncio.run(example_bulk_email_generation())
    
    print("\nFör att köra de fullständiga async exemplen:")
    print("1. Installera Playwright: pip install playwright")
    print("2. Installera browsers: playwright install")
    print("3. Avkommentera async exemplen i koden")
    print("4. Kör scriptet igen")
