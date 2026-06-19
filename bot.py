import discord
from discord import app_commands
import random
import string
import os
import threading
import io
from flask import Flask

# ====================== KONFİGÜRASYON ======================
TOKEN = os.getenv('DISCORD_TOKEN') 

# ====================== FLASK WEB SUNUCUSU (KEEP-ALIVE) ======================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Aktif! - Made by Zadrex"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ====================== NİTRO GENERATOR FONKSİYONU ======================
def generate_nitro_code(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

# ====================== DISCORD BOT SINIFI ======================
class NitroBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Komutlar senkronize edildi.")

    async def on_ready(self):
        print(f'{self.user} olarak giriş yapıldı!')
        await self.change_presence(activity=discord.Game(name="/nitro | Made by Zadrex"))

client = NitroBot()

# ====================== SLASH KOMUTU ======================
@client.tree.command(name="nitro", description="1 Milyona kadar Nitro kodu üretir ve TXT dosyası olarak gönderir.")
@app_commands.describe(adet="Kaç adet nitro kodu üretilsin? (Max: 1.000.000)")
async def nitro(interaction: discord.Interaction, adet: int):
    if adet <= 0:
        await interaction.response.send_message("Lütfen 0'dan büyük bir sayı girin!", ephemeral=True)
        return
    
    # 1 Milyon sınırı
    if adet > 1000000:
        await interaction.response.send_message("Tek seferde en fazla 1.000.000 (1 Milyon) adet üretebilirsiniz.", ephemeral=True)
        return

    # İlk yanıtı ver
    await interaction.response.send_message(f"🚀 **{adet}** adet nitro kodu üretiliyor... Bu işlem biraz zaman alabilir, lütfen bekleyin.", ephemeral=True)

    try:
        # Kodları üret ve bellekte biriktir
        output = io.StringIO()
        for _ in range(adet):
            code = generate_nitro_code()
            output.write(f"https://discord.gift/{code}\n")
        
        # Dosyayı hazırla
        output.seek(0)
        file_data = output.getvalue().encode('utf-8')
        discord_file = discord.File(fp=io.BytesIO(file_data), filename=f"nitro_codes_{adet}.txt")
        
        # DM gönder
        await interaction.user.send(content=f"✅ **{adet}** adet nitro kodu başarıyla üretildi ve dosyaya yazıldı!", file=discord_file)
        
        # Temizlik
        output.close()
            
    except discord.Forbidden:
        await interaction.followup.send("DM kutunuz kapalı olduğu için dosyayı gönderemedim! Lütfen DM'lerinizi açın.", ephemeral=True)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        await interaction.followup.send(f"Bir hata oluştu: {e}", ephemeral=True)

# ====================== ÇALIŞTIRMA ======================
if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

    if TOKEN:
        client.run(TOKEN)
    else:
        print("HATA: DISCORD_TOKEN bulunamadı!")
