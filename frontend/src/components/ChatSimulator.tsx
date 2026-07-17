import { useState, useEffect, useRef, FormEvent } from 'react';
import { Send, ArrowLeft, MoreVertical, Paperclip, Mic, Sparkles } from 'lucide-react';
import { ChatMessage } from '../types';
import { CHAT_PRESETS } from '../data';
import Logo from './Logo';

const SCENARIOS = [
  { id: 'jual', label: 'Jual', icon: '🟢' },
  { id: 'tunggu', label: 'Tunggu', icon: '🔵' },
  { id: 'jadwal', label: 'Jadwal', icon: '🟡' },
] as const;

export default function ChatSimulator() {
  const [activePreset, setActivePreset] = useState<'jual' | 'tunggu' | 'jadwal'>('jual');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  // Load preset conversation
  useEffect(() => {
    setMessages([]);
    setIsTyping(false);
    
    // Simulate type-writer conversation step-by-step
    const presetMsgs = CHAT_PRESETS[activePreset];
    if (!presetMsgs) return;

    let currentIdx = 0;
    const timeouts: NodeJS.Timeout[] = [];

    const sendNextMessage = () => {
      if (currentIdx >= presetMsgs.length) return;

      const nextMsg = presetMsgs[currentIdx];
      
      if (nextMsg.sender === 'bot') {
        setIsTyping(true);
        const typingTimeout = setTimeout(() => {
          setIsTyping(false);
          setMessages((prev) => [...prev, nextMsg]);
          currentIdx++;
          
          const nextTimeout = setTimeout(sendNextMessage, 1200);
          timeouts.push(nextTimeout);
        }, 1500);
        timeouts.push(typingTimeout);
      } else {
        setMessages((prev) => [...prev, nextMsg]);
        currentIdx++;
        const nextTimeout = setTimeout(sendNextMessage, 1000);
        timeouts.push(nextTimeout);
      }
    };

    // Start simulation after 400ms
    const startTimeout = setTimeout(sendNextMessage, 400);
    timeouts.push(startTimeout);

    return () => {
      timeouts.forEach(clearTimeout);
    };
  }, [activePreset]);

  // Scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSendMessage = (e: FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    const typedText = inputText.toLowerCase();
    setInputText('');

    // Trigger bot reply simulation
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);

      let botReplyText = '';
      if (
        typedText.includes('cabai') || typedText.includes('rawit') ||
        typedText.includes('panen') || typedText.includes('harga')
      ) {
        botReplyText =
          'Harga Cabai Rawit Merah di Jawa Barat saat ini Rp56.150/kg (data Bank Indonesia). Agria menggabungkan tren harga ini dengan jumlah petani yang panen berdekatan di wilayah Anda untuk merekomendasikan waktu jual terbaik.';
      } else if (typedText.includes('bantuan') || typedText.includes('help') || typedText.includes('cara')) {
        botReplyText =
          'Ketik /start di bot kami, pilih peran Petani, lalu laporkan komoditas, wilayah, dan tanggal panen Anda.';
      } else {
        botReplyText =
          'Terima kasih, Pak! Untuk contoh nyata, pilih salah satu skenario di atas (Jual / Tunggu / Jadwal), atau ketik "panen cabai rawit".';
      }

      const botReply: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: 'bot',
        text: botReplyText,
        timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, botReply]);
    }, 1500);
  };

  return (
    <div className="w-full max-w-lg mx-auto">
      {/* Preset Selector Chips */}
      <div className="flex items-center justify-center gap-2 mb-4 overflow-x-auto pb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-on-surface-variant/75 mr-2">Pilih Skenario:</span>
        {SCENARIOS.map((sc) => {
          const isActive = activePreset === sc.id;
          return (
            <button
              key={sc.id}
              onClick={() => setActivePreset(sc.id)}
              className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all flex items-center gap-1.5 active:scale-95 cursor-pointer shadow-sm ${
                isActive
                  ? 'bg-primary text-white scale-105'
                  : 'bg-white border border-outline-variant/40 text-on-surface hover:bg-surface-container-low'
              }`}
            >
              <span>{sc.icon}</span>
              <span>{sc.label}</span>
            </button>
          );
        })}
      </div>

      {/* Mobile Device Container Mockup */}
      <div className="bg-black rounded-[2.5rem] p-3 shadow-2xl border-[6px] border-slate-800 relative overflow-hidden">
        {/* Device camera notch */}
        <div className="absolute top-3 left-1/2 -translate-x-1/2 w-32 h-4 bg-black rounded-b-2xl z-20" />

        {/* Telegram Frame */}
        <div className="bg-[#72b1e1] rounded-[2rem] h-[520px] overflow-hidden flex flex-col relative">
          
          {/* Telegram App Bar Header */}
          <div className="bg-white/95 backdrop-blur px-4 pt-5 pb-3 flex items-center justify-between border-b border-slate-200/50 z-10">
            <div className="flex items-center gap-2.5">
              <ArrowLeft className="w-5 h-5 text-sky-600 cursor-pointer hover:opacity-75" />
              <div className="w-10 h-10 flex items-center justify-center">
                <Logo size={36} />
              </div>
              <div>
                <div className="font-bold text-slate-800 text-sm leading-tight flex items-center gap-1">
                  Panen Pas Bot
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                </div>
                <div className="text-[10px] text-slate-500 font-medium">bot asisten cerdas</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-primary animate-pulse" />
              <MoreVertical className="w-5 h-5 text-slate-500 cursor-pointer" />
            </div>
          </div>

          {/* Chat Messages List Container */}
          <div className="flex-1 p-3 overflow-y-auto space-y-3 flex flex-col">
            
            {/* System Info Banner */}
            <div className="self-center bg-slate-900/15 backdrop-blur-sm text-white text-[10px] py-1 px-3 rounded-full font-medium shadow-sm">
              Hari Ini
            </div>

            {messages.map((msg) => {
              const isUser = msg.sender === 'user';
              return (
                <div
                  key={msg.id}
                  className={`flex flex-col max-w-[85%] ${isUser ? 'self-end items-end' : 'self-start items-start'}`}
                >
                  <div
                    className={`p-3 rounded-2xl shadow-sm text-sm ${
                      isUser
                        ? 'bg-[#effdde] text-slate-950 rounded-tr-none border-l-2 border-emerald-500/30'
                        : 'bg-white text-slate-900 rounded-tl-none border border-slate-100'
                    }`}
                  >
                    <p className="leading-relaxed whitespace-pre-line">{msg.text}</p>

                    {/* Render custom interactive SVG chart inside the chat bubble */}
                    {!isUser && msg.chartData && (
                      <div className="mt-3 pt-2 border-t border-slate-100 w-full">
                        <div className="text-[10px] font-bold text-emerald-700 mb-1.5 flex items-center gap-1">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                          Tren Harga 7 Hari — data BI (IDR/kg):
                        </div>
                        
                        {/* Custom Pure SVG Line Chart */}
                        <div className="relative h-24 bg-slate-50/50 rounded-lg p-1 border border-slate-100">
                          <svg className="w-full h-full" viewBox="0 0 200 80" preserveAspectRatio="none">
                            {/* Grid lines */}
                            <line x1="0" y1="20" x2="200" y2="20" stroke="#f1f5f9" strokeWidth="1" />
                            <line x1="0" y1="40" x2="200" y2="40" stroke="#f1f5f9" strokeWidth="1" />
                            <line x1="0" y1="60" x2="200" y2="60" stroke="#f1f5f9" strokeWidth="1" />

                            {/* Render Line Paths and Data Points */}
                            {(() => {
                              const points = msg.chartData;
                              const minVal = Math.min(...points.map((p) => p.price));
                              const maxVal = Math.max(...points.map((p) => p.price));
                              const range = maxVal - minVal || 1;
                              
                              const coords = points.map((p, i) => {
                                const x = (i / (points.length - 1)) * 180 + 10;
                                // invert y for SVG coordinates (80px height, leave 10px padding)
                                const y = 70 - ((p.price - minVal) / range) * 50;
                                return { x, y, price: p.price, day: p.day };
                              });

                              const pathD = coords.reduce(
                                (acc, c, i) => (i === 0 ? `M ${c.x} ${c.y}` : `${acc} L ${c.x} ${c.y}`),
                                ''
                              );

                              return (
                                <>
                                  {/* Area under line */}
                                  <path
                                    d={`${pathD} L ${coords[coords.length - 1].x} 75 L ${coords[0].x} 75 Z`}
                                    fill="url(#chartGrad)"
                                    opacity="0.2"
                                  />
                                  
                                  {/* Definition for Gradient */}
                                  <defs>
                                    <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                      <stop offset="0%" stopColor="#10b981" />
                                      <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                                    </linearGradient>
                                  </defs>

                                  {/* Main trend line */}
                                  <path
                                    d={pathD}
                                    fill="none"
                                    stroke="#10b981"
                                    strokeWidth="2.5"
                                    strokeLinecap="round"
                                  />

                                  {/* Points and labels */}
                                  {coords.map((c, idx) => (
                                    <g key={idx}>
                                      <circle
                                        cx={c.x}
                                        cy={c.y}
                                        r="3.5"
                                        fill="#004532"
                                        stroke="#ffffff"
                                        strokeWidth="1.5"
                                      />
                                      {/* Only show label for first, mid, and last to avoid clutter */}
                                      {(idx === 0 || idx === coords.length - 1 || idx === Math.floor(coords.length / 2)) && (
                                        <text
                                          x={c.x}
                                          y={c.y - 6}
                                          fontSize="6"
                                          fontWeight="bold"
                                          fill="#004532"
                                          textAnchor="middle"
                                        >
                                          Rp{Math.round(c.price / 1000)}k
                                        </text>
                                      )}
                                      <text
                                        x={c.x}
                                        y="78"
                                        fontSize="6"
                                        fill="#64748b"
                                        textAnchor="middle"
                                      >
                                        {c.day}
                                      </text>
                                    </g>
                                  ))}
                                </>
                              );
                            })()}
                          </svg>
                        </div>
                        <div className="text-[9px] text-slate-500 mt-1.5 text-center font-medium">
                          Harga aktual cabai rawit merah dari data Bank Indonesia.
                        </div>
                      </div>
                    )}
                  </div>
                  
                  {/* Message Timestamp */}
                  <span className={`text-[9px] text-white/90 mt-0.5 px-1 ${isUser ? 'mr-1' : 'ml-1'}`}>
                    {msg.timestamp} {isUser && '✓✓'}
                  </span>
                </div>
              );
            })}

            {/* Simulated typing indicator */}
            {isTyping && (
              <div className="self-start flex flex-col items-start max-w-[80%]">
                <div className="bg-white p-3 rounded-2xl rounded-tl-none shadow-sm flex items-center gap-1">
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
            
            <div ref={chatEndRef} />
          </div>

          {/* Telegram input bar */}
          <form
            onSubmit={handleSendMessage}
            className="bg-white p-2.5 flex items-center gap-2 border-t border-slate-150 z-10"
          >
            <Paperclip className="w-5 h-5 text-slate-400 cursor-pointer shrink-0 hover:text-slate-600" />
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ketik pesan..."
              className="flex-1 bg-slate-100 rounded-full px-4 py-1.5 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-primary border-none"
            />
            {inputText.trim() ? (
              <button
                type="submit"
                className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center shrink-0 hover:opacity-90 active:scale-95 transition-all cursor-pointer"
              >
                <Send className="w-4 h-4" />
              </button>
            ) : (
              <Mic className="w-5 h-5 text-slate-400 cursor-pointer shrink-0 hover:text-slate-600" />
            )}
          </form>

        </div>
      </div>

      <div className="mt-2 text-center text-[11px] text-on-surface-variant font-medium">
        💡 Cobalah mengetik sesuatu seperti <span className="font-bold text-primary">"panen cabai rawit"</span> atau <span className="font-bold text-primary">"harga cabai"</span> di atas!
      </div>
    </div>
  );
}
