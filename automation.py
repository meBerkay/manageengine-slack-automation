import requests
import sys
import json
import datetime
#request paketi kurulumu için -pip install requests- kullanılmalı.

# Dosya adını al
filename = str(sys.argv[1])

# JSON dosyasını oku
with open(filename, encoding='utf-8') as data_file:
    data = json.load(data_file)

requestObj = data['request']

# Verileri değişkenlere atama
workorderid = requestObj['id']
requester = requestObj['requester']['name']
createdby = requestObj['created_by']['name']
priority = requestObj.get('priority', {}).get('name', '-')  # 'priority' yoksa '-'
subject = requestObj.get('subject', 'Belirtilmemiş')  # 'subject' yoksa 'Belirtilmemiş'

# Technician bilgisi ve etiket seçimi (Slack tarafından alınan userId ile mention yapılması sağlanıyor.)
technician = requestObj.get('technician', {}).get('name', 'Belirtilmemiş')  # 'technician' yoksa 'Belirtilmemiş'
if technician == "John Doe":
    technician_mention = "<@USER1234>"
elif technician == "Jane Smith":
    technician_mention = "<@USER5678>"
elif technician == "Alex Johnson":
    technician_mention = "<@USER91011>"
elif technician == "Chris Lee":
    technician_mention = "<@USER12131>"
else:
    technician_mention = "Teknisyen Belirtilmemiş."  # Teknisyeni belirtmek için mesajı buraya ekleyebilirsiniz

channel = "#supportchannel"
CREATEDTIME = requestObj['created_time']['value']
scheduledstarttime = datetime.datetime.fromtimestamp(int(CREATEDTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')

# Formatlanmış payload
#url_template ile manage engine service desk plus ticket görüntüleme linkini aşağıya bu şekilde eklemelisiniz.
url_template = "https://example.com/WorkOrder.do?woMode=viewWO&woID="
url_with_id = url_template + workorderid
payload = {
    "channel": channel,
    "text": (
        "*Yeni bir destek talebi oluşturuldu.*\n\n"
        "⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n"
        f"**Konu:** {subject}\n"
        f"**Bilete Gitmek İçin:** <{url_with_id}|Tıklayın>\n"
        f"**Öncelik:** {priority}\n"
        f"**Oluşturulma Zamanı:** {scheduledstarttime}\n"
        f"**Oluşturan:** {createdby}\n"
        f"**Talebi Yapan:** {requester}\n"
        f"**Teknisyen:** {technician_mention}"
    )
}

# Slack Webhook URL
slack_webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

# Mesajı Slack'e gönder
response = requests.post(slack_webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

# Response kontrolü
if response.status_code == 200:
    print("Mesaj başarıyla gönderildi.")
else:
    print(f"Mesaj gönderilirken bir hata oluştu. Status code: {response.status_code}")
