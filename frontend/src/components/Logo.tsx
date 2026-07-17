import React from 'react';

interface LogoProps {
  className?: string;
  size?: number; // width and height in px
}

export default function Logo({ className = '', size = 40 }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 512 512"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* 
        Background is transparent.
        Color palette exactly matching the uploaded image:
        - Outlines / Borders: #2D3A4A (Dark navy/slate)
        - 3D Extrusion Side Bezel: #5E7388 (Slate gray-blue)
        - Screen surface: #FFFFFF (White)
        - Sprout Outline / Stem / Veins: #4E7D0A (Deep olive green)
        - Sprout Leaf Fill: #A0DF19 (Vibrant fresh leaf green)
      */}
      
      {/* 1. SMARTPHONE SHADOW / 3D EXTRUSION BACKPLATE */}
      <path
        d="M 85 317 
           L 85 335 
           C 80 341, 90 351, 100 357 
           L 185 406 
           C 196 412, 204 412, 215 406 
           L 435 279 
           C 440 276, 445 270, 445 261 
           L 445 243 
           C 445 252, 440 258, 435 261 
           L 215 388 
           C 204 394, 196 394, 185 388 
           L 100 339 
           C 90 333, 85 325, 85 317 Z"
        fill="#5E7388"
        stroke="#2D3A4A"
        strokeWidth="14"
        strokeLinejoin="round"
        strokeLinecap="round"
      />

      {/* 2. SMARTPHONE MAIN BODY TOP FACE */}
      <path
        d="M 90 304 
           L 310 178 
           C 316 174, 324 174, 330 178 
           L 430 235 
           C 436 239, 436 247, 430 251 
           L 210 377 
           C 204 381, 196 381, 190 377 
           L 90 320 
           C 84 316, 84 308, 90 304 Z"
        fill="#2D3A4A"
        stroke="#2D3A4A"
        strokeWidth="14"
        strokeLinejoin="round"
        strokeLinecap="round"
      />

      {/* 3. WHITE SCREEN SURFACE (INSET) */}
      <path
        d="M 112 308 
           L 308 195 
           C 314 191, 320 191, 326 195 
           L 418 248 
           C 424 252, 424 258, 418 262 
           L 222 375 
           C 216 379, 210 379, 204 375 
           L 112 322 
           C 106 318, 106 312, 112 308 Z"
        fill="#FFFFFF"
        stroke="#2D3A4A"
        strokeWidth="14"
        strokeLinejoin="round"
        strokeLinecap="round"
      />

      {/* 4. SMARTPHONE NOTCH */}
      <path
        d="M 370 216 L 390 227"
        stroke="#2D3A4A"
        strokeWidth="14"
        strokeLinecap="round"
      />

      {/* 5. SMARTPHONE DECORATIVE CHIN LINE */}
      <path
        d="M 142 335 L 192 364"
        stroke="#2D3A4A"
        strokeWidth="10"
        strokeLinecap="round"
      />

      {/* 6. SPROUT MAIN STEM */}
      <path
        d="M 260 290 L 260 185"
        stroke="#4E7D0A"
        strokeWidth="16"
        strokeLinecap="round"
      />

      {/* 7. LEFT LEAF (OUTLINE & FILL) */}
      <path
        d="M 260 195 
           C 195 190, 135 150, 150 115 
           C 165 80, 235 115, 260 195 Z"
        fill="#A0DF19"
        stroke="#4E7D0A"
        strokeWidth="14"
        strokeLinejoin="round"
        strokeLinecap="round"
      />

      {/* 8. LEFT LEAF MIDDLE VEIN */}
      <path
        d="M 260 195 C 220 160, 185 140, 150 115"
        stroke="#4E7D0A"
        strokeWidth="10"
        strokeLinecap="round"
        fill="none"
      />

      {/* 9. RIGHT LEAF (OUTLINE & FILL) */}
      <path
        d="M 260 185 
           C 275 110, 335 55, 365 65 
           C 395 75, 320 165, 260 185 Z"
        fill="#A0DF19"
        stroke="#4E7D0A"
        strokeWidth="14"
        strokeLinejoin="round"
        strokeLinecap="round"
      />

      {/* 10. RIGHT LEAF MIDDLE VEIN */}
      <path
        d="M 260 185 C 295 145, 330 110, 365 65"
        stroke="#4E7D0A"
        strokeWidth="10"
        strokeLinecap="round"
        fill="none"
      />
    </svg>
  );
}
