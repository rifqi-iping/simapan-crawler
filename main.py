import re
import time
import requests
import html5lib
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt

console = Console()

console.print('[bold white]SIMAPAN BPSDMD Jateng Sertifikat Crawling by [bold red]rifqi.iping')
nip = Prompt.ask('Masukkan NIP/NIK')
jangkau = Prompt.ask('Masukkan Range')

with console.status("[bold green]Crawling data...") as status:
    for i in range(int(jangkau)):
        r = requests.post(f'https://daftar.bpsdmd.jatengprov.go.id/events-opd/index.php?halaman=cari_data&id_event={i}', 
            data={'nip_peserta': nip, 'id_event': str(i), 'simpan': ''},
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        )
        soup = BeautifulSoup(r.content, 'html5lib')
        try:
            text = str(soup.findAll('script', type='text/javascript')[1])
            if re.search("NIP Ditemukan!", text):
                judul = str(soup.findAll('a', style="color: white")[0]).replace('<a style="color: white">Unduh Data Peserta Pada ', '').replace('</a>', '')
                console.print(f'[bold green]NIP Ditemukan pada Bangkom:[/bold Green] {judul}')
                link = re.findall("e_sertifikat.*';", text)[0].replace("';", "")
                namafile = link.replace('e_sertifikat.php?no_sertifikat=','')+'.pdf'
                link = f'https://daftar.bpsdmd.jatengprov.go.id/events-opd/{link}'
                with requests.get(link, stream=True) as r:
                    with open(namafile, mode="wb") as file:
                        for chunk in r.iter_content(chunk_size=10 * 1024):
                            file.write(chunk)
            else:
                continue
        except:
            continue
    console.print('[bold green]Program Selesai')