# Gmailnator Service - Användningsguide

## Översikt
`gmailnator_service.py` är en Python-modul som integrerar med Gmailnator (Emailnator) API för att generera och hantera temporära e-postadresser. Detta är användbart för automatisk kontoregistrering och verifiering.

## Installation

### Förutsättningar
```bash
# Python 3.7 eller senare
python3 --version

# Installera Playwright (valfritt, för browser automation)
pip install playwright
playwright install
```

### API-nyckel
1. Skaffa en RapidAPI-nyckel från: https://rapidapi.com/Privatix/api/gmailnator
2. Sätt miljövariabeln:
   ```bash
   export RAPIDAPI_KEY='your_key_here'
   ```
   
   Eller skapa en `.env` fil:
   ```
   RAPIDAPI_KEY=your_key_here
   ```

## Snabbstart

### Grundläggande användning
```python
from gmailnator_service import GmailnatorService

# Initialisera service (API-nyckel från miljövariabel)
service = GmailnatorService()

# Generera en temporär e-post
email = service.generate_email(options=[1])
print(f"Temporär e-post: {email}")

# Vänta på meddelanden (efter registrering)
import time
time.sleep(10)

# Hämta inbox
messages = service.get_inbox(email, limit=5)
for msg in messages:
    print(f"Från: {msg.get('from')}, Ämne: {msg.get('subject')}")
```

### Komplett registreringsflöde
Se `example_integration.py` för ett fullständigt exempel med Playwright integration.

## API Metoder

### `generate_email(options=[1])`
Generera en enskild temporär e-postadress.

**Parametrar:**
- `options` (list): Välj typ av e-post
  - `[1]` - Public domain mail (standard)
  - `[2]` - Public Plus(+) Gmail
  - `[3]` - Public Dot(.) Gmail
  - `[4]` - Private domain mail
  - `[5]` - Private Plus(+) Gmail
  - `[6]` - Private Dot(.) Gmail
  - `[8]` - Public Googlemail
  - `[9]` - Private Googlemail

**Returnerar:** E-postadress (string)

**Exempel:**
```python
email = service.generate_email(options=[1])
```

---

### `generate_bulk_emails(limit, options=[1])`
Generera flera temporära e-postadresser samtidigt.

**Parametrar:**
- `limit` (int): Antal e-postadresser (max 500)
- `options` (list): Typ av e-post (samma som generate_email)

**Returnerar:** Lista med e-postadresser

**Exempel:**
```python
emails = service.generate_bulk_emails(limit=10, options=[1, 2])
# ['test1@gmail.com', 'test2@gmail.com', ...]
```

---

### `get_inbox(email, limit=10)`
Hämta meddelanden från en temporär e-postadress.

**Parametrar:**
- `email` (str): E-postadressen att hämta meddelanden från
- `limit` (int): Antal meddelanden att hämta (max 20)

**Returnerar:** Lista med meddelanden

**Exempel:**
```python
messages = service.get_inbox('test@gmail.com', limit=5)
for msg in messages:
    print(msg.get('subject'))
```

---

### `get_message(message_id)`
Hämta fullständigt innehåll för ett specifikt meddelande.

**Parametrar:**
- `message_id` (str): Unikt meddelande-ID (från inbox)

**Returnerar:** Meddelandeinnehåll (dict)

**Exempel:**
```python
messages = service.get_inbox(email)
if messages:
    full_message = service.get_message(messages[0]['messageID'])
    print(full_message.get('content'))
```

---

### `delete_message(message_id)`
Radera ett meddelande efter användning.

**Parametrar:**
- `message_id` (str): Meddelande-ID att radera

**Returnerar:** API response (dict)

**Exempel:**
```python
service.delete_message(message_id)
```

---

### `extract_verification_link(message_content)`
Hjälpfunktion för att extrahera verifieringslänkar från meddelanden.

**Parametrar:**
- `message_content` (str eller dict): Meddelandeinnehåll

**Returnerar:** URL (string) eller None

**Exempel:**
```python
from gmailnator_service import extract_verification_link

message = service.get_message(message_id)
link = extract_verification_link(message)
if link:
    print(f"Verifieringslänk: {link}")
```

## Typiskt Workflow

```python
from gmailnator_service import GmailnatorService, extract_verification_link
import time

# 1. Skapa service
service = GmailnatorService()

# 2. Generera temporär e-post
temp_email = service.generate_email(options=[1])
print(f"Använd denna e-post: {temp_email}")

# 3. Fyll i registreringsformulär (manuellt eller med Playwright)
# ... registrera konto med temp_email ...

# 4. Vänta på verifieringsmail
time.sleep(10)

# 5. Hämta inbox
messages = service.get_inbox(temp_email, limit=1)

if messages:
    # 6. Hämta meddelandet
    message = service.get_message(messages[0]['messageID'])
    
    # 7. Extrahera verifieringslänk
    link = extract_verification_link(message)
    
    if link:
        print(f"Besök denna länk: {link}")
        # ... navigera till länken med Playwright ...
    
    # 8. Rensa upp
    service.delete_message(messages[0]['messageID'])
```

## Integration med Playwright

```python
from playwright.async_api import async_playwright
from gmailnator_service import GmailnatorService, extract_verification_link
import asyncio

async def register_account():
    service = GmailnatorService()
    temp_email = service.generate_email(options=[1])
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Registrera
        await page.goto('https://example.com/register')
        await page.fill('input[name="email"]', temp_email)
        await page.fill('input[name="password"]', 'SecurePass123!')
        await page.click('button[type="submit"]')
        
        # Vänta på mail
        await asyncio.sleep(10)
        
        # Hämta och besök verifieringslänk
        messages = service.get_inbox(temp_email, limit=1)
        if messages:
            message = service.get_message(messages[0]['messageID'])
            link = extract_verification_link(message)
            
            if link:
                await page.goto(link)
                print("Konto verifierat!")
            
            service.delete_message(messages[0]['messageID'])
        
        await browser.close()

asyncio.run(register_account())
```

## Felsökning

### "API key krävs"
- Kontrollera att `RAPIDAPI_KEY` är satt som miljövariabel
- Eller skicka API-nyckeln direkt: `GmailnatorService(api_key='your_key')`

### "Inga meddelanden hittades"
- Öka väntetiden mellan registrering och inbox-polling
- Kontrollera att registreringen lyckades
- Vissa tjänster kan ta längre tid att skicka mail

### "Ingen verifieringslänk hittades"
- Kontrollera meddelandets innehåll manuellt
- Vissa mail kan ha länkar i HTML-format som inte matchas av regex
- Utöka `extract_verification_link()` med fler mönster om nödvändigt

## API Begränsningar
- Max 500 e-postadresser per bulk-generering
- Max 20 meddelanden per inbox-hämtning
- Rate limits enligt ditt RapidAPI-abonnemang

## Relaterade Filer
- `docs/gmailnator_api.md` - Fullständig API-dokumentation
- `example_integration.py` - Kompletta användningsexempel
- `.env-exmpel` - Miljövariabel mall

## Support
För problem eller frågor, se:
- Gmailnator API dokumentation: https://rapidapi.com/Privatix/api/gmailnator
- Projektets huvuddokumentation: `README.md`
