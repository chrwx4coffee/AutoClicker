/**
 * WEB AUTO CLICKER
 * Kullanım:
 * Bu kodu kopyalayıp herhangi bir web sayfasında İncele (F12) -> Console sekmesine 
 * yapıştırıp Enter'a basarak çalıştırabilirsiniz.
 * Sağ alt köşede şık ve modern bir arayüz açılacaktır.
 */
(function() {
    // Eğer daha önce çalıştırıldıysa tekrar ekleme
    if (document.getElementById('my-auto-clicker-ui')) return;

    // Arayüz oluştur
    const ui = document.createElement('div');
    ui.id = 'my-auto-clicker-ui';
    ui.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 320px;
        background: rgba(15, 23, 36, 0.95);
        color: white;
        border-radius: 16px;
        padding: 24px;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        z-index: 999999;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    `;

    ui.innerHTML = `
        <h3 style="margin:0 0 15px;text-align:left;font-size:20px;font-weight:600;display:flex;justify-content:space-between;align-items:center;">
            Web Auto Clicker
            <button id="ac-close" style="background:transparent;border:none;color:#aaa;cursor:pointer;font-size:16px;">&times;</button>
        </h3>
        <div style="background:#1e293b;padding:12px;border-radius:8px;margin-bottom:15px;border:1px solid #334155;">
            <div id="ac-status" style="color:#94a3b8;font-size:13px;word-break:break-all;">Hedef: Bekleniyor...</div>
        </div>
        <button id="ac-select" style="width:100%;padding:12px;margin-bottom:20px;background:#3b82f6;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:bold;transition:0.2s;">🎯 Tıklanacak Öğeyi Seç</button>
        
        <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
            <label style="font-size:14px;align-self:center;color:#cbd5e1;">Tıklama Sayısı:</label>
            <input id="ac-count" type="number" value="10" style="width:80px;padding:8px;border-radius:6px;border:1px solid #3b82f6;background:#0f172a;color:white;text-align:center;outline:none;">
        </div>
        
        <div style="display:flex;justify-content:space-between;margin-bottom:20px;">
            <label style="font-size:14px;align-self:center;color:#cbd5e1;">Gecikme (sn):</label>
            <input id="ac-delay" type="number" value="1.0" step="0.1" style="width:80px;padding:8px;border-radius:6px;border:1px solid #3b82f6;background:#0f172a;color:white;text-align:center;outline:none;">
        </div>
        
        <button id="ac-start" style="width:100%;padding:14px;margin-bottom:5px;background:#10b981;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:bold;font-size:16px;transition:0.2s;box-shadow:0 4px 12px rgba(16, 185, 129, 0.3);">🚀 Başlat</button>
    `;

    document.body.appendChild(ui);

    let targetElement = null;
    let isSelecting = false;

    const statusEl = document.getElementById('ac-status');
    const selectBtn = document.getElementById('ac-select');
    const countEl = document.getElementById('ac-count');
    const delayEl = document.getElementById('ac-delay');
    const startBtn = document.getElementById('ac-start');
    const closeBtn = document.getElementById('ac-close');

    // Hedef Seç Butonu
    selectBtn.addEventListener('click', () => {
        isSelecting = true;
        statusEl.innerText = 'Lütfen sayfada bir öğeye tıklayın...';
        statusEl.style.color = '#60a5fa';
        selectBtn.style.opacity = '0.5';
        document.body.style.cursor = 'crosshair';
    });

    closeBtn.addEventListener('click', () => {
        ui.remove();
        document.body.style.cursor = 'default';
        document.removeEventListener('click', clickHandler, {capture: true});
    });

    // Sayfaya tıklandığında hedefi seçme
    const clickHandler = (e) => {
        if (!isSelecting) return;
        
        // Arayüzün kendisine tıklanırsa dikkate alma
        if (ui.contains(e.target)) return;

        e.preventDefault();
        e.stopPropagation();

        targetElement = e.target;
        isSelecting = false;
        document.body.style.cursor = 'default';
        
        // Hedefin adını belirlemeye çalış
        let name = targetElement.tagName.toLowerCase();
        if(targetElement.id) name += '#' + targetElement.id;
        else if(targetElement.className && typeof targetElement.className === 'string') name += '.' + targetElement.className.split(' ')[0];

        statusEl.innerText = 'Seçildi: ' + name;
        statusEl.style.color = '#34d399';
        
        selectBtn.style.opacity = '1';
        selectBtn.innerText = '🎯 Hedefi Değiştir';
    };

    // Tüm tıklamaları en dıştan yakalamak için capture: true kullanıyoruz
    document.addEventListener('click', clickHandler, {capture: true});

    // Başlat Butonu
    startBtn.addEventListener('click', async () => {
        if (!targetElement) {
            alert('Lütfen önce tıklanacak öğeyi seçin!');
            return;
        }

        const count = parseInt(countEl.value);
        const delayMs = parseFloat(delayEl.value) * 1000;

        startBtn.disabled = true;
        startBtn.innerText = 'Tıklanıyor...';
        startBtn.style.background = '#f59e0b';
        startBtn.style.boxShadow = '0 4px 12px rgba(245, 158, 11, 0.3)';

        for (let i = 0; i < count; i++) {
            // Öğe sayfadan silinmiş mi kontrol et
            if (!document.body.contains(targetElement)) {
                statusEl.innerText = 'Hedef öğe sayfadan kayboldu!';
                statusEl.style.color = '#ef4444';
                break;
            }
            targetElement.click();
            await new Promise(r => setTimeout(r, delayMs));
        }

        startBtn.disabled = false;
        startBtn.innerText = '🚀 Başlat';
        startBtn.style.background = '#10b981';
        startBtn.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.3)';
        
        if (document.body.contains(targetElement)) {
            statusEl.innerText = 'Görev tamamlandı!';
            statusEl.style.color = '#34d399';
        }
    });

    console.log("%c Web Auto Clicker Yüklendi! ", "background: #10b981; color: white; border-radius: 4px; padding: 4px; font-weight: bold;");
})();
