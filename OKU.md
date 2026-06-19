# Discord Nitro Generator Bot - Render Uyumlu

Bu bot, `/nitro` slash komutu ile belirtilen adette Nitro kodu üretir ve kullanıcıya DM üzerinden gönderir. Render üzerinde 7/24 aktif kalması için web sunucusu entegre edilmiştir.

## 📁 Dosyalar
- `bot.py`: Ana bot kodu ve Flask web sunucusu.
- `requirements.txt`: Gerekli kütüphaneler (discord.py, flask).
- `Procfile`: Render için çalıştırma komutu.
- `OKU.md`: Kurulum talimatları.

## 🚀 Kurulum Adımları

### 1. Discord Bot Hazırlığı
1. [Discord Developer Portal](https://discord.com/developers/applications) adresine gidin.
2. Yeni bir uygulama oluşturun ve `Bot` kısmına gelin.
3. **Privileged Gateway Intents** başlığı altındaki şu seçenekleri aktif edin:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
4. Botun tokenını kopyalayın.

### 2. Render Üzerinde Yayına Alma
1. Bu dosyaları bir GitHub deposuna (repository) yükleyin.
2. [Render.com](https://render.com) adresine giriş yapın.
3. **New +** butonuna basın ve **Web Service** seçeneğini seçin.
4. GitHub deponuzu bağlayın.
5. Ayarları şu şekilde yapın:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
6. **Advanced** butonuna tıklayın ve **Add Environment Variable** diyerek şunları ekleyin:
   - Key: `DISCORD_TOKEN`
   - Value: `SİZİN_BOT_TOKENINIZ`
7. **Create Web Service** butonuna basın.

### 3. 7/24 Aktif Tutma (Ping Atma)
Render ücretsiz planında servisler 15 dakika işlem yapılmazsa uyku moduna geçer. Bunu engellemek için:
1. Render'ın size verdiği URL'yi kopyalayın (örn: `https://nitro-bot.onrender.com`).
2. [UptimeRobot](https://uptimerobot.com) gibi bir servise gidin.
3. Yeni bir "HTTP(s)" monitörü oluşturun ve Render URL'nizi yapıştırın.
4. 5 dakikada bir kontrol edilecek şekilde ayarlayın.

## 🛠️ Kullanım
- Bot sunucunuza eklendikten sonra `/nitro adet:10` yazarak kodları DM üzerinden alabilirsiniz.

---
**Made by Zadrex**
