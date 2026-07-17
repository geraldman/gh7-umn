import { useState } from 'react';
import { CheckCircle2, Copy, Download, ExternalLink, HelpCircle } from 'lucide-react';
import { STEP_ITEMS } from '../data';
import qrImage from '../../assets/agriagh7-qr.jpeg';

export default function HubungkanPage() {
  const [copyFeedback, setCopyFeedback] = useState(false);

  const handleCopyUsername = () => {
    navigator.clipboard.writeText('@AgriaGH7_bot');
    setCopyFeedback(true);
    setTimeout(() => {
      setCopyFeedback(false);
    }, 2500);
  };

  return (
    <div className="space-y-16">
      
      {/* Page Title Header */}
      <header className="text-center space-y-3">
        <h1 className="font-display-lg text-3xl md:text-4xl lg:text-5xl font-extrabold text-primary font-headline-md">
          Hubungkan ke Panen Pas
        </h1>
        <p className="font-body-lg text-sm md:text-base text-on-surface-variant max-w-xl mx-auto leading-relaxed">
          Mulai terima rekomendasi panen berbasis data harga Bank Indonesia langsung melalui aplikasi Telegram Anda.
        </p>
      </header>

      {/* Connection Layout Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        
        {/* Main Onboarding Card */}
        <section className="lg:col-span-8 bg-white border border-outline-variant/30 rounded-3xl p-8 flex flex-col items-center text-center justify-center shadow-sm space-y-6">
          
          {/* Telegram Logo Badge */}
          <div className="w-16 h-16 bg-[#0088cc]/10 text-[#0088cc] rounded-full flex items-center justify-center shadow-inner">
            <svg className="w-10 h-10 fill-current" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.5-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.11.02-1.93 1.23-5.46 3.62-.51.35-.98.52-1.4.51-.46-.01-1.35-.26-2.01-.48-.81-.27-1.45-.42-1.39-.88.03-.24.36-.48.99-.74 3.88-1.69 6.47-2.8 7.77-3.32 3.7-1.48 4.46-1.74 4.96-1.75.11 0 .36.03.52.16.13.11.17.26.19.37.02.09.02.26 0 .41z" />
            </svg>
          </div>

          <div className="space-y-2">
            <h2 className="font-headline-md text-xl md:text-2xl font-extrabold text-primary">Hubungkan Telegram Anda</h2>
            <p className="text-xs md:text-sm text-on-surface-variant max-w-lg leading-relaxed mx-auto">
              Pindai Kode QR atau klik tombol di bawah untuk mulai mengobrol dengan Panen Pas. Jika aplikasi Telegram belum terpasang, silakan unduh terlebih dahulu menggunakan tombol di bawah.
            </p>
          </div>

          {/* QR Code Frame */}
          <div className="relative bg-slate-50 p-4 rounded-2xl border border-outline-variant/30 shadow-inner">
            <img
              alt="QR Code Bot Telegram Agria"
              className="w-44 h-44 md:w-48 md:h-48 rounded-xl shadow-sm object-contain"
              src={qrImage}
            />
          </div>

          {/* Bot Username Chip */}
          <div>
            <span className="font-mono text-xs font-bold bg-[#ffdbca] text-[#331200] px-3.5 py-1.5 rounded-full border border-[#763300]/10 shadow-sm select-all">
              @AgriaGH7_bot
            </span>
          </div>

          {/* Quick Actions Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 w-full max-w-md justify-center">
            <a
              href="https://t.me/AgriaGH7_bot"
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-primary text-white font-bold py-3.5 rounded-full text-center hover:brightness-110 active:scale-95 transition-all text-xs flex items-center justify-center gap-1.5 shadow-sm"
            >
              Buka Bot Telegram
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
            <a
              href="https://telegram.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 border border-primary text-primary font-bold py-3.5 rounded-full text-center hover:bg-primary/5 active:scale-95 transition-all text-xs flex items-center justify-center gap-1.5"
            >
              Unduh Telegram
              <Download className="w-3.5 h-3.5" />
            </a>
          </div>

          {/* Copier Action */}
          <button
            onClick={handleCopyUsername}
            className={`text-xs font-bold flex items-center gap-1.5 px-4 py-2 rounded-xl transition-all cursor-pointer ${
              copyFeedback ? 'text-emerald-700 bg-emerald-50 border border-emerald-200' : 'text-primary hover:bg-slate-50 border border-transparent'
            }`}
          >
            {copyFeedback ? (
              <>
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Berhasil disalin!
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                Salin Nama Pengguna Bot
              </>
            )}
          </button>

        </section>

        {/* Sidebar Info Section */}
        <aside className="lg:col-span-4 flex flex-col justify-between">
          <div className="bg-[#004532] text-white rounded-3xl p-8 h-full flex flex-col justify-center space-y-6 border border-black/5 shadow-md">
            
            <h3 className="text-xl font-bold font-headline-md flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-[#a6f2d1]" />
              Mengapa Telegram?
            </h3>

            <ul className="space-y-4">
              {[
                'Ringan, hemat kuota dan mudah digunakan oleh siapapun',
                'Pemberitahuan peringatan panen instan real-time',
                'Rekomendasi harga pasar nasional & daerah akurat',
                'Gratis digunakan selamanya tanpa biaya tambahan'
              ].map((benefit, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[#6ffbbe] shrink-0 mt-0.5" />
                  <span className="text-xs md:text-sm text-slate-100 font-medium leading-relaxed">
                    {benefit}
                  </span>
                </li>
              ))}
            </ul>

            <div className="pt-4 border-t border-white/10 text-center">
              <p className="text-[10px] text-emerald-100 font-medium">
                Kompatibel dengan semua sistem operasi smartphone Anda.
              </p>
            </div>
          </div>
        </aside>

      </div>

      {/* Step Grid Indicators */}
      <section className="bg-slate-50 border border-outline-variant/20 rounded-3xl p-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {STEP_ITEMS.map((item, index) => (
            <div key={index} className="flex flex-col items-center text-center space-y-3 relative">
              <div className="w-12 h-12 rounded-full bg-white flex items-center justify-center text-xl shadow-sm border border-outline-variant/30">
                {item.emoji}
              </div>
              <div className="space-y-1">
                <span className="text-[10px] font-extrabold text-primary uppercase">{item.step}</span>
                <h4 className="font-bold text-xs text-primary">{item.title}</h4>
                <p className="text-[10px] text-on-surface-variant leading-relaxed max-w-[150px] mx-auto hidden md:block">
                  {item.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
