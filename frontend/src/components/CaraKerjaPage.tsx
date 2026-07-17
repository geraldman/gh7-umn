import { ArrowRight, Play, CheckCircle2, HelpCircle, ArrowRightCircle, Sparkles, AlertCircle } from 'lucide-react';
import { BENEFIT_CARDS, IMPACT_METRICS } from '../data';

interface CaraKerjaPageProps {
  onNavigateToConnect: () => void;
}

export default function CaraKerjaPage({ onNavigateToConnect }: CaraKerjaPageProps) {
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
              Temukan bagaimana mesin rekomendasi berbasis data Panen Pas membantu petani Indonesia membuat keputusan penjualan hasil tani yang lebih cerdas dan menguntungkan hanya dalam empat langkah sederhana.
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
          <p className="font-body-md text-sm text-on-surface-variant">Dari ladang hijau hingga ke tangan Pembeli Jangkar.</p>
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
              <h3 className="font-bold text-base text-primary mt-0.5">Analisis Harga & Klaster Panen</h3>
            </div>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              Sistem kami memproses tren harga Bank Indonesia dan mendeteksi panen serentak di wilayah Anda.
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
                👉 "JUAL SEKARANG — 5 petani di wilayah Anda panen bersamaan, harga lokal berisiko turun."
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
              Penawaran jual Anda diteruskan langsung ke Pembeli Jangkar yang siap menyerap panen.
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
            Mulai terima rekomendasi panen berbasis data Bank Indonesia hari ini juga. 100% gratis, ringan, aman, dan mudah digunakan langsung lewat Telegram.
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
