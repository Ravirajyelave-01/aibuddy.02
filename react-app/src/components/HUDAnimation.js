import React, { useEffect, useRef } from 'react';
import './HUDAnimation.css';

function HUDAnimation({ listening }) {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const angleRef = useRef(0);
  const pulseRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;

    const animate = () => {
      // Clear canvas
      ctx.fillStyle = 'rgba(10, 14, 39, 0.1)';
      ctx.fillRect(0, 0, width, height);

      // Update angles
      angleRef.current += 2;
      pulseRef.current += 0.1;
      if (angleRef.current >= 360) angleRef.current = 0;
      if (pulseRef.current >= 2 * Math.PI) pulseRef.current = 0;

      // Draw background gradient circles
      ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
      ctx.lineWidth = 1;

      // Draw outer rings
      for (let i = 1; i <= 3; i++) {
        ctx.beginPath();
        ctx.arc(centerX, centerY, 50 + i * 30, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Draw rotating lines
      ctx.strokeStyle = listening ? 'rgba(255, 100, 100, 0.6)' : 'rgba(0, 255, 255, 0.6)';
      ctx.lineWidth = 2;

      for (let i = 0; i < 4; i++) {
        const angle = (angleRef.current + i * 90) * Math.PI / 180;
        const x = centerX + Math.cos(angle) * 80;
        const y = centerY + Math.sin(angle) * 80;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.stroke();
      }

      // Draw arc segments
      ctx.strokeStyle = listening ? 'rgba(255, 100, 100, 0.4)' : 'rgba(0, 255, 255, 0.4)';
      ctx.lineWidth = 1;

      for (let i = 0; i < 8; i++) {
        const startAngle = ((angleRef.current + i * 45) % 360) * Math.PI / 180;
        const endAngle = startAngle + (30 * Math.PI / 180);
        ctx.beginPath();
        ctx.arc(centerX, centerY, 85, startAngle, endAngle);
        ctx.stroke();
      }

      // Draw center dot with pulse
      const pulseSize = 5 + 3 * Math.sin(pulseRef.current);
      ctx.fillStyle = listening ? 'rgba(255, 100, 100, 0.8)' : 'rgba(0, 255, 255, 0.8)';
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize, 0, Math.PI * 2);
      ctx.fill();

      // Draw outer glow for center dot
      ctx.strokeStyle = listening ? 'rgba(255, 100, 100, 0.3)' : 'rgba(0, 255, 255, 0.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize + 5, 0, Math.PI * 2);
      ctx.stroke();

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [listening]);

  return (
    <canvas
      ref={canvasRef}
      className="hud-animation"
      width={400}
      height={400}
    />
  );
}

export default HUDAnimation;
