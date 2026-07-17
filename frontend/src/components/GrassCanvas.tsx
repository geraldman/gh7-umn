import { useEffect, useRef } from 'react';

export default function GrassCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.offsetWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.offsetHeight || 300);

    const mouse = { x: -1000, y: -1000 };

    class GrassBlade {
      x: number;
      height: number;
      angle: number;
      maxBend: number;
      speed: number;
      offset: number;
      thickness: number;
      color: string;

      constructor(x: number) {
        this.x = x;
        this.height = Math.random() * 50 + 70;
        this.angle = 0;
        this.maxBend = Math.random() * 25 + 5;
        this.speed = Math.random() * 0.015 + 0.005;
        this.offset = Math.random() * Math.PI * 2;
        this.thickness = Math.random() * 2.5 + 1;
        this.color = this.getRandomGreen();
      }

      getRandomGreen() {
        const greens = ['#1b6b51', '#004532', '#065f46', '#8bd6b6', '#a6f2d1'];
        return greens[Math.floor(Math.random() * greens.length)];
      }

      update() {
        // Ambient wind sway
        this.angle = Math.sin(Date.now() * this.speed + this.offset) * (this.maxBend / 110);

        // Mouse interaction
        const dx = mouse.x - this.x;
        const dy = mouse.y - (height - this.height);
        const dist = Math.sqrt(dx * dx + dy * dy);
        const influenceRange = 140;

        if (dist < influenceRange) {
          const force = (1 - dist / influenceRange) * 1.6;
          const dir = dx > 0 ? -1 : 1;
          this.angle += dir * force;
        }
      }

      draw() {
        if (!ctx) return;
        ctx.save();
        ctx.translate(this.x, height);
        ctx.rotate(this.angle);

        ctx.beginPath();
        ctx.moveTo(0, 0);
        // Quadratic curve for smoother grass look
        ctx.quadraticCurveTo(0, -this.height / 2, Math.sin(this.angle) * 10, -this.height);

        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.thickness;
        ctx.lineCap = 'round';
        ctx.globalAlpha = 0.25; // Subtle grounding effect
        ctx.stroke();

        ctx.restore();
      }
    }

    let blades: GrassBlade[] = [];

    const init = () => {
      if (!canvas.parentElement) return;
      width = canvas.width = canvas.parentElement.offsetWidth;
      height = canvas.height = canvas.parentElement.offsetHeight;
      blades = [];
      const density = Math.floor(width / 4);
      for (let i = 0; i < density; i++) {
        blades.push(new GrassBlade(Math.random() * width));
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw subtle gradient at bottom for grounding
      const grad = ctx.createLinearGradient(0, height - 120, 0, height);
      grad.addColorStop(0, 'transparent');
      grad.addColorStop(1, 'rgba(27, 107, 81, 0.08)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, height - 120, width, 120);

      blades.forEach((blade) => {
        blade.update();
        blade.draw();
      });
      animationFrameId = requestAnimationFrame(animate);
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    };

    const handleMouseLeave = () => {
      mouse.x = -1000;
      mouse.y = -1000;
    };

    const handleResize = () => {
      init();
    };

    // Attach to parent element to cover the hero background smoothly
    const parent = canvas.parentElement;
    if (parent) {
      parent.addEventListener('mousemove', handleMouseMove);
      parent.addEventListener('mouseleave', handleMouseLeave);
    }

    window.addEventListener('resize', handleResize);

    init();
    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      if (parent) {
        parent.removeEventListener('mousemove', handleMouseMove);
        parent.removeEventListener('mouseleave', handleMouseLeave);
      }
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return <canvas ref={canvasRef} id="grass-canvas" className="absolute bottom-0 left-0 w-full h-full pointer-events-none z-0" />;
}
