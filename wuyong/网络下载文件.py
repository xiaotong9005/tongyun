import urllib 
import requests
url = 'http://img.hb.aicdn.com/05e739dc26ab56f033d871b98290c367f4ab30612bcbd-4842UI_fw658'  
r = requests.get(url=url)  
with open('demo.zip', 'wb') as f :  
    f.write(r.content)
