import discord
from discord import app_commands
import random
import string
import os
import threading
from flask import Flask

# ====================== KONFİGÜRASYON ======================
TOKEN = os.getenv('DISCORD_TOKEN') # Render üzerinde Environment Variable olarak eklenmeli

# ====================== FLASK WEB SUNUCUSU (KEEP-ALIVE) ======================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Aktif! - Made by Zadrex"

def run_web():
    # Render'ın beklediği port (varsayılan 10000 veya PORT env var)
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
        # Slash komutlarını senkronize et
        await self.tree.sync()
        print(f"Komutlar senkronize edildi.")

    async def on_ready(self):
        print(f'{self.user} olarak giriş yapıldı!')
        await self.change_presence(activity=discord.Game(name="/nitro | Made by Zadrex"))

client = NitroBot()

# ====================== SLASH KOMUTU ======================
@client.tree.command(name="nitro", description="Belirtilen adette Nitro kodu üretir ve DM'den gönderir.")
@app_commands.describe(adet="Kaç adet nitro kodu üretilsin?")
async def nitro(interaction: discord.Interaction, adet: int):
    if adet <= 0:
        await interaction.response.send_message("Lütfen 0'dan büyük bir sayı girin!", ephemeral=True)
        return
    
    if adet > 100:
        await interaction.response.send_message("Tek seferde en fazla 100 adet üretebilirsiniz.", ephemeral=True)
        return

    # İlk yanıtı ver (botun çalıştığını göstermek için)
    await interaction.response.send_message(f"{adet} adet nitro kodu DM kutunuza gönderiliyor...", ephemeral=True)

    try:
        codes = []
        for _ in range(adet):
            code = generate_nitro_code()
            codes.append(f"https://discord.gift/{code}")
        
        # Mesajı parçalara böl (Discord 2000 karakter sınırı)
        message_content = "\n".join(codes)
        
        # DM gönder
        if len(message_content) > 1900:
            # Eğer mesaj çok uzunsa parçalayarak gönder
            current_msg = ""
            for code in codes:
                if len(current_msg) + len(code) + 1 > 1900:
                    await interaction.user.send(f"**Üretilen Nitro Kodları:**\n{current_msg}")
                    current_msg = code + "\n"
                else:
                    current_msg += code + "\n"
            if current_msg:
                await interaction.user.send(current_msg)
        else:
            await interaction.user.send(f"**Üretilen Nitro Kodları ({adet} adet):**\n{message_content}")
            
    except discord.Forbidden:
        await interaction.followup.send("DM kutunuz kapalı olduğu için kodları gönderemedim!", ephemeral=True)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        await interaction.followup.send(f"Bir hata oluştu: {e}", ephemeral=True)

# ====================== ÇALIŞTIRMA ======================
if __name__ == "__main__":
    # Web sunucusunu ayrı bir thread'de başlat
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

    # Botu başlat
    if TOKEN:
        client.run(TOKEN)
    else:
        print("HATA: DISCORD_TOKEN bulunamadı! Lütfen Environment Variable olarak ekleyin.")
