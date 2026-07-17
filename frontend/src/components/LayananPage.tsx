import { Sparkles, Play, ShieldAlert, ArrowRight, BookOpen, ChevronRight } from 'lucide-react';
import GrassCanvas from './GrassCanvas';
import ChatSimulator from './ChatSimulator';
import { PROBLEM_CARDS } from '../data';

interface LayananPageProps {
  onNavigateToConnect: () => void;
  onNavigateToWorkflow: () => void;
}

export default function LayananPage({ onNavigateToConnect, onNavigateToWorkflow }: LayananPageProps) {
  return (
    <div className="space-y-20">
      
      {/* Hero Section with Live Grass Background */}
      <section className="relative overflow-hidden bg-gradient-to-b from-[#f9f9ff] to-[#f0f3ff] pt-20 pb-16 min-h-[550px] flex items-center rounded-3xl border border-outline-variant/20 shadow-sm px-6 md:px-12">
        <GrassCanvas />
        
        <div className="relative z-10 max-w-container-max mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 items-center w-full">
          {/* Hero text */}
          <div className="lg:col-span-7 space-y-6 text-left">
            <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-primary/10 text-primary font-bold text-xs border border-primary/25">
              <Sparkles className="w-3.5 h-3.5" /> Inovasi Agritech Modern 2026
            </span>
            <h1 className="font-display-lg text-4xl md:text-5xl lg:text-6xl font-extrabold text-primary leading-[1.15] tracking-tight font-headline-md">
              Jual Lebih Cerdas.<br />
              <span className="text-[#065f46]">Kurangi Limbah.</span><br />
              Raih Lebih Banyak.
            </h1>
            <p className="font-body-lg text-sm md:text-base text-on-surface-variant max-w-xl leading-relaxed">
              Panen Pas membantu petani kecil Indonesia menentukan kapan dan di mana tepatnya menjual hasil panen menggunakan WhatsApp / Telegram dan wawasan analisis pasar waktu nyata.
            </p>
            <div className="flex flex-wrap gap-4 pt-2">
              <button
                onClick={onNavigateToConnect}
                className="bg-primary text-white px-8 py-4 rounded-full font-bold hover:brightness-110 active:scale-95 transition-all shadow-md hover:shadow-lg cursor-pointer flex items-center justify-center gap-2 text-sm"
              >
                Hubungkan Bot
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                onClick={onNavigateToWorkflow}
                className="bg-white text-on-surface border border-outline-variant/60 px-8 py-4 rounded-full font-bold hover:bg-surface transition-all shadow-sm active:scale-95 cursor-pointer flex items-center justify-center gap-2 text-sm"
              >
                <Play className="w-4 h-4 text-primary fill-current" />
                Tonton Demo / Cara Kerja
              </button>
            </div>
          </div>

          {/* Hero graphic mockup */}
          <div className="lg:col-span-5 relative flex justify-center">
            <div className="absolute -top-10 -right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl" />
            <div className="absolute -bottom-10 -left-10 w-64 h-64 bg-secondary-fixed-dim/20 rounded-full blur-3xl" />
            
            <div className="relative rounded-2xl overflow-hidden shadow-2xl transform lg:rotate-1 border-4 border-white bg-white w-full max-w-sm">
              <img
                alt="Panen Pas Bot Telegram Preview"
                className="w-full h-auto object-cover aspect-[4/3] block"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuBGrEKlysvtJze9u_esHLfsDX5OKfo3nwVnYeQFmMQ4KzAhgUUu3MS-0Rb4DPYsfVGy2356usZti5rybrjtXTLxFDs1hFgRyHwnqBbQL31P3PKQSJEQHydYmqYwyVP7K68XK6DsP_27gScPY1xWGo_9sYA777jzDz0ByjRq8Xn3fz8XtDRN_NX6NeoyTlLTDxeJMfyBjP8E-gygchnab7fwoOAup0vuJqc6Egp6kHODGdKEMUttLeBGoeQuKFO7PBPcXTzm_WSe33TP"
                referrerPolicy="no-referrer"
              />
              
              {/* Floating micro profit card */}
              <div className="absolute -bottom-4 -right-4 md:right-4 bg-white p-4 rounded-2xl shadow-xl border border-outline-variant/30 flex items-center gap-3 animate-bounce" style={{ animationDuration: '3s' }}>
                <div className="w-10 h-10 rounded-full bg-secondary-fixed text-secondary flex items-center justify-center font-bold">
                  📈
                </div>
                <div>
                  <p className="text-[10px] text-on-surface-variant font-bold leading-none">Rata-rata Kenaikan Laba</p>
                  <p className="text-lg font-extrabold text-primary leading-tight font-headline-md">+34.2%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="bg-surface-container-low rounded-3xl py-12 px-6 md:px-12 border border-outline-variant/30">
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-10">
          <h2 className="font-headline-md text-2xl md:text-3xl font-extrabold text-primary">Tantangan Pertanian Saat Ini</h2>
          <p className="font-body-md text-sm md:text-base text-on-surface-variant leading-relaxed">
            Indonesia kehilangan jumlah pangan yang signifikan pasca panen. Petani kecil sering menderita akibat fluktuasi harga yang tidak terduga dan pasokan pasar berlebih karena waktu panen yang serentak.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Problem Bento Cards */}
          {PROBLEM_CARDS.map((prob) => (
            <div
              key={prob.id}
              className="bg-white p-8 rounded-2xl border border-outline-variant/20 shadow-sm flex flex-col items-center text-center justify-center space-y-4 transition-all hover:border-primary/25"
            >
              <div className="w-16 h-16 rounded-full flex items-center justify-center bg-red-50 text-red-600 border border-red-100">
                <ShieldAlert className="w-8 h-8" />
              </div>
              <h3 className="font-bold text-lg text-primary">{prob.title}</h3>
              <p className="text-sm text-on-surface-variant leading-relaxed max-w-sm">{prob.description}</p>
            </div>
          ))}
        </div>

        {/* Highlight Stats Infographic */}
        <div className="mt-8 bg-primary text-white p-8 rounded-2xl shadow-lg relative overflow-hidden group">
          <div className="absolute -right-10 -bottom-10 text-[180px] opacity-10 font-bold select-none rotate-12 transition-transform duration-500 group-hover:rotate-6">
            🗑️
          </div>
          <div className="relative z-10 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            <div className="md:col-span-8 space-y-2">
              <span className="bg-secondary px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase">
                Data Nasional
              </span>
              <h3 className="text-3xl font-extrabold font-headline-md">300kg / Kapita / Tahun</h3>
              <p className="text-sm text-on-primary-container leading-relaxed">
                Limbah makanan per kapita setiap tahun di Indonesia. Sekitar <span className="font-bold text-white underline decoration-wavy">75% dari jumlah ini sebenarnya dapat dihindari</span> dengan penentuan waktu panen yang tepat dan manajemen logistik terintegrasi.
              </p>
            </div>
            <div className="md:col-span-4 w-full">
              <div className="bg-white/10 p-4 rounded-xl border border-white/10 space-y-2">
                <div className="flex justify-between text-xs font-semibold">
                  <span>Dapat Dihindari Panen Pas</span>
                  <span>75%</span>
                </div>
                <div className="h-2.5 w-full bg-white/20 rounded-full overflow-hidden">
                  <div className="h-full bg-primary-fixed rounded-full transition-all duration-1000" style={{ width: '75%' }} />
                </div>
                <p className="text-[10px] text-primary-fixed font-bold">Membantu mengurangi kerugian finansial petani</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Chat Solution Demo Section */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        <div className="lg:col-span-6 space-y-6">
          <h2 className="font-headline-md text-3xl font-extrabold text-primary tracking-tight">
            Bagaimana Panen Pas Membantu Anda
          </h2>
          <p className="font-body-md text-on-surface-variant leading-relaxed">
            Petani hanya perlu mengirimkan pesan teks singkat berisi nama komoditas dan perkiraan tanggal panen mereka. Sistem asisten cerdas Panen Pas AI akan segera memberi tahu rekomendasi harga terbaik dan daftar pembeli grosir.
          </p>
          
          <div className="space-y-4">
            <div className="flex gap-4 p-4 rounded-xl hover:bg-surface-container-low transition-colors border border-transparent hover:border-outline-variant/30">
              <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary shrink-0 font-bold text-lg">
                📱
              </div>
              <div>
                <h4 className="font-bold text-primary mb-1 text-sm md:text-base">Antarmuka yang Akrab</h4>
                <p className="text-xs md:text-sm text-on-surface-variant leading-relaxed">
                  Bekerja sepenuhnya di dalam WhatsApp dan Telegram. Petani tidak perlu mengunduh aplikasi khusus yang rumit atau belajar sistem baru yang membingungkan.
                </p>
              </div>
            </div>

            <div className="flex gap-4 p-4 rounded-xl hover:bg-surface-container-low transition-colors border border-transparent hover:border-outline-variant/30">
              <div className="w-12 h-12 bg-secondary-fixed text-secondary rounded-xl flex items-center justify-center shrink-0 font-bold text-lg">
                🧠
              </div>
              <div>
                <h4 className="font-bold text-primary mb-1 text-sm md:text-base">Wawasan Berbasis AI</h4>
                <p className="text-xs md:text-sm text-on-surface-variant leading-relaxed">
                  Mesin kami terus memprediksi fluktuasi harga pasar, menganalisis data historis pasar, ketersediaan stok, dan cuaca lokal untuk menemukan jendela penjualan paling menguntungkan.
                </p>
              </div>
            </div>
          </div>

          <div className="pt-2">
            <button
              onClick={onNavigateToWorkflow}
              className="inline-flex items-center gap-1.5 font-bold text-sm text-primary hover:underline decoration-2 cursor-pointer group"
            >
              Lihat Alur Kerja Selengkapnya
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        </div>

        {/* Live Simulator Panel */}
        <div className="lg:col-span-6 bg-gradient-to-tr from-surface-container to-white rounded-3xl p-6 border border-outline-variant/20 shadow-sm">
          <ChatSimulator />
        </div>
      </section>

      {/* Bottom Process Steps Row */}
      <section className="bg-primary text-white py-12 px-6 rounded-3xl text-center space-y-10 shadow-md">
        <div className="space-y-2">
          <h2 className="text-2xl font-bold font-headline-md">Sederhana, Cepat & Menguntungkan</h2>
          <p className="text-sm text-on-primary-container max-w-lg mx-auto">
            Hanya butuh 3 langkah instan untuk meningkatkan nilai jual panen Anda bersama asisten cerdas Panen Pas.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-3">
            <div className="w-14 h-14 rounded-full bg-white/10 flex items-center justify-center mx-auto text-2xl shadow-sm border border-white/5">
              📅
            </div>
            <h4 className="font-bold text-base">1. Lapor Rencana Panen</h4>
            <p className="text-xs text-on-primary-container leading-relaxed px-4">
              Kirim rencana panen dan jumlah komoditas lewat pesan chat biasa di Telegram.
            </p>
          </div>

          <div className="space-y-3">
            <div className="w-14 h-14 rounded-full bg-white/10 flex items-center justify-center mx-auto text-2xl shadow-sm border border-white/5">
              📊
            </div>
            <h4 className="font-bold text-base">2. Dapatkan Rekomendasi</h4>
            <p className="text-xs text-on-primary-container leading-relaxed px-4">
              AI menganalisis harga pasar waktu nyata dan memberi tahu kapan tanggal rilis terbaik.
            </p>
          </div>

          <div className="space-y-3">
            <div className="w-14 h-14 rounded-full bg-white/10 flex items-center justify-center mx-auto text-2xl shadow-sm border border-white/5">
              🤝
            </div>
            <h4 className="font-bold text-base">3. Hubungkan Pembeli</h4>
            <p className="text-xs text-on-primary-container leading-relaxed px-4">
              Terhubung langsung dengan pembeli B2B grosir premium yang siap menjemput panen dari ladang.
            </p>
          </div>
        </div>

        <div className="pt-4">
          <button
            onClick={onNavigateToConnect}
            className="bg-white text-primary px-8 py-3.5 rounded-full font-bold text-sm hover:bg-surface transition-all active:scale-95 shadow-md cursor-pointer inline-flex items-center gap-2"
          >
            Hubungkan Sekarang Secara Gratis
            <ArrowRight className="w-4 h-4 text-primary" />
          </button>
        </div>
      </section>

    </div>
  );
}
