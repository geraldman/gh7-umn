/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Menu, X, Facebook, Mail, Share2, MessageSquare, BookOpen, Send, Calendar, CheckCircle2 } from 'lucide-react';
import { TabType } from './types';
import LayananPage from './components/LayananPage';
import CaraKerjaPage from './components/CaraKerjaPage';
import HubungkanPage from './components/HubungkanPage';
import Logo from './components/Logo';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabType>('layanan');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  const handleTabChange = (tab: TabType) => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-[#f9f9ff] flex flex-col font-sans">
      
      {/* Sticky Top Navigation Bar */}
      <nav className="w-full bg-white/90 backdrop-blur-md border-b border-outline-variant/30 sticky top-0 z-50 shadow-sm transition-all">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          
          {/* Brand Logo & Name */}
          <div 
            onClick={() => handleTabChange('layanan')} 
            className="flex items-center gap-2 cursor-pointer group"
          >
            <div className="w-12 h-12 flex items-center justify-center group-hover:scale-105 transition-transform duration-300">
              <Logo size={44} />
            </div>
            <span className="font-headline text-2xl font-extrabold text-primary tracking-tight">
              Panen Pas
            </span>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center gap-8 font-medium text-sm">
            <button
              onClick={() => handleTabChange('layanan')}
              className={`pb-1 transition-all hover:text-primary cursor-pointer ${
                activeTab === 'layanan'
                  ? 'text-primary font-bold border-b-2 border-primary'
                  : 'text-on-surface-variant'
              }`}
            >
              Layanan
            </button>
            <button
              onClick={() => handleTabChange('cara_kerja')}
              className={`pb-1 transition-all hover:text-primary cursor-pointer ${
                activeTab === 'cara_kerja'
                  ? 'text-primary font-bold border-b-2 border-primary'
                  : 'text-on-surface-variant'
              }`}
            >
              Cara Kerja
            </button>
            <button
              onClick={() => handleTabChange('hubungkan')}
              className={`pb-1 transition-all hover:text-primary cursor-pointer ${
                activeTab === 'hubungkan'
                  ? 'text-primary font-bold border-b-2 border-primary'
                  : 'text-on-surface-variant'
              }`}
            >
              Hubungkan Bot
            </button>
          </div>

          {/* Action Buttons */}
          <div className="hidden md:flex items-center gap-4">
            <button
              onClick={() => setModalOpen(true)}
              className="bg-primary text-white px-6 py-2.5 rounded-full font-bold text-xs hover:brightness-110 active:scale-95 transition-all shadow-sm cursor-pointer"
            >
              Mulai Sekarang
            </button>
          </div>

          {/* Mobile Menu Hamburger Trigger */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-primary p-2 hover:bg-slate-50 rounded-xl transition-colors cursor-pointer"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

        </div>

        {/* Mobile Navigation Dropdown Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-white border-b border-outline-variant/30 px-6 py-4 space-y-3 flex flex-col font-medium text-sm animate-fade-in">
            <button
              onClick={() => handleTabChange('layanan')}
              className={`py-2 text-left hover:text-primary border-b border-slate-50 ${
                activeTab === 'layanan' ? 'text-primary font-bold' : 'text-on-surface-variant'
              }`}
            >
              Layanan
            </button>
            <button
              onClick={() => handleTabChange('cara_kerja')}
              className={`py-2 text-left hover:text-primary border-b border-slate-50 ${
                activeTab === 'cara_kerja' ? 'text-primary font-bold' : 'text-on-surface-variant'
              }`}
            >
              Cara Kerja
            </button>
            <button
              onClick={() => handleTabChange('hubungkan')}
              className={`py-2 text-left hover:text-primary border-b border-slate-50 ${
                activeTab === 'hubungkan' ? 'text-primary font-bold' : 'text-on-surface-variant'
              }`}
            >
              Hubungkan Bot
            </button>
            <div className="pt-2">
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  setModalOpen(true);
                }}
                className="w-full bg-primary text-white py-3 rounded-xl font-bold text-xs hover:brightness-110 active:scale-95 transition-all text-center shadow-sm block"
              >
                Mulai Sekarang
              </button>
            </div>
          </div>
        )}
      </nav>

      {/* Main Dynamic View Content Container */}
      <main className="flex-1 max-w-7xl mx-auto px-6 py-10 w-full">
        {activeTab === 'layanan' && (
          <LayananPage
            onNavigateToConnect={() => handleTabChange('hubungkan')}
            onNavigateToWorkflow={() => handleTabChange('cara_kerja')}
          />
        )}

        {activeTab === 'cara_kerja' && (
          <CaraKerjaPage
            onNavigateToConnect={() => handleTabChange('hubungkan')}
          />
        )}

        {activeTab === 'hubungkan' && <HubungkanPage />}
      </main>

      {/* Global Application Footer */}
      <footer className="w-full bg-white border-t border-outline-variant/30 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          
          {/* Logo and Brand Details */}
          <div className="md:col-span-6 space-y-4 text-left">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 flex items-center justify-center">
                <Logo size={36} />
              </div>
              <span className="font-headline text-lg font-bold text-primary tracking-tight">
                Panen Pas
              </span>
            </div>
            <p className="text-xs md:text-sm text-on-surface-variant max-w-sm leading-relaxed">
              Solusi Pertanian Cerdas untuk petani modern Indonesia. Menjembatani teknologi modern dan kearifan tradisi untuk kesejahteraan petani.
            </p>
            <p className="text-[11px] text-slate-400 font-medium">
              © 2026 Panen Pas. Solusi Pertanian Cerdas. Hak cipta dilindungi undang-undang.
            </p>
          </div>

          {/* Quick Informational Links */}
          <div className="md:col-span-3 space-y-3 text-left">
            <h4 className="text-xs font-bold text-primary uppercase tracking-wider">Halaman Utama</h4>
            <div className="flex flex-col gap-2 text-xs text-on-surface-variant font-medium">
              <button onClick={() => handleTabChange('layanan')} className="text-left hover:text-primary transition-colors cursor-pointer">Layanan Kami</button>
              <button onClick={() => handleTabChange('cara_kerja')} className="text-left hover:text-primary transition-colors cursor-pointer">Cara Kerja AI</button>
              <button onClick={() => handleTabChange('hubungkan')} className="text-left hover:text-primary transition-colors cursor-pointer">Hubungkan Telegram</button>
            </div>
          </div>

          {/* Legals & Social Contacts */}
          <div className="md:col-span-3 space-y-4 text-left">
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-primary uppercase tracking-wider">Bantuan & Hubungi</h4>
              <div className="flex flex-col gap-2 text-xs text-on-surface-variant font-medium">
                <a href="mailto:support@panenpas.id" className="hover:text-primary transition-colors">support@panenpas.id</a>
              </div>
            </div>

            {/* Social Icons Row */}
            <div className="flex gap-3 text-primary pt-1">
              <a href="#" className="p-2 bg-slate-50 hover:bg-primary/5 hover:scale-105 rounded-full transition-all" title="Facebook">
                <Facebook className="w-4 h-4" />
              </a>
              <a href="mailto:support@panenpas.id" className="p-2 bg-slate-50 hover:bg-primary/5 hover:scale-105 rounded-full transition-all" title="Mail">
                <Mail className="w-4 h-4" />
              </a>
              <a href="#" className="p-2 bg-slate-50 hover:bg-primary/5 hover:scale-105 rounded-full transition-all" title="Bagikan">
                <Share2 className="w-4 h-4" />
              </a>
            </div>
          </div>

        </div>
      </footer>

      {/* Onboarding Connect Bot Popup Modal Overlay */}
      {modalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md transition-all duration-300">
          <div className="bg-white w-full max-w-md rounded-[2.5rem] overflow-hidden premium-shadow relative p-8 md:p-10 text-center border border-outline-variant/30 scale-100 animate-scale-up">
            
            {/* Close Modal Button */}
            <button
              onClick={() => setModalOpen(false)}
              className="absolute top-6 right-6 w-9 h-9 rounded-full bg-slate-50 flex items-center justify-center hover:bg-slate-100 transition-colors cursor-pointer"
            >
              <X className="w-5 h-5 text-on-surface-variant" />
            </button>

            <div className="space-y-6">
              <div className="w-20 h-20 flex items-center justify-center mx-auto">
                <Logo size={72} />
              </div>

              <div className="space-y-2">
                <h3 className="font-headline text-2xl font-extrabold text-primary">Hubungkan Bot</h3>
                <p className="text-xs text-on-surface-variant leading-relaxed max-w-sm mx-auto">
                  Pindai kode QR di bawah menggunakan aplikasi Telegram ponsel Anda atau klik tombol untuk mulai menggunakan asisten cerdas Panen Pas AI secara gratis.
                </p>
              </div>

              {/* QR Code Container */}
              <div className="bg-slate-50 p-4 rounded-3xl inline-block border border-outline-variant/30 shadow-inner">
                <img
                  alt="QR Code"
                  className="w-44 h-44 object-contain"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuC8GkyouUsrc_AnYN3QGL6hZJrn6Bqe3OV8VoQIJrvOorrEGDlM_hafhObeF08Q-8sRkDfMcBDjNJWQOl11TerbCVMCgh3bWGNYxy46eK_0awqZ4XkSyxQx8qDRR3jmkAfHE85Ou1DHZ968pBKuNqvWQX5WI7yswUZYZEUINyQ4QUefB734ExDhMStZkoV6zMU8mWUkrP9ZIcmXo49Byxg-1yYkadEkelD6mJ9P4-1dJxqS2VK0rGUnqZAbDevM7OMv4leNzvQXzZAn"
                  referrerPolicy="no-referrer"
                />
              </div>

              {/* Action Button */}
              <a
                href="https://t.me/AgriaGH7_bot"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full bg-primary hover:brightness-110 text-white font-bold py-4 rounded-xl text-sm transition-all text-center block shadow-md hover:shadow-lg active:scale-95"
              >
                Buka di Telegram
              </a>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
