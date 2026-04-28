package main

import (
	"fmt"
	"strconv"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"github.com/go-vgo/robotgo"
)

func main() {
	a := app.New()
	w := a.NewWindow("Go Auto Clicker")
	w.Resize(fyne.NewSize(350, 350))

	var targetX, targetY int
	var isLocationSet bool

	statusLabel := widget.NewLabel("Konum: Seçilmedi\nDurum: Bekleniyor")
	
	countEntry := widget.NewEntry()
	countEntry.SetText("10")
	
	delayEntry := widget.NewEntry()
	delayEntry.SetText("1.0")

	var selectBtn *widget.Button
	var startBtn *widget.Button

	selectBtn = widget.NewButton("Konum Seç (3 Saniye)", func() {
		selectBtn.Disable()
		startBtn.Disable()
		
		go func() {
			for i := 3; i > 0; i-- {
				statusLabel.SetText(fmt.Sprintf("Konum: Seçiliyor...\nDurum: Farenizi hedefe götürün... %d", i))
				time.Sleep(1 * time.Second)
			}
			
			x, y := robotgo.Location()
			targetX = x
			targetY = y
			isLocationSet = true
			
			statusLabel.SetText(fmt.Sprintf("Konum: X=%d, Y=%d\nDurum: Konum kaydedildi.", x, y))
			selectBtn.Enable()
			startBtn.Enable()
		}()
	})

	startBtn = widget.NewButton("Başlat", func() {
		if !isLocationSet {
			statusLabel.SetText("Konum: X=?, Y=?\nHata: Önce konum seçin!")
			return
		}

		count, err := strconv.Atoi(countEntry.Text)
		if err != nil || count <= 0 {
			statusLabel.SetText(fmt.Sprintf("Konum: X=%d, Y=%d\nHata: Geçerli bir sayı girin.", targetX, targetY))
			return
		}

		delay, err := strconv.ParseFloat(delayEntry.Text, 64)
		if err != nil || delay < 0 {
			statusLabel.SetText(fmt.Sprintf("Konum: X=%d, Y=%d\nHata: Geçerli bir gecikme girin.", targetX, targetY))
			return
		}

		selectBtn.Disable()
		startBtn.Disable()
		statusLabel.SetText(fmt.Sprintf("Konum: X=%d, Y=%d\nDurum: Tıklanıyor...", targetX, targetY))

		go func() {
			time.Sleep(500 * time.Millisecond)

			for i := 0; i < count; i++ {
				robotgo.Move(targetX, targetY)
				robotgo.Click("left")
				time.Sleep(time.Duration(delay * float64(time.Second)))
			}

			statusLabel.SetText(fmt.Sprintf("Konum: X=%d, Y=%d\nDurum: Tıklama tamamlandı.", targetX, targetY))
			selectBtn.Enable()
			startBtn.Enable()
		}()
	})

	form := container.NewVBox(
		widget.NewLabel("Tıklama Sayısı:"),
		countEntry,
		widget.NewLabel("Gecikme (sn):"),
		delayEntry,
	)

	content := container.NewVBox(
		widget.NewLabelWithStyle("Go Auto Clicker", fyne.TextAlignCenter, fyne.TextStyle{Bold: true}),
		statusLabel,
		selectBtn,
		form,
		startBtn,
	)

	w.SetContent(content)
	w.ShowAndRun()
}
