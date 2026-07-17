import { ChatMessage } from './types';

export const PROBLEM_CARDS = [
  {
    id: 'prob-1',
    title: 'Inefisiensi Pasca Panen',
    description: 'Indonesia adalah salah satu penyumbang kehilangan pangan (food loss) per kapita tertinggi di dunia — sebagian besar karena masalah waktu, bukan produksi.',
    iconName: 'warning',
    colorClass: 'text-red-500 bg-red-50',
  },
  {
    id: 'prob-2',
    title: 'Fluktuasi Harga Ekstrem',
    description: 'Banyak petani kecil menderita akibat pasokan berlebih dan kejatuhan harga mendadak karena panen bersamaan.',
    iconName: 'trending_down',
    colorClass: 'text-amber-500 bg-amber-50',
  },
];

export const BENEFIT_CARDS = [
  {
    id: 'ben-1',
    title: 'Harga Jual Lebih Tinggi',
    description: 'Hindari menjual di bawah harga pasar saat stok melimpah.',
    iconName: 'trending_up',
    colorClass: 'text-orange-500 bg-orange-50',
  },
  {
    id: 'ben-2',
    title: 'Kurangi Limbah Pangan',
    description: 'Pastikan hasil panen terserap pasar dengan optimal.',
    iconName: 'delete_sweep',
    colorClass: 'text-emerald-500 bg-emerald-50',
  },
  {
    id: 'ben-3',
    title: 'Rekomendasi Berbasis Data',
    description: 'Menggabungkan tren harga Bank Indonesia dengan deteksi panen serentak di wilayah Anda.',
    iconName: 'smart_toy',
    colorClass: 'text-teal-500 bg-teal-50',
  },
  {
    id: 'ben-4',
    title: 'Pembeli Jangkar',
    description: 'Penawaran jual langsung diteruskan ke pembeli utama yang siap menyerap panen.',
    iconName: 'handshake',
    colorClass: 'text-orange-600 bg-orange-50',
  },
];

export const IMPACT_METRICS = [
  { label: 'Volatilitas harga cabai rawit (CV, data BI)', value: '32%', style: 'primary' },
  { label: 'Rentang harga dalam setahun', value: '3–4×', style: 'secondary' },
  { label: 'Potensi kerugian akibat salah waktu jual', value: '20–30%', style: 'primary' },
  { label: 'Harga bersumber dari data Bank Indonesia', value: '100%', style: 'secondary' },
];

export const STEP_ITEMS = [
  {
    step: 'Langkah 1',
    title: 'Pasang Telegram',
    description: 'Pasang aplikasi Telegram di ponsel Anda melalui App Store atau Google Play.',
    emoji: '📥',
  },
  {
    step: 'Langkah 2',
    title: 'Pindai Kode QR',
    description: 'Pindai kode QR Panen Pas atau klik tombol "Buka Bot Telegram" untuk memulai.',
    emoji: '📱',
  },
  {
    step: 'Langkah 3',
    title: 'Mulai Chat',
    description: 'Kirim /start, pilih peran Petani, lalu laporkan rencana panen Anda.',
    emoji: '🤖',
  },
  {
    step: 'Langkah 4',
    title: 'Terima Rekomendasi',
    description: 'Dapatkan analisis tren harga terkini dan rekomendasi kapan menjual dalam hitungan detik.',
    emoji: '🌾',
  },
];

// Three interactive scenarios — the real bot's three recommendation outcomes
// for Cabai Rawit Merah (the only supported crop). Prices reflect real Bank
// Indonesia data; the sell case is driven by a local harvest cluster.
export const CHAT_PRESETS: { [key: string]: ChatMessage[] } = {
  jual: [
    { id: '1', sender: 'user', text: 'Halo! Saya mau lapor panen cabai rawit merah di Garut, sekitar 2 hari lagi, 150 kg.', timestamp: '10:30' },
    { id: '2', sender: 'bot', text: 'Halo Pak 👋 Harga Cabai Rawit Merah di Jawa Barat saat ini Rp56.150/kg (data Bank Indonesia) — tergolong stabil.', timestamp: '10:31' },
    {
      id: '3',
      sender: 'bot',
      text: '🟢 REKOMENDASI: JUAL SEKARANG.\nMeski harga stabil, 5 petani di Garut panen dalam waktu berdekatan — pasokan lokal akan menekan harga. Jual sekarang selagi harga masih baik.',
      timestamp: '10:31',
      chartData: [
        { day: '10 Jul', price: 55650 },
        { day: '11 Jul', price: 53850 },
        { day: '12 Jul', price: 54250 },
        { day: '13 Jul', price: 54550 },
        { day: '14 Jul', price: 54900 },
        { day: '15 Jul', price: 55800 },
        { day: '16 Jul', price: 56150 },
      ],
      isRecommendation: true,
    },
    { id: '4', sender: 'user', text: 'Baik, tolong hubungkan ke pembeli.', timestamp: '10:32' },
    { id: '5', sender: 'bot', text: '📨 Penawaran Anda diteruskan ke Pembeli Utama. Anda akan diberi tahu saat mereka menerima, lengkap dengan kontaknya.', timestamp: '10:32' },
  ],
  tunggu: [
    { id: '1', sender: 'user', text: 'Panen cabai rawit di Cianjur, 3 hari lagi.', timestamp: '14:10' },
    { id: '2', sender: 'bot', text: 'Harga Cabai Rawit Merah sedang naik (+8% dalam 7 hari) dan tidak ada panen serentak di wilayah Anda.', timestamp: '14:11' },
    {
      id: '3',
      sender: 'bot',
      text: '🔵 REKOMENDASI: TUNGGU BEBERAPA HARI.\nMenunggu beberapa hari kemungkinan memberi harga lebih baik.',
      timestamp: '14:11',
      chartData: [
        { day: '10 Jul', price: 50000 },
        { day: '11 Jul', price: 50500 },
        { day: '12 Jul', price: 51500 },
        { day: '13 Jul', price: 52500 },
        { day: '14 Jul', price: 53500 },
        { day: '15 Jul', price: 54200 },
        { day: '16 Jul', price: 54500 },
      ],
      isRecommendation: true,
    },
  ],
  jadwal: [
    { id: '1', sender: 'user', text: 'Cabai rawit di Cianjur, 2 hari lagi, 80 kg.', timestamp: '08:45' },
    { id: '2', sender: 'bot', text: 'Harga stabil dan tidak ada tekanan pasokan lokal di wilayah Anda saat ini.', timestamp: '08:46' },
    {
      id: '3',
      sender: 'bot',
      text: '🟡 REKOMENDASI: JUAL SESUAI JADWAL BIASA.\nTidak ada tekanan pasar — jual sesuai rencana Anda.',
      timestamp: '08:46',
      chartData: [
        { day: '10 Jul', price: 55900 },
        { day: '11 Jul', price: 56100 },
        { day: '12 Jul', price: 55800 },
        { day: '13 Jul', price: 56000 },
        { day: '14 Jul', price: 56100 },
        { day: '15 Jul', price: 55950 },
        { day: '16 Jul', price: 56150 },
      ],
      isRecommendation: true,
    },
  ],
};
