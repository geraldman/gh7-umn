export type TabType = 'layanan' | 'hubungkan' | 'cara_kerja';

export interface CropData {
  id: string;
  name: string;
  harvestDate: string;
  expectedYield: number; // in kg
  status: 'pending' | 'calculated' | 'sold';
  predictedPrice?: number; // per kg
  recommendedMarket?: string;
  buyersMatchedCount?: number;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  chartData?: { day: string; price: number }[];
  isRecommendation?: boolean;
}

export interface DecisionStep {
  id: string;
  label: string;
  icon: string;
  description: string;
}
