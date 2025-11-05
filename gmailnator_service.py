"""
Gmailnator (Emailnator) API Service
Temporär e-posttjänst för automatiserad kontoregistrering.

API Host: gmailnator.p.rapidapi.com
Dokumentation: docs/gmailnator_api.md
"""

import http.client
import json
import os
from typing import List, Dict, Optional, Union


class GmailnatorService:
    """Service klass för Gmailnator API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialisera Gmailnator service.
        
        Args:
            api_key: RapidAPI nyckel. Om None, hämtas från miljövariabel RAPIDAPI_KEY
        """
        self.host = "gmailnator.p.rapidapi.com"
        self.api_key = api_key or os.getenv('RAPIDAPI_KEY')
        
        if not self.api_key:
            raise ValueError("API key krävs. Sätt RAPIDAPI_KEY miljövariabel eller skicka som parameter.")
        
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': self.host
        }
    
    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict:
        """
        Gör en HTTP request till Gmailnator API.
        
        Args:
            method: HTTP metod (GET, POST)
            endpoint: API endpoint
            payload: Optional request body för POST requests
            
        Returns:
            Parsed JSON response
            
        Raises:
            Exception: Om request misslyckas
        """
        conn = http.client.HTTPSConnection(self.host)
        
        try:
            headers = self.headers.copy()
            
            if method == "POST" and payload:
                headers['Content-Type'] = 'application/json'
                body = json.dumps(payload)
                conn.request(method, endpoint, body, headers)
            else:
                conn.request(method, endpoint, headers=headers)
            
            response = conn.getresponse()
            data = response.read()
            
            # Parse JSON response
            result = json.loads(data.decode("utf-8"))
            
            return result
            
        except Exception as e:
            raise Exception(f"Gmailnator API request misslyckades: {str(e)}")
        finally:
            conn.close()
    
    def generate_email(self, options: List[int] = [1]) -> str:
        """
        Generera en temporär e-postadress.
        
        Args:
            options: Lista med alternativ [1,2,3,4,5,6,8,9]
                1 - Public domain mail
                2 - Public Plus(+) Gmail
                3 - Public Dot(.) Gmail
                4 - Private domain mail
                5 - Private Plus(+) Gmail
                6 - Private Dot(.) Gmail
                8 - Public Googlemail
                9 - Private Googlemail
        
        Returns:
            Genererad e-postadress
        """
        payload = {"options": options}
        response = self._make_request("POST", "/generate-email", payload)
        
        # Response innehåller e-postadressen
        if isinstance(response, dict) and 'email' in response:
            return response['email']
        elif isinstance(response, str):
            return response
        else:
            raise Exception(f"Oväntat response format: {response}")
    
    def generate_bulk_emails(self, limit: int, options: List[int] = [1]) -> List[str]:
        """
        Generera flera temporära e-postadresser samtidigt.
        
        Args:
            limit: Antal e-postadresser (max 500)
            options: Lista med alternativ [1,2,3,4,5,6,8,9]
        
        Returns:
            Lista med genererade e-postadresser
        """
        if limit > 500:
            raise ValueError("Max 500 e-postadresser kan genereras åt gången")
        
        payload = {
            "limit": limit,
            "option": options
        }
        response = self._make_request("POST", "/bulk-emails", payload)
        
        if isinstance(response, list):
            return response
        else:
            raise Exception(f"Oväntat response format: {response}")
    
    def get_inbox(self, email: str, limit: int = 10) -> List[Dict]:
        """
        Hämta meddelanden från inbox för en e-postadress.
        
        Args:
            email: E-postadressen att hämta meddelanden från
            limit: Antal meddelanden att hämta (max 20)
        
        Returns:
            Lista med meddelanden
        """
        if limit > 20:
            raise ValueError("Max 20 meddelanden kan hämtas åt gången")
        
        payload = {
            "email": email,
            "limit": limit
        }
        response = self._make_request("POST", "/inbox", payload)
        
        if isinstance(response, list):
            return response
        else:
            raise Exception(f"Oväntat response format: {response}")
    
    def get_message(self, message_id: str) -> Dict:
        """
        Hämta ett specifikt meddelande baserat på ID.
        
        Args:
            message_id: Unikt meddelande-ID (krypterad sträng)
        
        Returns:
            Meddelandeinnehåll
        """
        endpoint = f"/messageid?id={message_id}"
        response = self._make_request("GET", endpoint)
        return response
    
    def delete_message(self, message_id: str) -> Dict:
        """
        Radera ett specifikt meddelande.
        
        Args:
            message_id: Unikt meddelande-ID att radera
        
        Returns:
            API response
        """
        endpoint = f"/delete?id={message_id}"
        response = self._make_request("GET", endpoint)
        return response


# Hjälpfunktioner för vanliga workflows
def extract_verification_link(message_content: Union[str, Dict]) -> Optional[str]:
    """
    Extrahera verifieringslänk från meddelandeinnehåll.
    
    Args:
        message_content: Meddelandeinnehåll (sträng eller dict)
    
    Returns:
        Verifieringslänk om den hittas, annars None
    """
    import re
    
    # Om message_content är en dict, försök hitta textinnehållet
    if isinstance(message_content, dict):
        text = message_content.get('messageData', '') or message_content.get('content', '') or str(message_content)
    else:
        text = str(message_content)
    
    # Vanliga mönster för verifieringslänkar
    url_patterns = [
        r'https?://[^\s<>"]+?verify[^\s<>"]*',
        r'https?://[^\s<>"]+?confirm[^\s<>"]*',
        r'https?://[^\s<>"]+?activation[^\s<>"]*',
        r'https?://[^\s<>"]+?token=[^\s<>"]+',
    ]
    
    for pattern in url_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


# Exempel på användning
if __name__ == "__main__":
    # Detta kräver att RAPIDAPI_KEY är satt som miljövariabel
    try:
        service = GmailnatorService()
        
        # Generera en temporär e-post
        email = service.generate_email(options=[1])
        print(f"Genererad e-post: {email}")
        
        # Vänta på meddelanden (i verklig användning, gör detta efter registrering)
        # import time
        # time.sleep(10)
        
        # Hämta inbox
        # messages = service.get_inbox(email, limit=5)
        # print(f"Antal meddelanden: {len(messages)}")
        
        # if messages:
        #     # Hämta första meddelandet
        #     message = service.get_message(messages[0]['id'])
        #     print(f"Meddelande: {message}")
        #     
        #     # Extrahera verifieringslänk
        #     link = extract_verification_link(message)
        #     if link:
        #         print(f"Verifieringslänk: {link}")
        #     
        #     # Radera meddelandet
        #     service.delete_message(messages[0]['id'])
        
    except Exception as e:
        print(f"Fel: {e}")
