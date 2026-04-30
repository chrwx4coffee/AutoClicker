#include <iostream>
#include <thread>
#include <chrono>
#include <X11/Xlib.h>
#include <X11/extensions/XTest.h>

using namespace std;

void getMousePos(Display* dpy, Window root, int& x, int& y) {
    Window root_return, child_return;
    int root_x, root_y, win_x, win_y;
    unsigned int mask_return;
    XQueryPointer(dpy, root, &root_return, &child_return, &root_x, &root_y, &win_x, &win_y, &mask_return);
    x = root_x;
    y = root_y;
}

void click(Display* dpy, int x, int y) {
    XTestFakeMotionEvent(dpy, -1, x, y, CurrentTime);
    XTestFakeButtonEvent(dpy, 1, True, CurrentTime);
    XTestFakeButtonEvent(dpy, 1, False, CurrentTime);
    XFlush(dpy);
}

int main() {
    cout << "=================================\n";
    cout << "      C++ CLI AUTO CLICKER       \n";
    cout << "=================================\n\n";

    int count;
    double delay;

    cout << "Tiklama Sayisi giriniz: ";
    cin >> count;

    if (count <= 0) {
        cout << "Hata: Sayi 0'dan buyuk olmalidir.\n";
        return 1;
    }

    cout << "Gecikme (saniye) giriniz (orn: 0.5): ";
    cin >> delay;

    if (delay < 0) {
        cout << "Hata: Gecikme 0'dan kucuk olamaz.\n";
        return 1;
    }

    cout << "\n>>> KONUM SECIMI <<<\n";
    cout << "Farenizi 3 saniye icinde hedefinizin uzerine goturun ve bekleyin...\n";
    
    for (int i = 3; i > 0; i--) {
        cout << i << "..." << flush;
        this_thread::sleep_for(chrono::seconds(1));
    }
    cout << "\n";

    Display* dpy = XOpenDisplay(NULL);
    if (!dpy) {
        cerr << "X11 Ekranina baglanilamadi. Wayland kullaniyorsaniz bazi kisitlamalar olabilir.\n";
        return 1;
    }

    Window root = DefaultRootWindow(dpy);
    int targetX, targetY;
    getMousePos(dpy, root, targetX, targetY);

    cout << "[BASARILI] Konum kaydedildi: X=" << targetX << " Y=" << targetY << "\n";
    cout << "\n>>> ISLEM BASLIYOR <<<\n";
    
    this_thread::sleep_for(chrono::milliseconds(500));

    for (int i = 0; i < count; i++) {
        click(dpy, targetX, targetY);
        this_thread::sleep_for(chrono::milliseconds(static_cast<int>(delay * 1000)));
        if ((i+1) % 10 == 0 || i+1 == count) {
            cout << "Ilerleme: " << (i+1) << "/" << count << " tiklama tamamlandi.\n";
        }
    }

    cout << "\n[TAMAMLANDI] Tum tiklamalar basariyla gerceklestirildi!\n";

    XCloseDisplay(dpy);
    return 0;
}
