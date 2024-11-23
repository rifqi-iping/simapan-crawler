import re
import requests
import html5lib
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt

console = Console()

console.print('Masukkan NIP:')
nip = Prompt.ask('Masukkan NIP:')
jangkau = Prompt.ask('Masukkan NIP:')

r = requests.post('https://daftar.bpsdmd.jatengprov.go.id/events-opd/index.php?halaman=cari_data&id_event=714', 
    data={'nip_peserta': '197602061999032001', 'id_event': '714', 'simpan': ''},
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
)
soup = BeautifulSoup(r.content, 'html5lib')
text = str(soup.findAll('script', type='text/javascript')[1])
link = re.findall("e_sertifikat.*';", text)
link = link[0].replace("';", "")
namafile = link.replace('e_sertifikat.php?no_sertifikat=','')+'.pdf'
link = f'https://daftar.bpsdmd.jatengprov.go.id/events-opd/{link}'
with requests.get(link, stream=True) as r:
    with open(namafile, mode="wb") as file:
        for chunk in r.iter_content(chunk_size=10 * 1024):
            file.write(chunk)