# Google UI motion and rendering performance standards

Authoritative engineering rules, rendering pipeline constraints, and motion physics established by Chromium, Chrome Web Platform, Material Design 3, and Android UI frameworks.

Use these standards when auditing animation performance, debugging frame drops, calculating Core Web Vitals budgets, or designing physics-based gestures.

---

## 1. Chromium graphics and compositor architecture

### 1. Inside look at modern web browser part 3
* Tautan https://developer.chrome.com/blog/inside-browser-part3/
* Aturan teknis. Browser memisahkan parsing DOM, kalkulasi style, layout tree, paint records, dan compositing. Compositor thread membagi halaman menjadi layer, me-raster layer lewat raster threads dengan bantuan GPU, lalu menghasilkan draw quads untuk dikirim ke GPU process via IPC.
* Jebakan performa. Menjalankan JavaScript berat atau layout thrashing di main thread yang memblokir alur rendering, menyebabkan frame drop karena main thread tertahan menghitung ulang geometri elemen.

### 2. Inside look at modern web browser part 4
* Tautan https://developer.chrome.com/blog/inside-browser-part4/
* Aturan teknis. Input event seperti scroll, touch, dan wheel pertama kali diterima oleh browser process lalu langsung diarahkan ke compositor thread. Selama area tersebut bukan non-fast scrollable region, compositor menggulirkan viewport secara mulus tanpa perlu menunggu giliran eksekusi di main thread.
* Jebakan performa. Menambahkan touch atau wheel event listener ke window atau document tanpa opsi passive true, yang memaksa compositor thread berhenti dan menunggu main thread menjalankan JavaScript sebelum menggambar frame berikutnya.

### 3. Stick to Compositor-Only Properties and Manage Layer Count
* Tautan https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count
* Aturan teknis. Animasi performa tinggi hanya boleh mengubah transform dan opacity. Dua properti ini melewati tahapan layout dan paint, langsung diproses oleh compositor thread dengan akselerasi GPU. Elemen dapat dipromosikan menjadi layer mandiri memakai will-change transform.
* Jebakan performa. Terjadinya layer explosion akibat memasang will-change secara berlebihan pada puluhan elemen sekaligus. Setiap layer membutuhkan alokasi VRAM dan kalkulasi compositing tambahan yang menurunkan frame rate.

### 4. Simplify paint complexity and reduce paint areas
* Tautan https://web.dev/articles/simplify-paint-complexity-and-reduce-paint-areas
* Aturan teknis. Mengubah properti visual non-compositor memicu paint pass pada area elemen yang berubah. Batasi efek komputasi berat seperti filter blur atau drop-shadow dinamis yang dihitung berulang kali di area luas.
* Jebakan performa. Menyatukan elemen bergerak dengan elemen statis kompleks dalam satu layer grafis, sehingga seluruh layer harus digambar ulang terus-menerus setiap kali ada pergerakan kecil.

### 5. GPU Accelerated Compositing in Chrome
* Tautan https://www.chromium.org/developers/design-documents/gpu-accelerated-compositing-in-chrome/
* Aturan teknis. Chromium Compositor mengorganisasi hierarki RenderLayers dan GraphicsLayers. Setiap tekstur layer yang di-raster diunggah ke memori GPU dalam bentuk quad geometry, lalu ditransformasikan secara hardware oleh GPU shader saat tahap compositing akhir.
* Jebakan performa. Menganimasikan kombinasi properti yang merusak isolasi texture quad, misalnya mengubah border-radius bersamaan dengan box-shadow dinamis, yang memaksa CPU melakukan software rasterization ulang di setiap frame.

### 6. Chromium Graphics and Impl-Side Painting
* Tautan https://www.chromium.org/developers/design-documents/impl-side-painting/
* Aturan teknis. Arsitektur impl-side painting memisahkan perekaman perintah grafis di main thread dari proses rasterisasi aktual. Main thread merekam display list Skia, sementara rasterization dikerjakan secara asynchronous di impl thread pada grid ubin sesuai prioritas viewport.
* Jebakan performa. Mutasi DOM besar yang membatalkan seluruh display list secara serentak di tengah animasi, menyebabkan thread worker raster kehabisan waktu sebelum sinyal VSYNC tiba di layar.

---

## 2. Core Web Vitals and rendering performance

### 7. Rendering Performance
* Tautan https://web.dev/articles/rendering-performance
* Aturan teknis. Pipeline rendering browser mengikuti urutan JavaScript, Style, Layout, Paint, dan Composite. Animasi ideal wajib berada dalam batas durasi 16.6 milidetik per frame untuk layar 60Hz atau 8.3 milidetik untuk layar 120Hz, serta meniadakan fase Layout dan Paint saat animasi berlangsung.
* Jebakan performa. Forced Synchronous Layout dan Layout Thrashing, yaitu membaca properti geometri DOM seperti offsetWidth atau clientHeight tepat setelah menulis style baru di dalam loop animasi JavaScript.

### 8. Avoid non-composited animations
* Tautan https://developer.chrome.com/docs/lighthouse/performance/non-composited-animations/
* Aturan teknis. Audit Lighthouse mendeteksi animasi CSS atau Web Animations API yang gagal dipindahkan ke compositor thread. Animasi berjalan off-thread hanya jika elemen memiliki layer mandiri dan tidak menganimasikan properti geometri maupun paint.
* Jebakan performa. Menganimasikan properti top, left, width, height, margin, padding, atau filter statis, yang memaksa browser menjalankan recalculate style, relayout, dan repaint pada setiap interval frame.

### 9. Cumulative Layout Shift
* Tautan https://web.dev/articles/cls
* Aturan teknis. Skor CLS dihitung dari perkalian impact fraction dan distance fraction pada elemen tidak stabil yang bergeser tiba-tiba antar frame. Gerakan elemen tidak dihitung ke dalam penalti CLS jika dipicu langsung oleh interaksi pengguna dalam jendela toleransi 500 milidetik atau dieksekusi via CSS transform.
* Jebakan performa. Menggunakan animasi transisi CSS pada margin, top, atau height untuk elemen konten yang baru dimuat, karena pergeseran posisi fisik elemen lain di sekitarnya langsung diakumulasikan ke metrik CLS.

### 10. Optimize Cumulative Layout Shift
* Tautan https://web.dev/articles/optimize-cls
* Aturan teknis. Siapkan reservasi ruang layout dengan menetapkan dimensi width dan height eksplisit pada media atau memakai aspect-ratio pada wadah pembungkus. Seluruh animasi translasi wajib memanfaatkan transform translate agar dokumen flow asli tidak bergeser.
* Jebakan performa. Menganimasikan pembukaan accordion atau kartu dengan mengubah properti height tanpa pembungkus berdimensi tetap, sehingga mendorong blok teks di bawahnya dan memicu lonjakan skor CLS.

### 11. Interaction to Next Paint
* Tautan https://web.dev/articles/inp
* Aturan teknis. INP mengukur latensi interaksi secara menyeluruh, mencakup input delay saat event mengantre, processing duration saat callback dieksekusi, dan presentation delay hingga browser berhasil mempresentasikan frame visual baru ke layar display.
* Jebakan performa. Memulai komputasi animasi JavaScript yang sangat intensif langsung di dalam listener klik atau touch tanpa membagi frame pertama untuk umpan balik visual instan.

### 12. Optimize Interaction to Next Paint
* Tautan https://web.dev/articles/optimize-inp
* Aturan teknis. Pecah tugas JavaScript panjang dengan bantuan scheduler.yield() atau requestAnimationFrame. Sajikan umpan balik interaksi instan berbasis GPU compositor pada frame berikutnya, lalu tangguhkan proses mutasi DOM berat ke frame setelahnya.
* Jebakan performa. Menjalankan loop animasi synchronous atau mutasi DOM struktural berskala besar di dalam listener interaksi pengguna, yang menahan fase presentation delay melampaui batas toleransi 200 milidetik.

### 13. Animations Guide
* Tautan https://web.dev/articles/animations-guide
* Aturan teknis. Pilih mekanisme animasi paling efisien yang sesuai dengan kasus penggunaan. Prioritaskan deklarasi CSS transitions dan animations yang berjalan di compositor thread daripada manipulasi interval JavaScript yang mudah tersendat saat beban CPU meningkat.
* Jebakan performa. Memuat library animasi JavaScript berbobot berat hanya untuk menggerakkan interaksi mikro sederhana seperti transisi hover tombol atau indikator dropdown.

---

## 3. Modern web CSS motion standards

### 14. Prefers-reduced-motion media query
* Tautan https://web.dev/articles/prefers-reduced-motion
* Aturan teknis. Gunakan media query prefers-reduced-motion untuk mendeteksi kebutuhan aksesibilitas pengguna dengan gangguan vestibular. Ubah pergerakan spasial translasi yang agresif menjadi transisi opacity yang lembut tanpa menghilangkan konteks perubahan status UI.
* Jebakan performa. Menghilangkan transisi secara total tanpa pengganti visual sehingga status aplikasi berubah mendadak tanpa konteks, atau mengabaikan preferensi pengguna dan membiarkan efek gerakan intensif terus berjalan.

### 15. Four new CSS features for smooth entry and exit animations
* Tautan https://developer.chrome.com/blog/entry-exit-animations/
* Aturan teknis. Fitur CSS modern mendukung transisi elemen menuju atau keluar dari status display none dan top-layer. Gunakan @starting-style untuk menentukan kondisi style sebelum elemen dirender, gunakan transition-behavior allow-discrete untuk menganimasikan properti diskret, dan gunakan properti overlay untuk transisi penutupan dialog.
* Jebakan performa. Memaksa reflow lewat JavaScript dengan membaca element.offsetHeight hanya demi memicu animasi masuk CSS setelah menghapus properti display none.

### 16. Same-document view transitions for single-page applications
* Tautan https://developer.chrome.com/docs/web-platform/view-transitions/same-document/
* Aturan teknis. Fungsi document.startViewTransition mengambil snapshot visual kondisi DOM sebelum dan sesudah mutasi, lalu membungkusnya dalam pseudo-elements view-transition-old dan view-transition-new untuk dianimasikan secara hardware di level compositor.
* Jebakan performa. Menetapkan nama view-transition-name yang identik pada lebih dari satu elemen DOM aktif secara bersamaan, yang membuat browser langsung membatalkan seluruh proses transisi.

### 17. Cross-document view transitions for multi-page applications
* Tautan https://developer.chrome.com/docs/web-platform/view-transitions/cross-document/
* Aturan teknis. Transisi visual antar dokumen pada arsitektur multi-page application tanpa memerlukan framework JavaScript. Diaktifkan secara deklaratif menggunakan aturan CSS view-transition dengan nilai navigation auto pada kedua halaman yang berada dalam origin yang sama.
* Jebakan performa. Menerapkan transisi pada navigasi cross-origin atau memblokir proses rendering halaman tujuan dengan script berat, yang menyebabkan tampilan layar membeku sebelum transisi sempat dimulai.

### 18. Animate elements on scroll with Scroll-driven animations
* Tautan https://developer.chrome.com/docs/css-ui/scroll-driven-animations/
* Aturan teknis. Menautkan progres animasi secara langsung ke posisi scroll container lewat ScrollTimeline atau ke posisi elemen di dalam viewport lewat ViewTimeline. Seluruh siklus animasi berjalan langsung di compositor thread tanpa membebani main thread.
* Jebakan performa. Mengikat pembaruan style elemen ke listener event scroll manual di JavaScript yang membaca window.scrollY, yang menimbulkan stuttering parah karena kalkulasi style dipaksa berjalan di setiap tick scroll.

### 19. Animate to height auto using interpolate-size
* Tautan https://developer.chrome.com/docs/css-ui/animate-to-height-auto
* Aturan teknis. Mengaktifkan kemampuan browser menginterpolasi ukuran dari nilai numerik pasti ke intrinsic keyword seperti auto, min-content, atau fit-content menggunakan deklarasi interpolate-size allow-keywords pada elemen root atau target.
* Jebakan performa. Mengandalkan trik max-height dengan angka ribuan piksel dan kurva linear, yang menghasilkan jeda kosong saat animasi dimulai serta kecepatan gerak yang tidak proporsional dengan isi konten.

---

## 4. Material Design 3 motion standards

### 20. Material Design 3 Motion Overview
* Tautan https://m3.material.io/styles/motion/overview/how-it-works
* Aturan teknis. Motion pada Material Design 3 berfungsi membangun hierarki spasial, mengonfirmasi interaksi, dan memandu fokus pengguna. Gerakan antarmuka harus memiliki tujuan fungsional, terikat secara logis ke titik input pengguna, dan menjaga kontinuitas visual antar layer.
* Jebakan performa. Menambahkan animasi murni dekoratif tanpa tujuan navigasi fungsional, atau menetapkan durasi animasi fungsional melampaui batas 400 milidetik yang menghambat kecepatan kerja pengguna.

### 21. Material Design 3 Easing and Duration Tokens
* Tautan https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
* Aturan teknis. Material Design 3 menetapkan kurva gerak terstandarisasi seperti Emphasized Easing, yang memadukan percepatan awal dengan deselerasi panjang menuju posisi akhir. Skala durasi dibagi menjadi jenjang short (50 hingga 200 milidetik), medium (250 hingga 400 milidetik), dan long (450 hingga 700 milidetik).
* Jebakan performa. Memakai kurva ease-in konvensional pada elemen yang baru memasuki layar, yang memperlambat respons visual awal dan membuat antarmuka terasa lamban terhadap sentuhan.

### 22. Material Design 3 Transition Patterns
* Tautan https://m3.material.io/styles/motion/transitions/transition-patterns
* Aturan teknis. Mendefinisikan empat pola transisi utama. Container transform menghubungkan satu komponen ke komponen lain secara kontinu. Shared axis memvisualisasikan pergerakan spasial pada sumbu X, Y, atau Z. Fade through dipakai untuk perpindahan antar level navigasi utama yang tidak saling berbagi relasi spasial. Fade menangani elemen yang masuk atau keluar di dalam batas layar yang sama.
* Jebakan performa. Menggunakan transisi shared axis horizontal untuk komponen dialog modal yang muncul dari bawah layar, yang merusak model mental pengguna terhadap tata letak antarmuka.

---

## 5. Android physics and native gesture standards

### 23. Animate movement using spring physics
* Tautan https://developer.android.com/develop/ui/views/animations/spring-animation
* Aturan teknis. Menggunakan SpringAnimation dari pustaka Jetpack DynamicAnimation. Karakteristik gerak dikendalikan oleh dua parameter fisik, yaitu Damping Ratio yang mengatur osilasi pantulan, dan Stiffness yang menentukan tingkat kekakuan pegas dan kecepatan kembali ke titik kesetimbangan.
* Jebakan performa. Menghentikan animasi pegas secara mendadak dengan mereset koordinat posisi saat objek masih memiliki kecepatan tinggi, yang melenyapkan momentum fisik alami dan merusak ilusi gerak realistis.

### 24. Move views using a fling animation
* Tautan https://developer.android.com/develop/ui/views/animations/fling-animation
* Aturan teknis. FlingAnimation mensimulasikan gerak benda yang diluncurkan dengan kecepatan awal dari gestur pengguna lalu melambat bertahap akibat gaya gesek friksi. Memerlukan setStartVelocity dari gesture velocity tracker dan kalkulasi deselerasi yang proporsional.
* Jebakan performa. Menetapkan nilai kecepatan awal arbitrer yang tidak sinkron dengan kecepatan lepas jari pengguna, sehingga pergerakan terasa terputus saat jari meninggalkan layar.

### 25. Predictive back gesture implementation
* Tautan https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture
* Aturan teknis. Menangani gestur kembali interaktif melalui antarmuka OnBackAnimationCallback. Callback menyediakan metode handleOnBackStarted, handleOnBackProgressed yang menyuplai nilai progres antara 0.0 hingga 1.0, handleOnBackCancelled jika gestur dibatalkan, dan handleOnBackPressed jika gestur diselesaikan.
* Jebakan performa. Mengeksekusi perpindahan layar secara permanen di awal event geseran tanpa menunggu konfirmasi akhir, sehingga pengguna kehilangan kemampuan membatalkan navigasi saat mengembalikan posisi jari.

### 26. Predictive back design patterns
* Tautan https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back
* Aturan teknis. Komponen lembar bawah, lembar samping, bilah pencarian, dan kontainer kartu harus mengecil secara halus dan melepaskan diri dari tepi layar selaras dengan progres sapuan jari pengguna untuk memperlihatkan pratinjau halaman sebelumnya.
* Jebakan performa. Membiarkan tampilan antarmuka tetap statis kaku selama gestur berlangsung lalu mendadak berganti layar saat jari dilepas, yang membingungkan orientasi spasial pengguna.

### 27. Customize Compose animations
* Tautan https://developer.android.com/develop/ui/compose/animation/customize
* Aturan teknis. Jetpack Compose menyediakan spesifikasi animasi berbasis fisika dan waktu melalui AnimationSpec, mencakup spring, tween, keyframes, dan snap. Spesifikasi spring menjadi pilihan bawaan karena kemampuannya mempertahankan kontinuitas kecepatan saat target nilai diinterupsi di tengah jalan.
* Jebakan performa. Menggunakan tween berdurasi statis untuk animasi interaktif yang dapat diinterupsi oleh gestur pengguna, yang menyebabkan lompatan visual patah karena kecepatan awal diatur ulang ke angka nol secara paksa.

---

## 6. Engineering synthesis and audit rules

Terapkan standar Google di atas dalam setiap fase perancangan animasi:

1. Compositor thread protection. Setiap elemen yang bergerak wajib memanfaatkan `transform` dan `opacity`. Jangan pernah menganimasikan `width`, `height`, `top`, `left`, atau `margin` pada komponen dinamis.
2. Core Web Vitals safety.
* Untuk menjaga skor Interaction to Next Paint (INP) di bawah 200 milidetik, berikan feedback visual instan pada frame pertama lalu pecah tugas JavaScript berat memakai `scheduler.yield()` atau `requestAnimationFrame`.
* Untuk menjaga Cumulative Layout Shift (CLS) pada skor 0, sediakan reservasi dimensi eksplisit dan batasi seluruh translasi elemen ke GPU transform.
3. SSR and React 19 hydration safety. Jangan pernah menukar tag elemen di JSX berdasarkan status `useReducedMotion()`. Selalu pertahankan struktur DOM identik antara server dan client, lalu delegasikan fallback aksesibilitas ke selector CSS `[data-motion-enter]` dengan penanda `!important`.
