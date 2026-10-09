# Pola dan kosakata bahasa Indonesia untuk unslop

Dokumen ini memuat aturan mendeteksi, memotong, dan menulis ulang teks bahasa Indonesia buatan AI agar kembali wajar, lugas, dan berbobot.

## Sumber rujukan dan analisis

Dokumen ini menyintesis kaidah dari 14 rujukan terverifikasi lintas regulator, studi linguistik akademik, agensi kurasi konten, dan praktisi bahasa:

1. Peraturan Dewan Pers Nomor 1/Peraturan-DP/I/2025 tentang Pedoman Penggunaan Kecerdasan Buatan dalam Karya Jurnalistik (dewanpers.or.id).
2. Sirlia Sahid, dkk. (2026). Ragam Bahasa Indonesia dalam Prompt AI, Studi Komparatif Gaya Respons ChatGPT. Jurnal Morfologi, 4(3), 21-36.
3. Ariesta Bagus Pramuwibowo dan Titik Dwi Ramthi Hakim (2026). Evaluasi Komparatif Manusia, ChatGPT, dan Gemini dalam Menganalisis Pola Kalimat pada Teks Akademik. Prosiding SEMDIKJAR UNP Kediri, Vol. 9.
4. Narabahasa (Ivan Lanin). Analisis interferensi sintaksis asing pada pemakaian frasa di mana dan yang mana.
5. Narabahasa (Yudhistira). Benarkah Penyunting Tergantikan oleh AI? dan Robot yang Menulis.
6. Tempo.co Tekno. Alasan Berkomunikasi Menggunakan AI Disebut Tidak Manusiawi.
7. Jawa Pos Lifestyle. 7 Frasa Ciri Kenali Tulisan Khas ChatGPT yang Jadi Tanda Tulisan Buatan AI.
8. RadVoice Indonesia (Niken Anggun Nurani). 8 Cara Mendeteksi Tulisan yang Dibuat AI.
9. ARSA Technology Research (2025). Ketika AI Menulis, Menguak Pola Kalimat Bukan Hanya Ini, Tapi Juga Itu dalam Komunikasi Korporat.
10. cmlabs Blog (Alivia Ariatna). Apakah ChatGPT Sudah Melek Kaidah Penulisan? Sebuah Studi Deskriptif.
11. ToffeeDev SEO Blog. Konten AI Anda Bisa Kena Penalti Google di 2025? Ini Cara Menghindarinya!
12. Sastra Lingua Indonesia. Cara Efektif Mengatasi Naskah yang Terdeteksi AI.
13. Carolina Ratri. Cara Mengedit Tulisan Hasil AI agar Tidak Terlihat Kaku dan Generik.
14. Dewi Mahendradita (Medium). 4 Tanda Kaku, Cara Deteksi Tulisan dari AI Generatif.

## Mengapa teks AI bahasa Indonesia terasa kaku

1. Calque dan translationese. Model bahasa besar umumnya berlatih dengan korpus bahasa Inggris. Model menerjemahkan sintaksis dan ungkapan asing secara harfiah ke bahasa Indonesia. Pola ini memicu pemakaian kata hubung rancu seperti "di mana", frasa kaku seperti "memainkan peran penting", dan metafora asing seperti "dalam lanskap".
2. Perplexity rendah. AI memilih kata dengan probabilitas statistik tertinggi. Pilihan mekanis ini menghasilkan kosakata klise yang seragam tanpa variasi diksi alami.
3. Burstiness rendah. AI menyusun kalimat dengan panjang dan struktur klausa yang monoton dari awal hingga akhir. Tulisan kehilangan dinamika jeda dan ritme baca.
4. Pasifisme berlebihan. AI kerap menyamarkan subjek pelaku memakai verba pasif berprefiks di- seperti "dapat dipahami bahwa" atau "hal ini dilakukan guna" demi menjaga netralitas semu.
5. Retorika simetris dan triadik. AI sering menyusun pasangan klausa biner seperti "tidak hanya X, tetapi juga Y" serta deretan tiga kata sifat secara mekanis.
6. Basa-basi formulaik. AI membuka tulisan memakai premis usang seperti "di era digital yang serba cepat ini", lalu menutupnya dengan rangkuman hambar tanpa langkah tindak lanjut yang nyata.

## Katalog kosakata dan pola terlarang

### 1. Frasa pembuka dan penutup basa-basi

Buang klausa pengantar kosong. Tuliskan inti informasi langsung pada kalimat pertama.

| Frasa terlarang | Masalah | Pengganti konkret |
|---|---|---|
| Di era digital yang serba cepat ini / Di zaman modern saat ini | Klise pembuka generik tanpa data | Hapus total. Buka langsung dengan subjek dan fakta waktu riil |
| Di tengah pesatnya perkembangan teknologi | Premis pengantar tanpa substansi | Hapus total. Masuk langsung ke kondisi sistem |
| Tidak dapat dipungkiri bahwa / Tak dapat disangkal bahwa | Retorika kosong pengulur kalimat | Hapus total. Tulis langsung pernyataan faktanya |
| Bukan rahasia lagi bahwa | Asumsi klise tanpa pembuktian | Tulis data atau peristiwa yang membuktikannya |
| Perlu diingat bahwa / Penting untuk dicatat bahwa | Khotbah direktif yang menggurui | Hapus. Tulis aturannya secara deklaratif langsung |
| Perlu digarisbawahi bahwa / Patut dicatat bahwa | Penekanan artifisial | Hapus. Tulis fakta langsung |
| Mari kita telusuri lebih dalam / Mari kita bahas | Basa-basi ajakan khas chatbot | Hapus. Masuk langsung ke subtopik bahasan |
| Tentu saja! / Tentu, ini dia / Dengan senang hati | Pembuka percakapan bot yang menjilat | Hapus total. Buka langsung dengan data, kode, atau status |
| Pertanyaan yang bagus! / Pertanyaan yang sangat menarik! | Basa-basi penjilat bot sebelum menjawab | Hapus total. Jawab pertanyaan teknis secara langsung |
| Semoga informasi ini bermanfaat / Semoga membantu | Penutup sapaan khas asisten bot | Hapus. Ganti dengan instruksi aksi teknis berikutnya |
| Secara keseluruhan / Sebagai kesimpulan dapat disimpulkan bahwa | Rangkuman mekanis yang mengulang premis | Hapus. Tutup dengan langkah konkret atau status final |
| Masa depan tampak cerah / Menuju masa depan yang berkelanjutan | Retorika seremonial tanpa komitmen terukur | Sebut target numerik atau batas waktu riil proyek |

### 2. Konjungsi transisi robotik dan interferensi asing (calque)

Hindari konjungsi majemuk beruntun di setiap awal kalimat. Putus menjadi kalimat mandiri.

| Frasa terlarang | Masalah | Pengganti konkret |
|---|---|---|
| di mana / yang mana (sebagai penghubung klausa) | Calque kasar dari where dan which | Hapus. Sambung langsung dengan kata benda atau buat kalimat baru |
| memainkan peran penting dalam / memainkan peran kunci | Calque harfiah dari plays an important role in | menentukan, menjadi kunci, mempercepat, atau sebut dampak aksinya |
| dalam lanskap yang terus berkembang / menavigasi lanskap | Calque harfiah dari in the evolving landscape | pada industri, di pasar, dalam sistem, di codebase |
| sebuah bukti nyata dari | Calque harfiah dari a testament to | membuktikan, menunjukkan, memvalidasi |
| menyelami lebih dalam | Calque harfiah dari delve into | memeriksa, menganalisis, membedah, menguji |
| permadani yang kaya / rumit | Calque harfiah dari rich tapestry | variasi, kombinasi, susunan, sistem |
| merangkul perubahan / merangkul teknologi | Calque harfiah dari embrace change / technology | mengadopsi, menyesuaikan sistem, memperbarui |
| membuka potensi penuh | Calque harfiah dari unlock full potential | meningkatkan kapasitas, mempercepat alur kerja |
| mengambil tempat | Calque harfiah dari take place | berlangsung, diadakan, bertempat |
| membuat keputusan | Calque harfiah dari make a decision | memutuskan, menentukan |
| alat yang ampuh / senjata ampuh | Calque harfiah dari powerful tool | Sebut nama perkakas, algoritma, atau fitur teknis spesifik |
| berada di garis depan | Calque harfiah dari at the forefront | memimpin, merintis, berada di barisan awal |
| membuka jalan bagi | Calque harfiah dari pave the way for | memungkinkan, memfasilitasi, memicu |
| pedang bermata dua | Calque klise dari double-edged sword | Sebutkan dua risiko atau konsekuensi teknis secara eksplisit |
| menavigasi kompleksitas | Calque harfiah dari navigate complexity | menangani kerumitan, menyelesaikan masalah, mengelola alur |
| hadir untuk | Calque harfiah dari here to | berfungsi untuk, dirancang untuk, dibangun untuk |
| tidak kalah pentingnya / terakhir namun tidak kalah penting | Calque harfiah dari last but not least | Hapus frasa pengantar, sebut poin langsung |
| merupakan rumah bagi | Calque harfiah dari home to | menampung, memuat, mencakup |
| di bawah kap mesin | Calque harfiah dari under the hood | cara kerja internal, layer bawah, arsitektur dasar |
| ujung tombak | Calque harfiah dari spearhead | penggerak utama, fungsi inti |
| selain itu / di samping itu (diulang berurutan) | Lem transisi otomatis AI | Hubungkan dengan logika sebab akibat atau mulai kalimat baru |
| oleh karena itu / dengan demikian (beruntun) | Simpulan logika mekanis | Gunakan maka, akibatnya, atau jabarkan hasilnya |

### 3. Kata sifat dan pengisi abstrak (puffery)

Ganti kata sifat hiperbolis dengan metrik, waktu, atau mekanisme sistem.

| Frasa terlarang | Masalah | Pengganti konkret |
|---|---|---|
| krusial / vital / esensial | Sifat abstrak tanpa ukuran bahaya | wajib, dibutuhkan, atau sebutkan dampak bila gagal |
| berdampak signifikan / memberikan dampak positif | Pernyataan samar | Sebut angka kenaikan metrik atau persentase terukur |
| holistik / komprehensif / menyeluruh | Kata pengisi ruang | Sebut cakupan modul atau komponen yang diubah |
| dinamis / transformatif | Label megah tanpa definisi teknis | fleksibel, otomatis, atau sebutkan perubahan perilakunya |
| mulus / tanpa hambatan (seamless) | Janji promosi tanpa jaminan teknis | langsung, terintegrasi, tanpa intervensi manual |
| solusi cerdas / inovatif / mutakhir | Diksi promosi klise | Sebutkan arsitektur, algoritma, atau metode spesifik |
| segudang manfaat / berbagai macam keuntungan | Hiperbola generik | Sebutkan poin keuntungan teknis spesifik |

### 4. Pleonasme dan perangkai mubazir

Bersihkan tumpukan kata yang memiliki makna identik atau berlebihan.

| Pola terlarang | Masalah | Pengganti konkret |
|---|---|---|
| guna untuk / demi untuk | Pleonasme preposisi tujuan | untuk |
| disebabkan oleh karena / dikarenakan karena | Pleonasme konjungsi kausal | karena, akibat |
| agar supaya | Pleonasme konjungsi subordinatif | agar, supaya |
| adalah merupakan / merupakan sebuah | Pleonasme kopula dan kata tugas | adalah, atau jadikan kata benda sebagai predikat |
| sangat ... sekali / amat sangat | Pleonasme penguat derajat | sebutkan metrik riil, atau pilih salah satu kata |
| hanya ... saja | Pleonasme pembatas | hanya, saja |
| sejak dari | Pleonasme preposisi asal waktu | sejak, dari |
| contohnya seperti / antara lain misalnya | Pleonasme frasa ilustrasi | contohnya, misalnya |

### 5. Pola formulaik simetris dan triadik

Bongkar keseimbangan artifisial yang dipaksakan.

| Pola terlarang | Masalah | Cara perbaikan |
|---|---|---|
| tidak hanya X, tetapi juga Y / bukan hanya X, melainkan juga Y | Formula kontras korelatif mekanis | Tulis aksi X. Tulis aksi Y secara mandiri tanpa negasi pembuka |
| bukan sekadar X, melainkan Y / bukan cuma X, tetapi Y | Kontras artifisial | Sebut langsung esensi dari Y |
| cepat, aman, dan terpercaya | Rule-of-three klise | Pilih satu parameter performa terpenting dan tunjukkan buktinya |
| efisien, efektif, dan inovatif | Triad kata sifat hampa | Sebutkan penghematan waktu, alokasi memori, atau hasil uji |
| merupakan salah satu faktor yang / merupakan salah satu langkah | Verbositas pelemah predikat | Hilangkan. Jadikan kata benda setelahnya sebagai predikat |
| di satu sisi ..., di sisi lain ... | Formula kontras hampa | Sebutkan konsekuensi atau trade-off teknis secara langsung |

### 6. Nominalisasi berlebih dan verba pelemah

Ganti susunan kata kerja bantu yang dilemahkan dengan verba aktif berimbuhan me- atau ber-.

| Pola terlarang | Masalah | Pengganti konkret |
|---|---|---|
| melakukan implementasi / instalasi | Nominalisasi berlebih | mengimplementasikan, memasang |
| melakukan eksekusi / verifikasi | Verba bantu melemahkan aksi | mengeksekusi, memverifikasi |
| melakukan optimasi / pembaruan | Diksi birokratis | mengoptimalkan, memperbarui |
| memiliki kemampuan untuk | Calque has the ability to | dapat, mampu, bisa |
| bertujuan untuk melakukan perbaikan | Tumpukan frasa pelemah | bertujuan memperbaiki |
| memberikan dampak terhadap | Verba pasif semu | mempengaruhi, mengubah |
| memberikan kontribusi pada | Frasa nominal panjang | berkontribusi pada, membantu |
| berpotensi untuk dapat | Rantai hedging berlebih | dapat, bisa |
| diharapkan dapat membantu | Eufemisme pelemah kepastian | membantu, mempercepat |

## Kaidah sintaksis dan struktur alami

1. Utamakan kalimat aktif. Pasang subjek pelaku di depan kata kerja. Ubah "Konfigurasi ini dimuat oleh runner" menjadi "Runner memuat konfigurasi ini".
2. Variasikan panjang kalimat untuk menjaga burstiness. Gabungkan kalimat pendek berbobot (3 sampai 6 kata) untuk penegasan dengan kalimat penjelas sedang (10 sampai 15 kata). Hindari tiga kalimat berturut-turut dengan jumlah klausa sama.
3. Batasi kalimat majemuk bersarang. Hindari menumpuk anak kalimat dengan konjungsi bertingkat (meskipun, sehingga, karena, yang mana). Putus anak kalimat menjadi kalimat tunggal kedua.
4. Pasangkan batasan negatif dengan tindakan positif. Saat melarang sebuah kata atau pola, berikan padanan kata aktif penggantinya pada kalimat yang sama.
5. Bersihkan pleonasme preposisi. Hapus bentukan mubazir seperti "guna untuk", "demi untuk", atau "disebabkan karena". Gunakan "untuk" atau "karena".
6. Disiplin tanda baca. Jangan menggunakan em dash atau en dash. Gunakan koma atau titik. Jangan gunakan tanda titik dua di tengah kalimat sebagai pengganti kata hubung atau sebagai pseudo-label. Gunakan titik dua hanya untuk mengawali daftar poin, tabel, atau blok kode.

## Contoh perombakan naskah

### Contoh 1. Penjelasan sistem dan arsitektur

#### Draf sebelum perbaikan

Di era digital yang serba cepat ini, tidak dapat dipungkiri bahwa pengelolaan memori memainkan peran penting dalam lanskap komputasi modern. Arsitektur baru ini bukan sekadar sebuah pembaruan biasa, melainkan sebuah transformasi menyeluruh yang tidak hanya meningkatkan efisiensi alokasi data, tetapi juga memastikan kinerja sistem berjalan dengan mulus tanpa hambatan. Selain itu, penting untuk dicatat bahwa permadani dependensi yang rumit telah dirombak secara holistik. Sebagai kesimpulan, solusi ini merupakan bukti nyata dari keandalan rekayasa perangkat lunak kami.

#### Naskah hasil perbaikan

Pengelolaan memori menentukan stabilitas server di bawah beban kerja tinggi. Pembaruan arsitektur ini memangkas overhead alokasi memori sebesar 35 persen. Proses sinkronisasi data antarprosesor kini berjalan tanpa antrean kunci manual. Tim rekayasa juga memisahkan dependensi siklis pada layer basis data. Sistem kini dapat melayani sepuluh ribu kueri bersamaan tanpa penurunan latensi.

### Contoh 2. Komunikasi teknis dan catatan rilis

#### Draf sebelum perbaikan

Perlu diingat bahwa dalam lanskap integrasi API saat ini, verifikasi payload merupakan salah satu langkah yang sangat krusial. Selain itu, yang mana hal ini sering diabaikan oleh pengembang pemula, fungsi validasi token harus diimplementasikan secara komprehensif guna merangkul standar keamanan terbaru. Semoga panduan ini bermanfaat!

#### Naskah hasil perbaikan

Sistem wajib memverifikasi payload sebelum mengeksekusi mutasi basis data. Middleware gerbang API memvalidasi token JWT dan menolak request kedaluwarsa sebelum menyentuh controller. Tim operasi memasang konfigurasi kunci publik pada file environment produksi.

### Contoh 3. Panduan operasional dan instruksi tugas

#### Draf sebelum perbaikan

Tentu saja! Dalam rangka menavigasi kompleksitas deployment, alat yang ampuh ini hadir untuk melakukan otomatisasi terhadap pipeline rilis. Perlu digarisbawahi bahwa skrip ini memiliki kemampuan untuk melakukan verifikasi status container. Tidak kalah pentingnya, pengembang diharapkan dapat memanfaatkan fitur ini guna untuk memastikan integrasi berjalan dengan mulus.

#### Naskah hasil perbaikan

Runner mengeksekusi pipeline rilis secara otomatis setiap kali ada tag git baru. Skrip memeriksa status kesehatan container sebelum mengalihkan traffic jaringan. Pasang variabel lingkungan pada dashboard CI agar runner dapat mengakses klaster Kubernetes.
