import { useState, useEffect } from 'react';
import { ArrowRight, Play, CheckCircle2, Cpu, HelpCircle, ArrowRightCircle, Sparkles, AlertCircle, RefreshCw } from 'lucide-react';
import { BENEFIT_CARDS, IMPACT_METRICS } from '../data';

interface CaraKerjaPageProps {
  onNavigateToConnect: () => void;
}

export default function CaraKerjaPage({ onNavigateToConnect }: CaraKerjaPageProps) {
  // Decision pipeline state
  const [pipelineCrop, setPipelineCrop] = useState<'cabai' | 'tomat' | 'bawang'>('cabai');
  const [activePipelineStep, setActivePipelineStep] = useState<number>(-1);
  const [pipelineStatus, setPipelineStatus] = useState<string>('Siap dijalankan');
  const [pipelineLogs, setPipelineLogs] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  // Run pipeline simulation
  const runPipelineSimulation = () => {
    if (isProcessing) return;
    setIsProcessing(true);
    setActivePipelineStep(0);
    setPipelineLogs([]);
    
    const cropName = pipelineCrop === 'cabai' ? '🌶️ Cabai Merah Keriting' : pipelineCrop === 'tomat' ? '🍅 Tomat Beef' : '🧅 Bawang Merah Brebes';
    
    const logs = [
      `[STEP 1] Menerima input tanggal rencana panen untuk komoditas ${cropName}...`,
      `[STEP 2] Memindai basis data harga real-time di 5 pasar induk regional...`,
      `[STEP 3] Memetakan perkiraan cuaca satelit BMKG untuk mendeteksi risiko curah hujan tinggi...`,
      `[STEP 4] Memulai model prediksi ekonomi AI Panen Pas untuk mengukur elastisitas permintaan...`,
      `[STEP 5] Menghasilkan rekomendasi waktu penjualan yang optimal untuk laba maksimal...`,
      `[STEP 6] Mencocokkan ketersediaan stok panen dengan daftar pembeli grosir B2B terverifikasi...`
    ];

    const statuses = [
      'Memvalidasi rencana tanggal panen...',
      'Mengambil data harga grosir Pasar Induk Kramat Jati, Cibitung & Johar...',
      'Mengidentifikasi risiko curah hujan tinggi yang berpotensi mengganggu logistik...',
      'Menghitung indeks penawaran dan permintaan wilayah Jawa Barat & DKI...',
      'Merumuskan rekomendasi keputusan optimal...',
      'Selesai! Mencocokkan data Anda dengan 3 pembeli supermarket premium...'
    ];

    let step = 0;
    setPipelineStatus(statuses[0]);
    setPipelineLogs([logs[0]]);

    const interval = setInterval(() => {
      step++;
      if (step < 6) {
        setActivePipelineStep(step);
        setPipelineStatus(statuses[step]);
        setPipelineLogs((prev) => [...prev, logs[step]]);
      } else {
        clearInterval(interval);
        setIsProcessing(false);
      }
    }, 1200);
  };

  useEffect(() => {
    // Reset pipeline when crop changes
    setActivePipelineStep(-1);
    setPipelineStatus('Siap dijalankan. Klik tombol simulasikan di bawah.');
    setPipelineLogs([]);
    setIsProcessing(false);
  }, [pipelineCrop]);

  return (
    <div className="space-y-20">
      
      {/* Hero Section */}
      <section className="relative pt-12 pb-16 overflow-hidden">
        <div className="max-w-container-max mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6 z-10 text-left">
            <h1 className="font-display-lg text-4xl md:text-5xl font-extrabold text-primary leading-tight font-headline-md">
              Bagaimana Panen Pas Bekerja
            </h1>
            <p className="font-body-lg text-sm md:text-base text-on-surface-variant leading-relaxed max-w-xl">
              Temukan bagaimana teknologi kecerdasan buatan Panen Pas membantu petani Indonesia membuat keputusan penjualan hasil tani yang lebih cerdas dan menguntungkan hanya dalam empat langkah sederhana.
            </p>
            <div className="flex flex-wrap gap-4 pt-2">
              <button
                onClick={onNavigateToConnect}
                className="bg-primary text-white px-8 py-4 rounded-full font-bold hover:brightness-110 active:scale-95 transition-all shadow-md hover:shadow-lg cursor-pointer flex items-center justify-center gap-2 text-sm"
              >
                Mulai Chat Sekarang
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="relative flex justify-center items-center">
            <div className="w-full aspect-square bg-[#a6f2d1] rounded-full absolute opacity-20 blur-3xl" />
            <img
              className="w-full max-w-md h-auto object-contain z-10 drop-shadow-2xl rounded-2xl"
              alt="Petani modern Indonesia memegang smartphone dengan latar belakang ladang cabai hijau yang asri"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAJcSzLZnoVFCjdvUw1s8a1ISLw4falXEWwaN3OCYaQybWBiu8Ay_Tkepn1NL9k8n2eRe6RCnaHYZKqOKHdADdzgyuj3n9gFAO7g9RlX6SsvkOBcncrO60o_Ak4REimeWNv7rDD_j-ypnARRExiLJsYE_LoJVhCXvxIddoG4Q2Ca61hB0DZ_-9854Hnb2djD5bEcGHmN2r-wSz9sdNmOGQM-l3jc9OiyOeAgrOKpaElrS6q5UmBw-EJmlPbgBe7cFClkrk_zdbqnSkh"
              referrerPolicy="no-referrer"
            />
          </div>
        </div>
      </section>

      {/* Step-by-Step Walkthrough Timeline Grid */}
      <section className="py-12 bg-white rounded-3xl border border-outline-variant/20 shadow-sm px-6 md:px-12">
        <div className="text-center max-w-2xl mx-auto mb-12 space-y-2">
          <h2 className="font-headline-md text-2xl md:text-3xl font-extrabold text-primary">Alur Kerja Sederhana</h2>
          <p className="font-body-md text-sm text-on-surface-variant">Dari ladang hijau hingga ke tangan pembeli B2B terbaik.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Step 1 */}
          <div className="bg-surface-container-low p-6 rounded-2xl border border-outline-variant/20 hover:border-primary/25 transition-all flex flex-col items-center text-center space-y-4">
            <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center font-bold text-lg shadow-sm">
              💬
            </div>
            <div>
              <span className="text-xs font-extrabold text-primary uppercase">Langkah 1</span>
              <h3 className="font-bold text-base text-primary mt-0.5">Lapor Panen Anda</h3>
            </div>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Kirim pesan sederhana seperti "Panen 5 hari lagi" melalui Telegram Bot cerdas kami.
            </p>
            <div className="w-full h-28 rounded-xl bg-white overflow-hidden border border-outline-variant/30 p-2 flex items-center justify-center">
              <div className="bg-emerald-50 text-[10px] p-2.5 rounded-xl border border-emerald-100 font-medium max-w-[90%] text-slate-800 shadow-sm">
                💬 "Lapor rencana panen cabai merah tanggal 20 Juli, berat 500kg"
              </div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="bg-surface-container-low p-6 rounded-2xl border border-outline-variant/20 hover:border-primary/25 transition-all flex flex-col items-center text-center space-y-4">
            <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center font-bold text-lg shadow-sm">
              📊
            </div>
            <div>
              <span className="text-xs font-extrabold text-primary uppercase">Langkah 2</span>
              <h3 className="font-bold text-base text-primary mt-0.5">Analisis Pasar AI</h3>
            </div>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Sistem kami langsung memproses data tren harga, cuaca satelit, dan ketersediaan stok nasional.
            </p>
            <div className="w-full h-28 rounded-xl bg-white overflow-hidden border border-outline-variant/30 p-2 flex items-center justify-center">
              <div className="w-full space-y-1 px-2">
                <div className="flex justify-between text-[8px] font-bold text-on-surface-variant">
                  <span>Indeks Permintaan</span>
                  <span className="text-primary">Tinggi (85%)</span>
                </div>
                <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-[#065f46] rounded-full" style={{ width: '85%' }} />
                </div>
                <div className="text-[8px] text-on-surface-variant leading-tight bg-slate-50 p-1.5 rounded border border-slate-100/50 mt-1">
                  💡 Permintaan cabai naik pasca musim hujan regional Jawa Tengah.
                </div>
              </div>
            </div>
          </div>

          {/* Step 3 */}
          <div className="bg-surface-container-low p-6 rounded-2xl border border-outline-variant/20 hover:border-primary/25 transition-all flex flex-col items-center text-center space-y-4">
            <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center font-bold text-lg shadow-sm">
              💡
            </div>
            <div>
              <span className="text-xs font-extrabold text-primary uppercase">Langkah 3</span>
              <h3 className="font-bold text-base text-primary mt-0.5">Rekomendasi Cerdas</h3>
            </div>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Dapatkan saran kapan waktu optimal untuk melepas panen demi memaksimalkan laba.
            </p>
            <div className="w-full h-28 rounded-xl bg-white overflow-hidden border border-outline-variant/30 p-3 flex flex-col justify-center space-y-1">
              <div className="text-[10px] font-extrabold text-primary">Rekomendasi Panen Pas:</div>
              <div className="text-[9px] text-emerald-800 bg-emerald-50 p-1.5 rounded-lg border border-emerald-100 font-bold leading-tight">
                👉 "TUNDA penjualan 2 hari. Prediksi harga naik 15% di tingkat grosir."
              </div>
            </div>
          </div>

          {/* Step 4 */}
          <div className="bg-surface-container-low p-6 rounded-2xl border border-outline-variant/20 hover:border-primary/25 transition-all flex flex-col items-center text-center space-y-4">
            <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center font-bold text-lg shadow-sm">
              🤝
            </div>
            <div>
              <span className="text-xs font-extrabold text-primary uppercase">Langkah 4</span>
              <h3 className="font-bold text-base text-primary mt-0.5">Pencocokan Pembeli</h3>
            </div>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Kami menghubungkan Anda langsung dengan rantai supermarket atau distributor grosir premium.
            </p>
            <div className="w-full h-28 rounded-xl bg-white overflow-hidden border border-outline-variant/30 p-2 flex items-center justify-center">
              <div className="space-y-1 text-center">
                <div className="text-[10px] font-bold text-primary">Pembeli Cocok:</div>
                <div className="flex justify-center gap-1">
                  <span className="text-[8px] bg-slate-100 text-slate-800 px-2 py-0.5 rounded-full font-bold">PT Fresh</span>
                  <span className="text-[8px] bg-slate-100 text-slate-800 px-2 py-0.5 rounded-full font-bold">Indomart</span>
                </div>
                <div className="text-[8px] text-emerald-600 font-bold">Gratis penjemputan dari sawah!</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive AI Decision Engine Pipeline Simulation */}
      <section className="bg-surface-container rounded-3xl py-12 px-6 md:px-12 border border-outline-variant/30">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          
          <div className="lg:col-span-5 space-y-6">
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold">
              <Cpu className="w-3.5 h-3.5" /> Mesin Analisis AI Canggih
            </span>
            <h2 className="font-headline-md text-2xl md:text-3xl font-extrabold text-primary">
              Mesin Keputusan AI Kami
            </h2>
            <p className="text-sm text-on-surface-variant leading-relaxed">
              Penasaran bagaimana algoritma kami merumuskan rekomendasi harga? Pilih salah satu komoditas dan jalankan simulator pipa analisis di sebelah kanan untuk melihat proses kalkulasi data secara real-time!
            </p>

            {/* Select simulator crop */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-on-surface-variant block">Pilih Komoditas Simulasi:</label>
              <div className="flex gap-2">
                {(['cabai', 'tomat', 'bawang'] as const).map((crop) => (
                  <button
                    key={crop}
                    onClick={() => setPipelineCrop(crop)}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                      pipelineCrop === crop
                        ? 'bg-primary text-white shadow-sm'
                        : 'bg-white border border-outline-variant/45 text-on-surface hover:bg-slate-50'
                    }`}
                  >
                    {crop === 'cabai' ? '🌶️ Cabai' : crop === 'tomat' ? '🍅 Tomat' : '🧅 Bawang'}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={runPipelineSimulation}
              disabled={isProcessing}
              className="w-full bg-[#065f46] hover:bg-[#004532] disabled:bg-slate-300 text-white font-bold py-3.5 rounded-xl text-sm transition-all flex items-center justify-center gap-2 cursor-pointer active:scale-95 shadow-sm"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" /> Sedang Menganalisis...
                </>
              ) : (
                <>
                  Simulasikan Pipa Keputusan AI
                </>
              )}
            </button>
          </div>

          {/* Stepper Pipeline Viewer */}
          <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-outline-variant/30 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <span className="text-xs font-bold text-on-surface-variant uppercase tracking-wider">Pipa Analisis AI</span>
              <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${isProcessing ? 'bg-amber-100 text-amber-800 animate-pulse' : 'bg-emerald-100 text-emerald-800'}`}>
                {isProcessing ? 'Running' : 'Ready'}
              </span>
            </div>

            {/* Pipeline Step Indicators */}
            <div className="space-y-3">
              {[
                { name: 'Tanggal Rencana Panen', desc: 'Validasi waktu rilis komoditas', icon: '📅' },
                { name: 'Analisis Harga Pasar', desc: 'Pemantauan fluktuasi grosir regional', icon: '💰' },
                { name: 'Prakiraan Cuaca Satelit', desc: 'Deteksi curah hujan & risiko penyakit', icon: '☁️' },
                { name: 'Model Prediksi AI', desc: 'Estimasi indeks penawaran vs permintaan', icon: '🤖' },
                { name: 'Rekomendasi Keputusan', desc: 'Pemilihan keputusan (Jual / Tunda)', icon: '💡' },
                { name: 'Pencocokan Rantai Pasok', desc: 'Integrasi dengan B2B Supermarket', icon: '🤝' },
              ].map((step, idx) => {
                const isActive = activePipelineStep === idx;
                const isPassed = activePipelineStep > idx;
                
                return (
                  <div
                    key={idx}
                    className={`flex items-start gap-3 p-2.5 rounded-xl transition-all border ${
                      isActive
                        ? 'bg-emerald-50/70 border-emerald-200 shadow-sm translate-x-1'
                        : isPassed
                        ? 'bg-slate-50/50 border-slate-100 opacity-60'
                        : 'bg-transparent border-transparent opacity-40'
                    }`}
                  >
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${isActive ? 'bg-primary text-white scale-110' : isPassed ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-400'}`}>
                      {isPassed ? '✓' : step.icon}
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-primary leading-tight">{idx + 1}. {step.name}</h4>
                      <p className="text-[10px] text-on-surface-variant mt-0.5">{step.desc}</p>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Live Progress Logs Display */}
            <div className="bg-slate-950 text-emerald-400 p-4 rounded-xl font-mono text-[10px] h-32 overflow-y-auto space-y-1.5 border border-slate-800">
              <div className="text-slate-500">// Log Analisis Real-Time:</div>
              {pipelineLogs.map((log, index) => (
                <div key={index} className="animate-fade-in">{log}</div>
              ))}
              {isProcessing && (
                <div className="flex items-center gap-1.5 text-emerald-400 animate-pulse mt-1">
                  <span>●</span> <span>{pipelineStatus}</span>
                </div>
              )}
              {pipelineLogs.length === 0 && !isProcessing && (
                <div className="text-slate-500 font-medium">Belum ada aktivitas. Silakan klik "Simulasikan Pipa Keputusan AI" untuk memulai.</div>
              )}
              {!isProcessing && pipelineLogs.length > 0 && (
                <div className="text-emerald-300 font-bold border-t border-slate-800/80 pt-1.5 mt-1">
                  ✓ Analisis Sukses! Rekomendasi siap dikirim ke Telegram petani.
                </div>
              )}
            </div>
          </div>

        </div>
      </section>

      {/* Benefits Grid Section */}
      <section className="space-y-10">
        <div className="text-center space-y-2">
          <h2 className="font-headline-md text-2xl md:text-3xl font-extrabold text-primary">Keuntungan Utama</h2>
          <p className="font-body-md text-sm text-on-surface-variant max-w-lg mx-auto">
            Memaksimalkan kesejahteraan petani modern Indonesia lewat integrasi teknologi cerdas.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {BENEFIT_CARDS.map((ben) => (
            <div
              key={ben.id}
              className="bg-white p-6 rounded-2xl border border-outline-variant/20 hover:border-primary/25 transition-all shadow-sm space-y-4 hover:-translate-y-1 duration-300"
            >
              <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary font-bold text-lg">
                📈
              </div>
              <h3 className="font-bold text-base text-primary leading-tight">{ben.title}</h3>
              <p className="text-xs text-on-surface-variant leading-relaxed">{ben.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Impact Statistics Counter Row */}
      <section className="bg-primary text-white py-12 px-6 rounded-3xl">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
          {IMPACT_METRICS.map((metric, index) => (
            <div
              key={index}
              className="p-6 rounded-2xl bg-white/10 text-center border border-white/5 shadow-sm space-y-1"
            >
              <div className="text-4xl font-extrabold text-[#a6f2d1] font-headline-md">{metric.value}</div>
              <div className="text-[11px] text-on-primary-container font-semibold uppercase tracking-wider">{metric.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Bottom CTA Card */}
      <section className="bg-gradient-to-tr from-[#004532] to-[#065f46] rounded-3xl p-8 md:p-12 text-white relative overflow-hidden text-center shadow-lg">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-80 h-80 bg-white rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-primary-fixed rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
        </div>

        <div className="relative z-10 max-w-xl mx-auto space-y-6">
          <h2 className="text-3xl font-extrabold font-headline-md">Siap Mencoba Panen Pas?</h2>
          <p className="text-sm text-on-primary-container leading-relaxed">
            Mulai terima rekomendasi panen bertenaga AI hari ini juga. 100% gratis, ringan, aman, dan mudah digunakan langsung lewat Telegram.
          </p>
          <div className="pt-2">
            <button
              onClick={onNavigateToConnect}
              className="bg-white text-primary px-8 py-4 rounded-full font-bold text-sm hover:bg-surface transition-all active:scale-95 shadow-md cursor-pointer inline-flex items-center gap-2"
            >
              Hubungkan Telegram Bot Sekarang
              <ArrowRight className="w-4 h-4 text-primary" />
            </button>
          </div>
        </div>
      </section>

    </div>
  );
}
