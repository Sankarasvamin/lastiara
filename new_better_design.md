@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* 复旦/CDO 核心色系 */
  --cdo-blue: #004598;       /* 提取自官网导航栏的复旦蓝 */
  --cdo-blue-light: #E6F0FA; /* 极浅的蓝，用于背景或激活态 */
  
  /* 浅色主题基调 */
  --bg-base: #F8FAFC;        /* 干净的灰蓝色底色 */
  --glass-bg: rgba(255, 255, 255, 0.85);
  --glass-border: rgba(0, 0, 0, 0.06);
  
  /* 文字颜色 */
  --text-main: #1E293B;      /* 深石板灰，比纯黑更护眼 */
  --text-dim: #64748B;       /* 辅助文本颜色 */
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background-color: var(--bg-base);
  /* 极简的背景修饰：左上角有一点点非常柔和的蓝色光晕 */
  background-image: radial-gradient(circle at top left, var(--cdo-blue-light) 0%, transparent 40%);
  color: var(--text-main);
  height: 100vh;
  overflow: hidden;
}

/* 浅色版玻璃组件 */
.glass-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
}

.glass-card {
  background: #ffffff;
  border: 1px solid var(--glass-border);
  border-radius: 16px; /* 相比黑金版，边角稍微硬朗一点，更具学术严谨感 */
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03); /* 阴影极弱，只提供层次感 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 69, 152, 0.08); /* 悬浮时带一点点复旦蓝的阴影 */
}

/* 隐藏滚动条 */
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }