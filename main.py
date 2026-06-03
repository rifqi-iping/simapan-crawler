import os
import re
import time
import requests
import html5lib
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt

console = Console()
directory = "./results"

console.print('[bold white]SIMAPAN BPSDMD Jateng Sertifikat Crawling by [bold red]rifqi.iping')
console.print('1. Single Mode')
console.print('2. Batch Mode')
mode = Prompt.ask('Pilih Mode 1/2')
if mode == '1':
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
                    console.print(f'[bold green]NIP Ditemukan pada Bangkom:[/bold Green][white] {judul}')
                    link = re.findall("e_sertifikat.*';", text)[0].replace("';", "")
                    namafile = link.replace('e_sertifikat.php?no_sertifikat=','')+'.pdf'
                    link = f'https://daftar.bpsdmd.jatengprov.go.id/events-opd/{link}'
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    file_path = os.path.join(directory, namafile)
                    with requests.get(link, stream=True) as r:
                        with open(file_path, mode="wb") as file:
                            for chunk in r.iter_content(chunk_size=10 * 1024):
                                file.write(chunk)
                else:
                    continue
            except:
                continue
elif mode == '2':
    namaFile = Prompt.ask('Masukkan Nama File')
    eventId = Prompt.ask('Masukkan Id Kegiatan')
    with open(namaFile, 'r', encoding='utf-8') as file:
        for line in file:
            nip = line.strip()
            r = requests.post(f'https://daftar.bpsdmd.jatengprov.go.id/events-opd/index.php?halaman=cari_data&id_event={eventId}', 
                data={'nip_peserta': nip, 'id_event': str(eventId), 'simpan': ''},
                headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
            )
            soup = BeautifulSoup(r.content, 'html5lib')
            try:
                text = str(soup.findAll('script', type='text/javascript')[1])
                if re.search("NIP Ditemukan!", text):
                    judul = str(soup.findAll('a', style="color: white")[0]).replace('<a style="color: white">Unduh Data Peserta Pada ', '').replace('</a>', '')
                    console.print(f'[bold green]NIP {nip} Ditemukan pada Bangkom:[/bold Green][white] {judul}')
                    link = re.findall("e_sertifikat.*';", text)[0].replace("';", "")
                    namafile = link.replace('e_sertifikat.php?no_sertifikat=','')+'.pdf'
                    link = f'https://daftar.bpsdmd.jatengprov.go.id/events-opd/{link}'
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    file_path = os.path.join(directory, namafile)
                    with requests.get(link, stream=True) as r:
                        with open(file_path, mode="wb") as file:
                            for chunk in r.iter_content(chunk_size=10 * 1024):
                                file.write(chunk)
                else:
                    continue
            except:
                continue
else:
    console.print('[bold red]ERROR Mode yang dipilih tidak tersedia!')
console.print('[bold green]Program Selesai')