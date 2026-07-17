import { ArrowLeft, MoreVertical, Smile, Paperclip, Mic } from 'lucide-react';

export default function TelegramMockup() {
  return (
    <div id="telegram-mockup" className="w-full bg-[#b1ccb2] rounded-3xl overflow-hidden shadow-2xl border border-slate-300/80 font-sans flex flex-col h-[560px] relative select-none pointer-events-none">
      {/* Subtle Telegram Doodle Pattern Background Layer */}
      <div 
        className="absolute inset-0 opacity-[0.06] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='%231e3a1e' fill-opacity='1'%3E%3Cpath d='M15 15h2v2h-2zm10 0h2v2h-2zm-10 10h2v2h-2zm10 0h2v2h-2zm15-15h2v2h-2zm10 0h2v2h-2zm-10 10h2v2h-2zm10 0h2v2h-2zM15 45h2v2h-2zm10 0h2v2h-2zm-10 10h2v2h-2zm10 0h2v2h-2zm15-15h2v2h-2zm10 0h2v2h-2zm-10 10h2v2h-2zm10 0h2v2h-2z'/%3E%3Cpath d='M40 5c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 40c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm25-30c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-50 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z'/%3E%3C/g%3E%3C/svg%3E")`
        }}
      />

      {/* 1. Android Status Bar (Static Image-style) */}
      <div className="bg-white/95 backdrop-blur px-4 pt-2.5 pb-1 flex items-center justify-between text-[11px] font-medium text-slate-800 z-10 shrink-0">
        <div className="flex items-center gap-1.5">
          <span>15:41</span>
          {/* Simulated tiny WhatsApp icon */}
          <div className="w-3 h-3 rounded-full bg-[#25D366] flex items-center justify-center text-[7px] text-white font-bold leading-none scale-90">
            w
          </div>
          <span className="text-[9px] opacity-60">•••</span>
        </div>
        <div className="flex items-center gap-1.5">
          {/* Connection Icons */}
          <svg className="w-3.5 h-3.5 fill-current opacity-80" viewBox="0 0 24 24">
            <path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c3.9 3.89 10.22 3.89 14.12 0l1.38-1.79C21.08 16.07 21.82 14.12 21.82 12c0-4.97-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/>
          </svg>
          <div className="flex items-end gap-[1px] h-2.5">
            <div className="w-[1.5px] h-1 bg-current rounded-full" />
            <div className="w-[1.5px] h-1.5 bg-current rounded-full" />
            <div className="w-[1.5px] h-2 bg-current rounded-full" />
            <div className="w-[1.5px] h-2.5 bg-current rounded-full" />
          </div>
          {/* Battery */}
          <div className="flex items-center gap-0.5 border border-slate-700 rounded-sm px-[2px] py-[1px] text-[8px] font-bold h-3 leading-none scale-95">
            <span>23</span>
          </div>
        </div>
      </div>

      {/* 2. Telegram App Header */}
      <div className="bg-white/95 backdrop-blur px-3 py-2 flex items-center justify-between border-b border-slate-200/60 z-10 shrink-0">
        <div className="flex items-center gap-2.5">
          <ArrowLeft className="w-5 h-5 text-slate-700" />
          
          {/* Avatar Circle */}
          <div className="w-9 h-9 rounded-full bg-[#52a2d4] flex items-center justify-center text-white font-semibold text-sm shadow-inner">
            A
          </div>
          
          {/* Name and Bot Status */}
          <div className="flex flex-col">
            <span className="font-bold text-slate-800 text-[14px] leading-tight">AgriaGH7</span>
            <span className="text-[11px] text-slate-400 leading-none">bot</span>
          </div>
        </div>
        
        {/* Right Action Menu */}
        <MoreVertical className="w-5 h-5 text-slate-500" />
      </div>

      {/* 3. Chat Conversation Area */}
      <div className="flex-1 overflow-y-auto px-3.5 py-3 space-y-3.5 z-10 scrollbar-none">
        {/* Date Stamp */}
        <div className="flex justify-center my-1.5">
          <span className="bg-[#7fa87f]/80 text-white text-[11px] font-medium px-3 py-1 rounded-full shadow-sm">
            July 17
          </span>
        </div>

        {/* User Message: /start */}
        <div className="flex justify-end">
          <div className="bg-[#effdde] text-slate-800 rounded-2xl rounded-tr-sm px-3.5 py-2 max-w-[85%] shadow-sm text-sm relative flex flex-col">
            <span className="pr-12 text-[14px]">/start</span>
            <div className="self-end flex items-center gap-1 mt-0.5">
              <span className="text-[9px] text-[#4f9c52]">15:40</span>
              <span className="text-[11px] text-[#4f9c52] font-bold leading-none">✓✓</span>
            </div>
          </div>
        </div>

        {/* Bot Message: 📍 Brebes. Berapa hari... */}
        <div className="flex justify-start">
          <div className="bg-white text-slate-800 rounded-2xl rounded-tl-sm px-3.5 py-2 max-w-[85%] shadow-sm text-sm flex flex-col">
            <span className="text-[14px] leading-relaxed">
              📍 Brebes.<br />Berapa hari lagi sampai panen? (angka saja, misal: 2)
            </span>
            <span className="self-end text-[9px] text-slate-400 mt-1">15:40</span>
          </div>
        </div>

        {/* User Message: 2 */}
        <div className="flex justify-end">
          <div className="bg-[#effdde] text-slate-800 rounded-2xl rounded-tr-sm px-3.5 py-2 max-w-[85%] shadow-sm text-sm flex flex-col">
            <span className="pr-12 text-[14px]">2</span>
            <div className="self-end flex items-center gap-1 mt-0.5">
              <span className="text-[9px] text-[#4f9c52]">15:40</span>
              <span className="text-[11px] text-[#4f9c52] font-bold leading-none">✓✓</span>
            </div>
          </div>
        </div>

        {/* Bot Message: Perkiraan jumlah panen... */}
        <div className="flex justify-start">
          <div className="bg-white text-slate-800 rounded-2xl rounded-tl-sm px-3.5 py-2 max-w-[85%] shadow-sm text-sm flex flex-col">
            <span className="text-[14px] leading-relaxed">
              Perkiraan jumlah panen dalam kg? (angka saja, misal: 150 – ketik 0 jika belum tahu)
            </span>
            <span className="self-end text-[9px] text-slate-400 mt-1">15:40</span>
          </div>
        </div>

        {/* User Message: 150 */}
        <div className="flex justify-end">
          <div className="bg-[#effdde] text-slate-800 rounded-2xl rounded-tr-sm px-3.5 py-2 max-w-[85%] shadow-sm text-sm flex flex-col">
            <span className="pr-12 text-[14px]">150</span>
            <div className="self-end flex items-center gap-1 mt-0.5">
              <span className="text-[9px] text-[#4f9c52]">15:41</span>
              <span className="text-[11px] text-[#4f9c52] font-bold leading-none">✓✓</span>
            </div>
          </div>
        </div>

        {/* Bot Message: Nomor HP/WA... */}
        <div className="flex justify-start">
          <div className="bg-white text-slate-800 rounded-2xl rounded-tl-sm px-3.5 py-2 max-w-[85%] shadow-sm text-sm flex flex-col">
            <span className="text-[14px] leading-relaxed">
              Nomor HP/WA yang bisa dihubungi pembeli? (misal: 081234567890)
            </span>
            <span className="self-end text-[9px] text-slate-400 mt-1">15:41</span>
          </div>
        </div>
      </div>

      {/* 4. Telegram Input Footer */}
      <div className="p-2 pb-1 flex items-center gap-2 bg-transparent z-10 shrink-0">
        {/* Message Input Container */}
        <div className="flex-1 bg-white rounded-full flex items-center px-3 py-2 shadow-sm border border-slate-200/50">
          <Smile className="w-5 h-5 text-slate-400 mr-2 shrink-0" />
          <div className="flex-1 text-sm text-slate-400 py-0.5 select-none">
            Message
          </div>
          <Paperclip className="w-5 h-5 text-slate-400 ml-2 shrink-0" />
        </div>

        {/* Voice Button */}
        <div className="w-9 h-9 rounded-full bg-[#2fa6e7] flex items-center justify-center text-white shadow-sm shrink-0">
          <Mic className="w-4.5 h-4.5" />
        </div>
      </div>

      {/* 5. Android Bottom Gesture Bar */}
      <div className="w-full h-4 bg-transparent flex items-center justify-center shrink-0 z-10 pb-1">
        <div className="w-28 h-1 bg-slate-800/80 rounded-full" />
      </div>
    </div>
  );
}
