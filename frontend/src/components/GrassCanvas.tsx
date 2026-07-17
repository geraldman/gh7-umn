import { useEffect, useRef } from 'react';

export default function GrassCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.offsetWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.offsetHeight || 400);

    const mouse = { x: -1000, y: -1000 };
    let isMouseDown = false;
    let globalLushness = 0; // Global transition state (0 = arid, 1 = lush)

    // Color structures for smooth transition
    const COLOR_PALETTE = {
      back: {
        dry: {
          base: { r: 120, g: 90, b: 65 },  // Warm dry soil/wood
          tip: { r: 195, g: 165, b: 110 }  // Dry straw gold
        },
        lush: {
          base: { r: 6, g: 78, b: 59 },   // Deep emerald forest
          tip: { r: 16, g: 185, b: 129 }  // Vibrant emerald
        }
      },
      mid: {
        dry: {
          base: { r: 105, g: 78, b: 52 },  // Clay brown
          tip: { r: 210, g: 180, b: 120 }  // Pale golden straw
        },
        lush: {
          base: { r: 20, g: 83, b: 45 },  // Rich deep grass
          tip: { r: 163, g: 230, b: 53 }  // Chartreuse green
        }
      },
      fore: {
        dry: {
          base: { r: 90, g: 65, b: 40 },   // Deep grounding earth
          tip: { r: 220, g: 195, b: 130 }  // Golden wheat
        },
        lush: {
          base: { r: 5, g: 46, b: 22 },   // Ground shadow green
          tip: { r: 190, g: 242, b: 100 }  // Bright sunlit lime
        }
      }
    };

    const lerpColor = (c1: { r: number; g: number; b: number }, c2: { r: number; g: number; b: number }, f: number) => {
      const r = Math.round(c1.r + (c2.r - c1.r) * f);
      const g = Math.round(c1.g + (c2.g - c1.g) * f);
      const b = Math.round(c1.b + (c2.b - c1.b) * f);
      return `rgb(${r}, ${g}, ${b})`;
    };

    // Optimized Bokeh Particles
    class BokehParticle {
      x: number;
      y: number;
      size: number;
      speedY: number;
      opacity: number;
      offset: number;

      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * (height * 0.7);
        this.size = Math.random() * 40 + 25;
        this.speedY = Math.random() * 0.1 + 0.03;
        this.opacity = Math.random() * 0.08 + 0.02;
        this.offset = Math.random() * Math.PI * 2;
      }

      update() {
        this.y -= this.speedY;
        this.x += Math.sin(Date.now() * 0.0008 + this.offset) * 0.06;
        
        if (this.y < -this.size) {
          this.y = height * 0.7 + this.size;
          this.x = Math.random() * width;
        }
      }

      draw(c: CanvasRenderingContext2D, f: number) {
        c.save();
        c.globalAlpha = this.opacity;
        
        // Golden-amber bokeh when dry, vibrant-lime bokeh when lush
        const dryColor = '217, 160, 91';  // Amber
        const lushColor = '163, 230, 53';  // Lime
        const color = f > 0.5 ? lushColor : dryColor;

        const grad = c.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size);
        grad.addColorStop(0, `rgba(${color}, 0.5)`);
        grad.addColorStop(0.8, 'rgba(0, 0, 0, 0)');
        c.fillStyle = grad;
        c.beginPath();
        c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        c.fill();
        c.restore();
      }
    }

    class GrassBlade {
      x: number;
      baseHeight: number;
      thickness: number;
      angle: number;
      velocity: number;
      maxBend: number;
      speed: number;
      offset: number;
      bendDirection: number;
      layer: 'back' | 'mid' | 'fore';
      lushFactor: number;

      constructor(x: number, layer: 'back' | 'mid' | 'fore') {
        this.x = x;
        this.layer = layer;
        this.angle = 0;
        this.velocity = 0;
        this.offset = Math.random() * Math.PI * 2;
        this.bendDirection = Math.random() * 1.6 - 0.8; // soft lean
        this.lushFactor = 0; // Starts dry/arid

        if (layer === 'back') {
          this.baseHeight = Math.random() * 50 + 70;
          this.thickness = Math.random() * 5 + 3;
          this.maxBend = Math.random() * 12 + 4;
          this.speed = Math.random() * 0.006 + 0.002;
        } else if (layer === 'mid') {
          this.baseHeight = Math.random() * 80 + 110;
          this.thickness = Math.random() * 10 + 6;
          this.maxBend = Math.random() * 20 + 8;
          this.speed = Math.random() * 0.01 + 0.004;
        } else {
          this.baseHeight = Math.random() * 100 + 180;
          this.thickness = Math.random() * 14 + 10;
          this.maxBend = Math.random() * 30 + 10;
          this.speed = Math.random() * 0.012 + 0.005;
        }
      }

      update(btnCenterX: number, targetGlobalLushness: number) {
        // Distance to the "Hubungkan Bot" button x-coordinate
        const dxToBtn = Math.abs(this.x - btnCenterX);
        
        // Blades closer to the button grow lush first! Create a beautiful horizontal greening wave.
        const distanceRatio = dxToBtn / width; // 0.0 at button, up to ~1.0 at far edges
        
        // Define blade target lushness
        const targetIndividualLushness = Math.max(
          0,
          Math.min(1, (targetGlobalLushness * 1.5) - (distanceRatio * 0.5))
        );

        // Interpolate smoothly
        this.lushFactor += (targetIndividualLushness - this.lushFactor) * 0.08;

        // Interactive mouse push mechanics
        let pushForce = 0;
        if (mouse.x !== -1000 && mouse.y !== -1000) {
          const dx = mouse.x - this.x;
          // Scale active height of the blade tip
          const currentHeight = this.baseHeight * (0.6 + 0.4 * this.lushFactor);
          const dy = mouse.y - (height - currentHeight * 0.85);
          const dist = Math.sqrt(dx * dx + dy * dy);

          let influenceRange = this.layer === 'fore' ? 180 : this.layer === 'mid' ? 120 : 60;
          let forceMultiplier = this.layer === 'fore' ? 1.2 : 0.7;

          if (isMouseDown) {
            influenceRange *= 1.8;
            forceMultiplier *= 2.6;
          }

          if (dist < influenceRange) {
            const factor = 1 - dist / influenceRange;
            const dir = dx > 0 ? 1 : -1;
            pushForce = dir * factor * forceMultiplier;
          }
        }

        // Stiffer/brittler wind sway when dry, elegant flexing when lush
        const currentMaxBend = this.maxBend * (0.45 + 0.55 * this.lushFactor);
        const time = Date.now() * this.speed + this.offset;
        const windSway = Math.sin(time) * (currentMaxBend / 180) + Math.sin(time * 2) * (currentMaxBend / 400);

        const targetAngle = (this.bendDirection * (0.15 - 0.05 * this.lushFactor)) + windSway + pushForce;
        const springForce = -0.08 * (this.angle - targetAngle);
        
        this.velocity += springForce;
        this.velocity *= 0.84; // responsive damping
        this.angle += this.velocity;
      }

      draw(c: CanvasRenderingContext2D) {
        c.save();
        c.translate(this.x, height);

        // Dynamically compute size based on lushness (sprouts up)
        const currentHeight = this.baseHeight * (0.55 + 0.45 * this.lushFactor);
        const currentThickness = this.thickness * (0.8 + 0.2 * this.lushFactor);

        // Draw dry to lush gradient for this individual blade
        const grad = c.createLinearGradient(0, 0, 0, -currentHeight);
        
        const palette = COLOR_PALETTE[this.layer];
        const baseColor = lerpColor(palette.dry.base, palette.lush.base, this.lushFactor);
        const tipColor = lerpColor(palette.dry.tip, palette.lush.tip, this.lushFactor);

        grad.addColorStop(0, baseColor);
        grad.addColorStop(1, tipColor);
        c.fillStyle = grad;

        const tipX = Math.sin(this.angle) * (currentHeight * 0.3) + (this.bendDirection * currentHeight * 0.08);
        const tipY = -currentHeight * Math.cos(this.angle * 0.12);

        const leftControlX = -currentThickness / 2 + tipX * 0.4;
        const leftControlY = tipY * 0.45;
        const rightControlX = currentThickness / 2 + tipX * 0.4;
        const rightControlY = tipY * 0.45;

        c.beginPath();
        c.moveTo(-currentThickness / 2, 5);
        c.quadraticCurveTo(leftControlX, leftControlY, tipX, tipY);
        c.quadraticCurveTo(rightControlX, rightControlY, currentThickness / 2, 5);
        c.closePath();
        c.fill();

        // Subtle center vein
        c.beginPath();
        c.moveTo(0, 0);
        c.quadraticCurveTo(tipX * 0.45, tipY * 0.45, tipX, tipY);
        
        // Golden/brown vein when dry, white/lime vein when lush
        const veinDry = 'rgba(139, 115, 85, 0.12)';
        const veinLush = 'rgba(255, 255, 255, 0.15)';
        c.strokeStyle = this.lushFactor > 0.5 ? veinLush : veinDry;
        c.lineWidth = Math.max(1, currentThickness * 0.1);
        c.stroke();

        c.restore();
      }
    }

    let bokehs: BokehParticle[] = [];
    let backBlades: GrassBlade[] = [];
    let midBlades: GrassBlade[] = [];
    let foreBlades: GrassBlade[] = [];

    const init = () => {
      if (!canvas.parentElement) return;
      width = canvas.width = canvas.parentElement.offsetWidth;
      height = canvas.height = canvas.parentElement.offsetHeight;

      bokehs = [];
      backBlades = [];
      midBlades = [];
      foreBlades = [];

      const bokehCount = Math.min(12, Math.floor(width / 100));
      for (let i = 0; i < bokehCount; i++) {
        bokehs.push(new BokehParticle());
      }

      const backCount = Math.floor(width / 15);
      for (let i = 0; i < backCount; i++) {
        backBlades.push(new GrassBlade(Math.random() * width, 'back'));
      }

      const midCount = Math.floor(width / 22);
      for (let i = 0; i < midCount; i++) {
        midBlades.push(new GrassBlade(Math.random() * width, 'mid'));
      }

      const foreCount = Math.floor(width / 52);
      for (let i = 0; i < foreCount; i++) {
        foreBlades.push(new GrassBlade(Math.random() * width, 'fore'));
      }

      backBlades.sort((a, b) => a.x - b.x);
      midBlades.sort((a, b) => a.x - b.x);
      foreBlades.sort((a, b) => a.x - b.x);
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      // Locate the "Hubungkan Bot" button coordinates dynamically relative to the canvas
      const btn = document.getElementById('connect-bot-btn');
      let btnCenterX = width * 0.18; // fallback coordinates
      let btnCenterY = height - 80;

      if (btn) {
        const btnRect = btn.getBoundingClientRect();
        const canvasRect = canvas.getBoundingClientRect();
        btnCenterX = btnRect.left - canvasRect.left + btnRect.width / 2;
        btnCenterY = btnRect.top - canvasRect.top + btnRect.height / 2;
      }

      // Calculate target global lushness based on proximity of the mouse to the button
      let targetLushness = 0;
      if (mouse.x !== -1000 && mouse.y !== -1000) {
        const dx = mouse.x - btnCenterX;
        const dy = mouse.y - btnCenterY;
        const distToButton = Math.sqrt(dx * dx + dy * dy);

        // Active growth range starts at 580px
        const maxDist = 580;
        if (distToButton < maxDist) {
          const ratio = 1 - (distToButton / maxDist);
          // Exponential ease for high responsiveness
          targetLushness = Math.min(1, ratio * 1.6);
        }
      }

      // Smoothly transition global lushness
      globalLushness += (targetLushness - globalLushness) * 0.08;

      // 1. Draw beautiful warm glowing sunny backdrop (dry dusty sun vs fertile golden sun)
      const radialSun = ctx.createRadialGradient(width * 0.3, height * 0.1, 50, width * 0.3, height * 0.1, width * 0.8);
      
      const sunCenterDry = 'rgba(230, 210, 180, 0.35)'; // Dusty sunset
      const sunCenterLush = 'rgba(254, 252, 232, 0.45)'; // Vivid warm sun
      const sunCenter = globalLushness > 0.5 ? sunCenterLush : sunCenterDry;

      radialSun.addColorStop(0, sunCenter);
      radialSun.addColorStop(0.5, 'rgba(243, 246, 236, 0.15)');
      radialSun.addColorStop(1, 'rgba(230, 242, 206, 0)');
      ctx.fillStyle = radialSun;
      ctx.fillRect(0, 0, width, height);

      // 2. Draw Bokeh sun flares
      bokehs.forEach((b) => {
        b.update();
        b.draw(ctx, globalLushness);
      });

      // 3. Update and draw background grass
      backBlades.forEach((b) => {
        b.update(btnCenterX, globalLushness);
        b.draw(ctx);
      });

      // 4. Update and draw midground grass
      midBlades.forEach((b) => {
        b.update(btnCenterX, globalLushness);
        b.draw(ctx);
      });

      // 5. Update and draw foreground grass
      foreBlades.forEach((b) => {
        b.update(btnCenterX, globalLushness);
        b.draw(ctx);
      });

      // 6. Ground shadow at base (dry brown shadow vs fertile forest-green shadow)
      const bottomGrad = ctx.createLinearGradient(0, height - 30, 0, height);
      const shadowDry = 'rgba(80, 60, 40, 0.08)';
      const shadowLush = 'rgba(5, 46, 22, 0.12)';
      const shadowColor = globalLushness > 0.5 ? shadowLush : shadowDry;

      bottomGrad.addColorStop(0, 'rgba(0, 0, 0, 0)');
      bottomGrad.addColorStop(1, shadowColor);
      ctx.fillStyle = bottomGrad;
      ctx.fillRect(0, height - 30, width, 30);

      animationFrameId = requestAnimationFrame(animate);
    };

    // Event handlers for full interactive tracking
    const updateMousePos = (clientX: number, clientY: number) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = clientX - rect.left;
      mouse.y = clientY - rect.top;
    };

    const handleMouseMove = (e: MouseEvent) => {
      updateMousePos(e.clientX, e.clientY);
    };

    const handleMouseDown = (e: MouseEvent) => {
      isMouseDown = true;
      updateMousePos(e.clientX, e.clientY);
    };

    const handleMouseUp = () => {
      isMouseDown = false;
    };

    const handleMouseLeave = () => {
      mouse.x = -1000;
      mouse.y = -1000;
      isMouseDown = false;
    };

    // Touch event support for tablets and mobile
    const handleTouchStart = (e: TouchEvent) => {
      isMouseDown = true;
      if (e.touches.length > 0) {
        updateMousePos(e.touches[0].clientX, e.touches[0].clientY);
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (e.touches.length > 0) {
        updateMousePos(e.touches[0].clientX, e.touches[0].clientY);
      }
    };

    const handleTouchEnd = () => {
      mouse.x = -1000;
      mouse.y = -1000;
      isMouseDown = false;
    };

    const handleResize = () => {
      init();
    };

    // Attach listeners on parent section to capture all inputs smoothly
    const parent = canvas.parentElement;
    if (parent) {
      parent.addEventListener('mousemove', handleMouseMove);
      parent.addEventListener('mousedown', handleMouseDown);
      parent.addEventListener('mouseup', handleMouseUp);
      parent.addEventListener('mouseleave', handleMouseLeave);
      
      // Touch Support
      parent.addEventListener('touchstart', handleTouchStart, { passive: true });
      parent.addEventListener('touchmove', handleTouchMove, { passive: true });
      parent.addEventListener('touchend', handleTouchEnd);
    }

    window.addEventListener('resize', handleResize);

    init();
    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      if (parent) {
        parent.removeEventListener('mousemove', handleMouseMove);
        parent.removeEventListener('mousedown', handleMouseDown);
        parent.removeEventListener('mouseup', handleMouseUp);
        parent.removeEventListener('mouseleave', handleMouseLeave);
        
        parent.removeEventListener('touchstart', handleTouchStart);
        parent.removeEventListener('touchmove', handleTouchMove);
        parent.removeEventListener('touchend', handleTouchEnd);
      }
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      id="grass-canvas"
      className="absolute bottom-0 left-0 w-full h-full pointer-events-none z-0"
    />
  );
}
