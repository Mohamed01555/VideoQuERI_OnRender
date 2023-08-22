from uuid import uuid4
from re import findall
import tls_client

# ch = [chrome_103, chrome_104, chrome_105, chrome_106, chrome_107, chrome_108, chrome109, Chrome110, chrome111, chrome112, 
#       firefox_102, firefox_104, firefox108, Firefox110,
#       opera_89, opera_90,
#       safari_15_3, safari_15_6_1, safari_16_0,
#       safari_ios_15_5, safari_ios_15_6, safari_ios_16_0,
#       safari_ios_15_6,
#       okhttp4_android_7, okhttp4_android_8, okhttp4_android_9, okhttp4_android_10, okhttp4_android_11, okhttp4_android_12, okhttp4_android_13]


class Completion:
    async def create(self, prompt):
        """
        Create a completion for the given prompt using the you.com API.

        Args:
            prompt (str): The prompt for which completion is requested.
            proxy (str, optional): The proxy to be used for the API request. Defaults to None.

        Returns:
            str: The completion result as a string.

        Raises:
            Exception: If unable to fetch the response or the required token from the response.
        """
        client = tls_client.Session(client_identifier='firefox_102')
        client.headers = {
            "authority": "you.com",
            "accept": "text/event-stream",
            "accept-language": "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "cache-control": "no-cache",
            "referer": "https://you.com/search?q=who+are+you&tbm=youchat",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            "user-agent": "Mozilla/5.0 (Windows NT 5.1; U;  ; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.52",
        }
        params = {
            "q": prompt,
            "page": 1,
            "count": 10,
            "safeSearch": "Off",
            "onShoppingPage": False,
            "mkt": "",
            "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
            "domain": "youchat",
            "queryTraceId": str(uuid4()),
            "chat": [],
        }
        resp = client.get(
            "https://you.com/api/streamingSearch", params=params, timeout_seconds=30
        )
        
        if "youChatToken" not in resp.text:
            raise Exception("Unable to fetch response.")
        return (
            "".join(findall(r"{\"youChatToken\": \"(.*?)\"}", resp.text))
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
        )
    
