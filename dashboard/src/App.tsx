import { useState } from 'react';
import { 
  Upload, CloudRain, Thermometer, Users, Clock, Zap, 
  MapPin, CheckCircle2, LayoutDashboard, Activity, Lightbulb, 
  Hammer, TrendingUp, AlertCircle, Calendar
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, RadialBarChart, RadialBar, PolarAngleAxis,
  RadarChart, PolarGrid, PolarRadiusAxis, Radar, Legend
} from 'recharts';
import { motion } from 'framer-motion';
import type { ReportData } from './types';

// 👇 IMPORTANTE: Importando sua logo (certifique-se que ela está na pasta src com nome logo.png)
import logoImg from './logo.png';

// 👇 MANTENHA O SEU LINK CORRETO DO NGROK AQUI
const API_URL = "https://submeningeal-unexpansively-alberta.ngrok-free.dev/api/v1/complete-analysis"; 

function App() {
  const [data, setData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Novos Estados para Inputs do Usuário
  const [selectedMonth, setSelectedMonth] = useState("4"); // Default: Abril
  const [selectedTime, setSelectedTime] = useState("12:00"); // Default: Meio-dia

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);
    // Adiciona os segundos (:00) para garantir formato HH:MM:SS
    formData.append("start_time", `${selectedTime}:00`); 
    formData.append("month", selectedMonth);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "ngrok-skip-browser-warning": "true" },
        body: formData
      });
      
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Erro API: ${res.status} - ${errText}`);
      }
      
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError("Erro ao processar. Verifique se o link do Ngrok no código está igual ao do terminal.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // --- TELA DE UPLOAD (Inicial) ---
  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-background relative overflow-hidden">
        {/* Efeitos de Fundo */}
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
          className="bg-card/50 backdrop-blur-xl border border-white/10 p-8 md:p-10 rounded-3xl shadow-2xl max-w-lg w-full text-center z-10"
        >
          <div className="mb-6 flex justify-center">
            {/* LOGO GRANDE NA TELA INICIAL */}
            <div className="relative">
              <div className="absolute inset-0 bg-purple-500 blur-2xl opacity-20 rounded-full"></div>
              <img 
                src={logoImg} 
                alt="Cidade Viva Logo" 
                className="w-24 h-24 object-contain relative z-10 drop-shadow-[0_0_15px_rgba(168,85,247,0.5)]" 
              />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
            Cidade Viva
          </h1>
          <p className="text-gray-400 mb-8">Inteligência Artificial para Espaços Urbanos</p>
          
          <div className="space-y-4 text-left">
            
            {/* Input de Arquivo */}
            <label className={`block w-full h-32 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all ${file ? 'border-purple-500 bg-purple-500/10' : 'border-gray-700 hover:border-gray-500 hover:bg-white/5'}`}>
              <Upload className={`mb-2 ${file ? 'text-purple-400' : 'text-gray-500'}`} size={24} />
              <span className="text-sm font-medium text-gray-300 text-center px-4">
                {file ? file.name : "Clique para selecionar o vídeo (MP4)"}
              </span>
              <input type="file" className="hidden" accept="video/*" onChange={e => setFile(e.target.files?.[0] || null)} />
            </label>

            {/* Grid de Inputs (Mês e Hora) */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs text-gray-400 ml-1 flex items-center gap-1"><Calendar size={12}/> Mês da Análise</label>
                <select 
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-purple-500 focus:bg-white/10 transition-all appearance-none cursor-pointer"
                >
                  <option value="1" className="bg-card">Janeiro</option>
                  <option value="2" className="bg-card">Fevereiro</option>
                  <option value="3" className="bg-card">Março</option>
                  <option value="4" className="bg-card">Abril</option>
                  <option value="5" className="bg-card">Maio</option>
                  <option value="6" className="bg-card">Junho</option>
                  <option value="7" className="bg-card">Julho</option>
                  <option value="8" className="bg-card">Agosto</option>
                  <option value="9" className="bg-card">Setembro</option>
                  <option value="10" className="bg-card">Outubro</option>
                  <option value="11" className="bg-card">Novembro</option>
                  <option value="12" className="bg-card">Dezembro</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs text-gray-400 ml-1 flex items-center gap-1"><Clock size={12}/> Horário</label>
                <input 
                  type="time" 
                  value={selectedTime}
                  onChange={(e) => setSelectedTime(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-purple-500 focus:bg-white/10 transition-all cursor-pointer"
                />
              </div>
            </div>

            {error && (
              <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-xs flex items-center justify-center gap-2 text-center">
                <AlertCircle size={16} /> {error}
              </div>
            )}

            <button 
              onClick={handleAnalyze} 
              disabled={!file || loading}
              className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:to-blue-500 rounded-xl font-bold text-white shadow-lg shadow-purple-900/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-4"
            >
              {loading ? (
                <><span className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span> Processando...</>
              ) : (
                <><TrendingUp size={20} /> Gerar Relatório Completo</>
              )}
            </button>
          </div>
        </motion.div>
      </div>
    );
  }

  // --- DASHBOARD (View) ---
  
  const radarData = [
    { subject: 'Fluxo', A: Math.min(data.metrics_basic.fluxo.value * 2, 100), fullMark: 100 },
    { subject: 'Perm.', A: Math.min(data.metrics_basic.permanencia.value * 10, 100), fullMark: 100 },
    { subject: 'Veloc.', A: Math.max(100 - (data.metrics_behavioral.velocidade.value * 20), 0), fullMark: 100 },
    { subject: 'Vitalid.', A: data.urban_vitality_index, fullMark: 100 },
    { subject: 'Conf.', A: data.climate.temperature_avg_c > 28 ? 40 : 90, fullMark: 100 },
  ];

  const barData = [
    { name: 'Fluxo', valor: data.metrics_basic.fluxo.value, fill: '#3b82f6' },
    { name: 'Perm.', valor: data.metrics_basic.permanencia.value, fill: '#8b5cf6' },
    { name: 'Veloc.', valor: data.metrics_behavioral.velocidade.value, fill: '#f59e0b' },
  ];

  const recTypes = data.analysis.recomendacoes.reduce((acc: any, curr) => {
    acc[curr.tipo] = (acc[curr.tipo] || 0) + 1;
    return acc;
  }, {});
  const pieData = Object.keys(recTypes).map(key => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value: recTypes[key]
  }));
  const COLORS = ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981'];

  const vitalityData = [{ name: 'IVU', value: data.urban_vitality_index, fill: '#f59e0b' }];

  return (
    <div className="flex h-screen bg-background text-text overflow-hidden font-sans">
      
      {/* SIDEBAR */}
      <aside className="w-20 lg:w-64 bg-card/50 backdrop-blur-md border-r border-white/5 flex flex-col justify-between hidden md:flex">
        <div>
          <div className="h-20 flex items-center justify-center lg:justify-start lg:px-6 border-b border-white/5">
            {/* LOGO PEQUENA NA SIDEBAR */}
            <div className="w-10 h-10 flex items-center justify-center">
              <img src={logoImg} alt="Logo" className="w-full h-full object-contain drop-shadow-[0_0_8px_rgba(168,85,247,0.5)]" />
            </div>
            <span className="ml-3 font-bold text-lg hidden lg:block tracking-wide text-white">Cidade Viva</span>
          </div>
          
          <nav className="mt-8 space-y-2 px-3">
            <button className="flex items-center gap-3 w-full p-3 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-xl transition-all">
              <LayoutDashboard size={22} /> <span className="hidden lg:block font-medium">Dashboard</span>
            </button>
            <button className="flex items-center gap-3 w-full p-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-all">
              <MapPin size={22} /> <span className="hidden lg:block font-medium">Mapa de Calor</span>
            </button>
          </nav>
        </div>

        <div className="p-4">
          <button onClick={() => setData(null)} className="flex items-center gap-2 w-full p-3 text-red-400 hover:bg-red-500/10 rounded-xl transition-colors text-sm font-medium">
             <span className="hidden lg:block">← Nova Análise</span>
          </button>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 overflow-y-auto relative">
        <div className="h-1 w-full bg-gradient-to-r from-purple-500 via-blue-500 to-purple-400 fixed top-0 left-0 z-50 opacity-50" />

        <div className="p-4 lg:p-8 max-w-[1600px] mx-auto space-y-8">
          
          {/* HEADER */}
          <header className="flex flex-col md:flex-row justify-between md:items-center gap-4">
            <div>
              <div className="flex items-center gap-2 text-purple-400 mb-1">
                <CheckCircle2 size={16} /> <span className="text-xs font-bold uppercase tracking-wider">Análise Concluída</span>
              </div>
              <h2 className="text-3xl font-bold text-white">{data.context.local}</h2>
              <p className="text-gray-400 text-sm flex items-center gap-2 mt-1">
                <Clock size={14} /> Ref: {data.climate.hour}h00 • Mês {data.climate.month} • {data.video_id}
              </p>
            </div>
            
            <div className="flex items-center gap-3 bg-card border border-white/5 p-2 rounded-xl">
               <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${data.climate.temperature_avg_c > 28 ? 'bg-orange-500/10 text-orange-400' : 'bg-blue-500/10 text-blue-400'}`}>
                  <Thermometer size={18} /> <span className="font-bold">{data.climate.temperature_avg_c}°C</span>
               </div>
               <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-500/10 text-blue-400">
                  <CloudRain size={18} /> <span className="font-bold">{data.climate.rain_probability_pct}%</span>
               </div>
            </div>
          </header>

          {/* KPI CARDS */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.1 }}
              className="bg-card border border-white/5 p-6 rounded-2xl relative group overflow-hidden hover:border-purple-500/30 transition-all">
               <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"><Users size={64} /></div>
               <p className="text-gray-400 text-sm font-medium mb-1">Fluxo Total</p>
               <div className="text-4xl font-bold text-white mb-2">{data.metrics_basic.fluxo.value}</div>
               <div className="inline-flex items-center text-xs font-medium text-purple-400 bg-purple-500/10 px-2 py-1 rounded">{data.metrics_basic.fluxo.unit}</div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }}
              className="bg-card border border-white/5 p-6 rounded-2xl relative group overflow-hidden hover:border-blue-500/30 transition-all">
               <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"><Clock size={64} /></div>
               <p className="text-gray-400 text-sm font-medium mb-1">Permanência Média</p>
               <div className="text-4xl font-bold text-white mb-2">{data.metrics_basic.permanencia.value}</div>
               <div className="inline-flex items-center text-xs font-medium text-blue-400 bg-blue-500/10 px-2 py-1 rounded">{data.metrics_basic.permanencia.unit}</div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.3 }}
              className="bg-card border border-white/5 p-6 rounded-2xl relative group overflow-hidden hover:border-orange-500/30 transition-all">
               <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"><Zap size={64} /></div>
               <p className="text-gray-400 text-sm font-medium mb-1">Ritmo Médio</p>
               <div className="text-4xl font-bold text-white mb-2">{data.metrics_behavioral.velocidade.value}</div>
               <div className="inline-flex items-center text-xs font-medium text-orange-400 bg-orange-500/10 px-2 py-1 rounded">{data.metrics_behavioral.velocidade.unit}</div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }}
              className="bg-gradient-to-br from-purple-500/20 to-blue-500/10 border border-purple-500/20 p-6 rounded-2xl relative">
               <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-xs font-bold text-purple-400 uppercase tracking-widest">Janela de Oportunidade</span>
               </div>
               <div className="text-xl font-bold text-white leading-tight mb-2">{data.opportunity_window.status}</div>
               <p className="text-sm text-gray-300">Horário Sugerido: {data.opportunity_window.horario}</p>
            </motion.div>
          </div>

          {/* CHARTS ROW 1 */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.5 }}
              className="bg-card border border-white/5 p-6 rounded-2xl lg:col-span-1 flex flex-col items-center justify-center">
              <h3 className="text-lg font-bold mb-6 flex items-center gap-2 w-full"><Activity size={18} className="text-blue-400" /> Perfil Urbano</h3>
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                    <PolarGrid stroke="#334155" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar name="Local" dataKey="A" stroke="#8b5cf6" strokeWidth={3} fill="#8b5cf6" fillOpacity={0.3} />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.6 }}
              className="bg-card border border-white/5 p-6 rounded-2xl lg:col-span-2 flex flex-col md:flex-row items-center gap-8">
               <div className="relative w-64 h-64 flex-shrink-0">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadialBarChart innerRadius="80%" outerRadius="100%" data={vitalityData} startAngle={180} endAngle={0}>
                      <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                      <RadialBar background dataKey="value" cornerRadius={30} fill="#f59e0b" />
                    </RadialBarChart>
                  </ResponsiveContainer>
                  <div className="absolute inset-0 flex flex-col items-center justify-center pt-8">
                     <span className="text-5xl font-bold text-white">{data.urban_vitality_index}</span>
                     <span className="text-sm text-gray-500 uppercase tracking-widest mt-1">Índice IVU</span>
                  </div>
               </div>
               <div className="flex-1 space-y-4">
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">Diagnóstico de Vitalidade</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">
                      O índice de <strong>{data.urban_vitality_index}</strong> indica um perfil 
                      <span className="text-purple-400"> {data.analysis.perfil.replace('_', ' ').toUpperCase()}</span>. 
                      Os dados foram calculados considerando as condições climáticas de {data.climate.month === 12 ? "Dezembro" : "Abril"}.
                    </p>
                  </div>
               </div>
            </motion.div>
          </div>

          {/* CHARTS ROW 2 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.6 }}
              className="bg-card border border-white/5 p-6 rounded-2xl">
              <h3 className="text-lg font-bold mb-4">Métricas Comparativas</h3>
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={barData} layout="vertical" margin={{ left: 20 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ backgroundColor: '#0f172a', border: 'none' }} />
                    <Bar dataKey="valor" radius={[0, 4, 4, 0]} barSize={30} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.7 }}
              className="bg-card border border-white/5 p-6 rounded-2xl flex flex-col">
               <h3 className="text-lg font-bold mb-4">Distribuição de Recomendações</h3>
               <div className="flex-1 flex items-center justify-center relative">
                 <div className="w-full h-[250px]">
                   <ResponsiveContainer width="100%" height="100%">
                     <PieChart>
                       <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                         {pieData.map((entry, index) => (
                           <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} strokeWidth={0} />
                         ))}
                       </Pie>
                       <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none' }} />
                       <Legend verticalAlign="bottom" height={36}/>
                     </PieChart>
                   </ResponsiveContainer>
                 </div>
               </div>
            </motion.div>
          </div>

          {/* RECOMENDAÇÕES */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.8 }} className="space-y-4">
              <h3 className="text-xl font-bold flex items-center gap-2"><Hammer className="text-purple-400" /> Oportunidades Públicas</h3>
              <p className="text-sm text-gray-400 mb-4">{data.analysis.oportunidade_publica.objetivo_urbano}</p>
              <div className="grid gap-4">
                {data.analysis.oportunidade_publica.intervencoes_leves.map((item, idx) => (
                  <div key={idx} className="bg-card border border-purple-500/20 p-4 rounded-xl flex items-start gap-4 hover:bg-purple-500/5 transition-colors">
                    <div className="p-2 bg-purple-500/10 rounded-lg text-purple-400 mt-1"><Lightbulb size={20} /></div>
                    <div><h4 className="font-bold text-white">{item.acao}</h4><p className="text-sm text-gray-400 mt-1">{item.objetivo}</p></div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.9 }} className="space-y-4">
               <h3 className="text-xl font-bold flex items-center gap-2"><TrendingUp className="text-orange-400" /> Recomendações de Uso</h3>
               <div className="grid gap-4">
                 {data.analysis.recomendacoes.map((rec, idx) => (
                   <div key={idx} className="bg-card border border-white/5 p-4 rounded-xl flex items-center justify-between group hover:border-orange-500/30 transition-all">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${rec.tipo === 'cultura' ? 'bg-purple-500/20 text-purple-300' : rec.tipo === 'comercio' ? 'bg-green-500/20 text-green-300' : 'bg-orange-500/20 text-orange-300'}`}>{rec.tipo}</span>
                        </div>
                        <p className="font-semibold text-white">{rec.item}</p>
                        <p className="text-xs text-gray-500 mt-0.5">{rec.porque}</p>
                      </div>
                   </div>
                 ))}
               </div>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;