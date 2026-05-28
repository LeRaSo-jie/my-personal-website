/** @type {import('tailwindcss').Config} */
export default {
  // 启用 class 策略的暗黑模式
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // 赛博朋克色系
      colors: {
        primary: '#0ea5e9',
        neon: {
          DEFAULT: '#00f3ff',
          cyan: '#00f3ff',
          blue: '#0ea5e9',
          purple: '#b670ff',
          pink: '#ff2d75',
          green: '#39ff14',
          yellow: '#ffe600'
        },
        cyber: {
          bg: '#0a0e1a',
          card: '#0d1321',
          border: '#1a2332',
          surface: '#111827'
        }
      },
      // 自定义字体
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      // 自定义动画
      animation: {
        'gradient': 'gradient 8s ease infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite',
        'pulse-neon': 'pulse-neon 2s ease-in-out infinite',
        'scan': 'scan 8s linear infinite',
        'flicker': 'flicker 3s linear infinite',
        'typing': 'typing 3.5s steps(40, end), blink-caret .75s step-end infinite',
        'slide-up': 'slide-up 0.6s ease-out',
        'fade-in': 'fade-in 0.8s ease-out',
        'glitch': 'glitch 2s infinite linear alternate-reverse'
      },
      keyframes: {
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        glow: {
          '0%, 100%': { opacity: 0.5 },
          '50%': { opacity: 1 }
        },
        'pulse-neon': {
          '0%, 100%': { 
            boxShadow: '0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff',
            opacity: 1
          },
          '50%': { 
            boxShadow: '0 0 2px #00f3ff, 0 0 5px #00f3ff, 0 0 10px #00f3ff',
            opacity: 0.8
          }
        },
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' }
        },
        flicker: {
          '0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100%': { opacity: 1 },
          '20%, 21.999%, 63%, 63.999%, 65%, 69.999%': { opacity: 0.33 }
        },
        typing: {
          'from': { width: 0 },
          'to': { width: '100%' }
        },
        'blink-caret': {
          'from, to': { borderColor: 'transparent' },
          '50%': { borderColor: '#00f3ff' }
        },
        'slide-up': {
          'from': { transform: 'translateY(30px)', opacity: 0 },
          'to': { transform: 'translateY(0)', opacity: 1 }
        },
        'fade-in': {
          'from': { opacity: 0 },
          'to': { opacity: 1 }
        },
        glitch: {
          '0%': { transform: 'translate(0)' },
          '20%': { transform: 'translate(-2px, 2px)' },
          '40%': { transform: 'translate(-2px, -2px)' },
          '60%': { transform: 'translate(2px, 2px)' },
          '80%': { transform: 'translate(2px, -2px)' },
          '100%': { transform: 'translate(0)' }
        }
      },
      // 背景图
      backgroundImage: {
        'grid-pattern': 'linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px)',
        'cyber-gradient': 'linear-gradient(135deg, #0a0e1a 0%, #0d1321 50%, #111827 100%)'
      },
      backgroundSize: {
        'grid': '40px 40px'
      }
    }
  },
  plugins: [],
}
