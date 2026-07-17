import { CropData, ChatMessage } from './types';

export const CROP_PRESETS = [
  { id: 'cabai', name: 'Cabai Merah Keriting', basePrice: 40000, volatility: 0.15, icon: '🌶️', unit: 'kg' },
  { id: 'tomat', name: 'Tomat Beef', basePrice: 15000, volatility: 0.1, icon: '🍅', unit: 'kg' },
  { id: 'bawang', name: 'Bawang Merah Brebes', basePrice: 28000, volatility: 0.08, icon: '🧅', unit: 'kg' },
  { id: 'kentang', name: 'Kentang Granola', basePrice: 12000, volatility: 0.05, icon: '🥔', unit: 'kg' },
  { id: 'kubis', name: 'Kubis Bulat', basePrice: 6000, volatility: 0.12, icon: '🥬', unit: 'kg' },
];

export const INITIAL_CROPS: CropData[] = [
  {
    id: 'crop-1',
    name: 'Cabai Merah Keriting',
    harvestDate: '2026-07-20',
    expectedYield: 500,
    status: 'calculated',
    predictedPrice: 45000,
    recommendedMarket: 'Pasar Induk Kramat Jati',
    buyersMatchedCount: 3,
  },
  {
    id: 'crop-2',
    name: 'Tomat Beef',
    harvestDate: '2026-07-25',
    expectedYield: 1200,
    status: 'pending',
  },
];

export const PROBLEM_CARDS = [
  {
    id: 'prob-1',
    title: 'Inefisiensi Pasca Panen',
    description: 'Indonesia menempati peringkat tertinggi di dunia dalam kehilangan pangan per kapita karena masalah waktu.',
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
    title: 'Didukung AI Canggih',
    description: 'Sistem rekomendasi berbasis data sains yang presisi.',
    iconName: 'smart_toy',
    colorClass: 'text-teal-500 bg-teal-50',
  },
  {
    id: 'ben-4',
    title: 'Pembeli Terverifikasi',
    description: 'Langsung terhubung dengan jaringan B2B terpercaya.',
    iconName: 'handshake',
    colorClass: 'text-orange-600 bg-orange-50',
  },
];

export const IMPACT_METRICS = [
  { label: 'Limbah Pasca Panen Berkurang', value: '30%', style: 'primary' },
  { label: 'Potensi Pendapatan Meningkat', value: '25%', style: 'secondary' },
  { label: 'Pencocokan Pembeli Lebih Cepat', value: '2x', style: 'primary' },
  { label: 'Waktu Pasar Teroptimasi', value: '100%', style: 'secondary' },
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
    description: 'Kirim pesan sederhana seperti "Halo" atau laporkan rencana panen Anda.',
    emoji: '🤖',
  },
  {
    step: 'Langkah 4',
    title: 'Terima Rekomendasi',
    description: 'Dapatkan prakiraan harga panen optimal dan daftar pembeli dalam hitungan detik.',
    emoji: '🌾',
  },
];

export const CHAT_PRESETS: { [key: string]: ChatMessage[] } = {
  cabai: [
    { id: '1', sender: 'user', text: 'Halo Panen Pas Bot! Saya ingin lapor rencana panen cabai tanggal 20 Juli.', timestamp: '10:30 AM' },
    {
      id: '2',
      sender: 'bot',
      text: 'Halo Pak! Berdasarkan analisis kami, harga Cabai Merah Keriting di pasar terdekat diprediksi naik 15% pada tanggal 20 Juli karena pasokan sedang sedikit menurun.',
      timestamp: '10:32 AM',
    },
    {
      id: '3',
      sender: 'bot',
      text: 'Rekomendasi terbaik: Jual di Pasar Induk Kramat Jati seharga Rp45.000 / kg. Permintaan pasar sedang memuncak.',
      timestamp: '10:33 AM',
      chartData: [
        { day: '14 Jul', price: 39000 },
        { day: '15 Jul', price: 40000 },
        { day: '16 Jul', price: 41000 },
        { day: '17 Jul', price: 40500 },
        { day: '18 Jul', price: 42000 },
        { day: '19 Jul', price: 43500 },
        { day: '20 Jul', price: 45000 },
      ],
      isRecommendation: true,
    },
    { id: '4', sender: 'user', text: 'Hebat, tolong hubungkan saya dengan pembeli untuk tanggal itu.', timestamp: '10:35 AM' },
    {
      id: '5',
      sender: 'bot',
      text: 'Pilihan tepat! Jadwal panen Anda telah dicatat. Kami mencocokkan Anda dengan 3 pembeli supermarket terverifikasi yang setuju dengan harga kisaran Rp44.000 - Rp46.000/kg.',
      timestamp: '10:36 AM',
    },
  ],
  tomat: [
    { id: '1', sender: 'user', text: 'Saya panen Tomat Beef tanggal 25 Juli sekitar 1,2 ton.', timestamp: '02:15 PM' },
    {
      id: '2',
      sender: 'bot',
      text: 'Halo! Kami sedang menganalisis data pasar untuk Tomat Beef. Terdeteksi adanya cuaca buruk di sentra produksi Jawa Barat, yang berpotensi menghambat panen daerah lain.',
      timestamp: '02:16 PM',
    },
    {
      id: '3',
      sender: 'bot',
      text: 'Kami memprediksi harga akan naik stabil menjadi Rp17.500/kg. Jendela penjualan terbaik Anda adalah 24-26 Juli.',
      timestamp: '02:17 PM',
      chartData: [
        { day: '20 Jul', price: 14500 },
        { day: '21 Jul', price: 15000 },
        { day: '22 Jul', price: 15200 },
        { day: '23 Jul', price: 16000 },
        { day: '24 Jul', price: 17000 },
        { day: '25 Jul', price: 17500 },
        { day: '26 Jul', price: 17800 },
      ],
      isRecommendation: true,
    },
    {
      id: '4',
      sender: 'bot',
      text: 'Sudah kami sediakan pembeli grosir B2B (PT Fresh Indonesia & Supermarket Indomart) siap menjemput langsung dari ladang Anda.',
      timestamp: '02:18 PM',
    },
  ],
  bawang: [
    { id: '1', sender: 'user', text: 'Saya panen bawang merah akhir minggu ini.', timestamp: '08:45 AM' },
    {
      id: '2',
      sender: 'bot',
      text: 'Bawang Merah Brebes saat ini stabil di kisaran Rp28.000/kg. Namun, pasokan dari Nganjuk diperkirakan masuk minggu depan yang bisa menekan harga turun.',
      timestamp: '08:46 AM',
    },
    {
      id: '3',
      sender: 'bot',
      text: 'Disarankan untuk mempercepat penjualan Anda atau menyimpannya di gudang pengeringan (instore drying) selama 2 minggu agar dilepas saat harga kembali pulih ke Rp32.000/kg.',
      timestamp: '08:47 AM',
      chartData: [
        { day: 'Sen', price: 28500 },
        { day: 'Sel', price: 28000 },
        { day: 'Rab', price: 27800 },
        { day: 'Kam', price: 28200 },
        { day: 'Jum', price: 29000 },
        { day: 'Sab', price: 28000 },
        { day: 'Min', price: 27500 },
      ],
      isRecommendation: true,
    },
  ],
};
