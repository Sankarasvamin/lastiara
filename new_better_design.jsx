import React, { useState } from 'react';

const DigitalAnatomyDashboard = () => {
  const [messages, setMessages] = useState([
    {
      role: 'agent',
      content: `📊 查询结果\n\n统计维度：数据库表数量\n总数：13 张\n\n构成明细：\n- 字典表：4张 (majors, skills...)\n- 实体表：7张 (students, companies...)`
    }
  ]);
  const [input, setInput] = useState('');

  return (
    <div className="flex h-screen bg-[#09090b] text-gray-200 font-sans antialiased overflow-hidden selection:bg-yellow-500/30">
      
      {/* 1. 侧边栏 (Sidebar) - 赋予应用结构感 */}
      <aside className="w-64 border-r border-zinc-800/60 bg-[#0c0c0e] flex flex-col hidden md:flex">
        <div className="p-6 border-b border-zinc-800/60">
          <h1 className="text-xl font-bold tracking-wider text-yellow-500">LASTIARA</h1>
          <p className="text-xs text-zinc-500 tracking-widest mt-1 uppercase">Digital Anatomy</p>
        </div>
        
        <div className="flex-1 p-4 space-y-6 overflow-y-auto">
          <div>
            <p className="text-xs font-semibold text-zinc-600 uppercase tracking-wider mb-3">Database</p>
            <ul className="space-y-2 text-sm text-zinc-400">
              <li className="flex items-center gap-2 hover:text-white cursor-pointer px-2 py-1.5 rounded bg-zinc-800/30 text-yellow-500/90 border border-zinc-800">
                <span className="w-2 h-2 rounded-full bg-green-500"></span> FDSM_Career_DB
              </li>
              <li className="flex items-center gap-2 hover:text-white cursor-pointer px-2 py-1.5">
                <span className="w-2 h-2 rounded-full bg-zinc-700"></span> Local_Cache
              </li>
            </ul>
          </div>
          
          <div>
            <p className="text-xs font-semibold text-zinc-600 uppercase tracking-wider mb-3">Sessions</p>
            <ul className="space-y-2 text-sm text-zinc-400">
              <li className="hover:text-white cursor-pointer px-2 py-1">Schema Analysis</li>
              <li className="hover:text-white cursor-pointer px-2 py-1">Placement Stats</li>
            </ul>
          </div>
        </div>
        
        <div className="p-4 border-t border-zinc-800/60 text-xs text-zinc-600 flex justify-between items-center">
          <span>Agent: Coze Core</span>
          <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-yellow-500 animate-pulse"></span> Online</span>
        </div>
      </aside>

      {/* 2. 主工作区 (Main Content) */}
      <main className="flex-1 flex flex-col relative bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-zinc-900/40 via-[#09090b] to-[#09090b]">
        
        {/* 顶部导航 */}
        <header className="h-16 flex items-center justify-between px-8 border-b border-zinc-800/40 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center gap-3 text-sm text-zinc-400">
            <span className="hover:text-white cursor-pointer">Workspace</span>
            <span className="text-zinc-600">/</span>
            <span className="text-zinc-200 font-medium">Query Engine</span>
          </div>
          <div className="text-xs px-3 py-1 rounded-full border border-yellow-500/20 text-yellow-500/80 bg-yellow-500/5">
            COZE CONFIGURED
          </div>
        </header>

        {/* 聊天流区域 */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-8 md:px-12 lg:px-24">
          <div className="max-w-4xl mx-auto space-y-8 pb-32">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`
                  max-w-[85%] rounded-2xl p-6 text-[0.95rem] leading-relaxed shadow-sm
                  ${msg.role === 'user' 
                    ? 'bg-yellow-500 text-black font-medium' 
                    : 'bg-zinc-900/60 border border-zinc-800/80 text-zinc-300 backdrop-blur-sm'
                  }
                `}>
                  {/* 使用 whitespace-pre-wrap 渲染纯文本的换行 */}
                  <pre className="font-sans whitespace-pre-wrap">{msg.content}</pre>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 底部输入控制台 */}
        <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-[#09090b] via-[#09090b] to-transparent">
          <div className="max-w-4xl mx-auto">
            <div className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-yellow-500/20 to-zinc-800/50 rounded-[28px] blur opacity-40 group-hover:opacity-60 transition duration-500"></div>
              <div className="relative bg-[#121214] border border-zinc-800 rounded-[24px] flex items-center p-2 shadow-2xl">
                <textarea 
                  className="flex-1 bg-transparent border-none outline-none text-zinc-200 px-6 py-4 resize-none h-14"
                  placeholder="Ask your data..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                />
                <button className="bg-yellow-500 hover:bg-yellow-400 text-black font-bold px-8 py-3.5 rounded-[18px] transition-colors ml-2 shadow-[0_0_15px_rgba(247,198,0,0.2)]">
                  SEND
                </button>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
};

export default DigitalAnatomyDashboard;