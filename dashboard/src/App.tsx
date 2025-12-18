import { useState } from 'react';
import { 
  Upload, CloudRain, Thermometer, Users, Clock, Zap, 
  MapPin, CheckCircle2, LayoutDashboard, Activity, Lightbulb, 
  Hammer, TrendingUp, AlertCircle
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, RadialBarChart, RadialBar, PolarAngleAxis,
  RadarChart, PolarGrid, PolarRadiusAxis, Radar, Legend
} from 'recharts';
import { motion } from 'framer-motion';
// 👇 AQUI ESTAVA O ERRO. ADICIONAMOS "type" NA IMPORTAÇÃO
import type { ReportData } from './types';

// 👇 ATUALIZE SEU LINK AQUI
const API_URL = "https://submeningeal-unexpansively-alberta.ngrok-free.dev/api/v1/complete-analysis"; 

function App() {
  const [data, setData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);
    formData.append("start_time", "12:00:00");
    formData.append("month", "12");

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "ngrok-skip-browser-warning": "true" },
        body: formData
      });
      
      if (!res.ok) throw new Error("Falha na comunicação com a API");
      
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError("Erro ao processar. Verifique se o Ngrok está rodando.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // --- TELA DE UPLOAD ---
  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-background relative overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
          className="bg-card/50 backdrop-blur-xl border border-white/10 p-10 rounded-3xl shadow-2xl max-w-lg w-full text-center z-10"
        >
          <div className="mb-8 flex justify-center">
            <div className="w-20 h-20 bg-gradient-to-tr from-primary to-secondary rounded-2xl flex items-center justify-center shadow-lg shadow-primary/25">
              <Activity size={40} className="text-white" />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
            Vitrine Virtual
          </h1>
          <p className="text-gray-400 mb-8 text-lg">Urban Analytics & Intelligence AI</p>
          
          <div className="space-y-4">
            <label className={`block w-full h-40 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all ${file ? 'border-primary bg-primary/10' : 'border-gray-700 hover:border-gray-500 hover:bg-white/5'}`}>
              <Upload className={`mb-3 ${file ? 'text-primary' : 'text-gray-500'}`} size={32} />
              <span className="text-sm font-medium text-gray-300">
                {file ? file.name : "Arraste ou clique para enviar vídeo"}
              </span>
              <input type="file" className="hidden" accept="video/*" onChange={e => setFile(e.target.files?.[0] || null)} />
            </label>

            {error && (
              <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-sm flex items-center justify-center gap-2">
                <AlertCircle size={16} /> {error}
              </div>
            )}

            <button 
              onClick={handleAnalyze} 
              disabled={!file || loading}
              className="w-full py-4 bg-gradient-to-r from-primary to-blue-600 hover:to-blue-500 rounded-xl font-bold text-white shadow-lg shadow-blue-900/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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

  // --- PREPARAÇÃO DOS DADOS ---
  
  // 1. Radar Data (Normalizado)
  const radarData = [
    { subject: 'Fluxo', A: Math.min(data.metrics_basic.fluxo.value * 2, 100), fullMark: 100 },
    { subject: 'Perm.', A: Math.min(data.metrics_basic.permanencia.value * 10, 100), fullMark: 100 },
    { subject: 'Veloc.', A: Math.max(100 - (data.metrics_behavioral.velocidade.value * 20), 0), fullMark: 100 },
    { subject: 'Vitalid.', A: data.urban_vitality_index, fullMark: 100 },
    { subject: 'Conf.', A: data.climate.temperature_avg_c > 28 ? 40 : 90, fullMark: 100 },
  ];

  // 2. Bar Chart Data (Comparativo)
  const barData = [
    { name: 'Fluxo', valor: data.metrics_basic.fluxo.value, fill: '#3b82f6' },
    { name: 'Perm.', valor: data.metrics_basic.permanencia.value, fill: '#8b5cf6' },
    { name: 'Veloc.', valor: data.metrics_behavioral.velocidade.value, fill: '#f59e0b' },
  ];

  // 3. Pie Chart Data (Recomendações)
  const recTypes = data.analysis.recomendacoes.reduce((acc: any, curr) => {
    acc[curr.tipo] = (acc[curr.tipo] || 0) + 1;
    return acc;
  }, {});
  const pieData = Object.keys(recTypes).map(key => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value: recTypes[key]
  }));
  const COLORS = ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981'];

  // 4. Vitality Gauge
  const vitalityData = [{ name: 'IVU', value: data.urban_vitality_index, fill: '#f59e0b' }];

  return (
    <div className="flex h-screen bg-background text-text overflow-hidden font-sans">
      
      {/* SIDEBAR */}
      <aside className="w-20 lg:w-64 bg-card/50 backdrop-blur-md border-r border-white/5 flex flex-col justify-between hidden md:flex">
        <div>
          <div className="h-20 flex items-center justify-center lg:justify-start lg:px-6 border-b border-white/5">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center shadow-lg shadow-primary/20">
              <Activity className="text-white" size={24} />
            </div>
            <span className="ml-3 font-bold text-lg hidden lg:block tracking-wide">Vitrine.AI</span>
          </div>
          
          <nav className="mt-8 space-y-2 px-3">
            <button className="flex items-center gap-3 w-full p-3 bg-primary/10 text-primary border border-primary/20 rounded-xl transition-all">
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
        <div className="h-1 w-full bg-gradient-to-r from-primary via-secondary to-accent fixed top-0 left-0 z-50 opacity-50" />

        <div className="p-4 lg:p-8 max-w-[1600px] mx-auto space-y-8">
          
          {/* HEADER */}
          <header className="flex flex-col md:flex-row justify-between md:items-center gap-4">
            <div>
              <div className="flex items-center gap-2 text-primary mb-1">
                <CheckCircle2 size={16} /> <span className="text-xs font-bold uppercase tracking-wider">Análise Concluída</span>
              </div>
              <h2 className="text-3xl font-bold">{data.context.local}</h2>
              <p className="text-gray-400 text-sm flex items-center gap-2 mt-1">
                <Clock size={14} /> Ref: {data.climate.hour}h00 • {data.video_id}
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
              className="bg-card border border-white/5 p-6 rounded-2xl relative group overflow-hidden hover:border-primary/30 transition-all">
               <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"><Users size={64} /></div>
               <p className="text-gray-400 text-sm font-medium mb-1">Fluxo Total</p>
               <div className="text-4xl font-bold text-white mb-2">{data.metrics_basic.fluxo.value}</div>
               <div className="inline-flex items-center text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded">{data.metrics_basic.fluxo.unit}</div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }}
              className="bg-card border border-white/5 p-6 rounded-2xl relative group overflow-hidden hover:border-secondary/30 transition-all">
               <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"><Clock size={64} /></div>
               <p className="text-gray-400 text-sm font-medium mb-1">Permanência Média</p>
               <div className="text-4xl font-bold text-white mb-2">{data.metrics_basic.permanencia.value}</div>
               <div className="inline-flex items-center text-xs font-medium text-secondary bg-secondary/10 px-2 py-1 rounded">{data.metrics_basic.permanencia.unit}</div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.3 }}
              className="bg-card border border-white/5 p-6 rounded-2xl relative group overflow-hidden hover:border-accent/30 transition-all">
               <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"><Zap size={64} /></div>
               <p className="text-gray-400 text-sm font-medium mb-1">Ritmo Médio</p>
               <div className="text-4xl font-bold text-white mb-2">{data.metrics_behavioral.velocidade.value}</div>
               <div className="inline-flex items-center text-xs font-medium text-accent bg-accent/10 px-2 py-1 rounded">{data.metrics_behavioral.velocidade.unit}</div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }}
              className="bg-gradient-to-br from-primary/20 to-secondary/10 border border-primary/20 p-6 rounded-2xl relative">
               <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-xs font-bold text-primary uppercase tracking-widest">Janela de Oportunidade</span>
               </div>
               <div className="text-xl font-bold text-white leading-tight mb-2">{data.opportunity_window.status}</div>
               <p className="text-sm text-gray-300">Horário Sugerido: {data.opportunity_window.horario}</p>
            </motion.div>
          </div>

          {/* CHARTS ROW 1: RADAR & GAUGE */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* RADAR CHART */}
            <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.5 }}
              className="bg-card border border-white/5 p-6 rounded-2xl lg:col-span-1 flex flex-col items-center justify-center">
              <h3 className="text-lg font-bold mb-6 flex items-center gap-2 w-full"><Activity size={18} className="text-secondary" /> Perfil Urbano</h3>
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

            {/* VITALITY GAUGE */}
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
                      <span className="text-accent"> {data.analysis.perfil.replace('_', ' ').toUpperCase()}</span>. 
                      A área apresenta potencial de ativação imediato.
                    </p>
                  </div>
               </div>
            </motion.div>
          </div>

          {/* CHARTS ROW 2: BAR & PIE */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* BAR CHART: COMPARATIVO */}
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

            {/* PIE CHART: TIPOS DE RECOMENDAÇÃO */}
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

          {/* LISTA DE RECOMENDAÇÕES */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.8 }} className="space-y-4">
              <h3 className="text-xl font-bold flex items-center gap-2"><Hammer className="text-primary" /> Oportunidades Públicas</h3>
              <p className="text-sm text-gray-400 mb-4">{data.analysis.oportunidade_publica.objetivo_urbano}</p>
              <div className="grid gap-4">
                {data.analysis.oportunidade_publica.intervencoes_leves.map((item, idx) => (
                  <div key={idx} className="bg-card border border-primary/20 p-4 rounded-xl flex items-start gap-4 hover:bg-primary/5 transition-colors">
                    <div className="p-2 bg-primary/10 rounded-lg text-primary mt-1"><Lightbulb size={20} /></div>
                    <div><h4 className="font-bold text-white">{item.acao}</h4><p className="text-sm text-gray-400 mt-1">{item.objetivo}</p></div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.9 }} className="space-y-4">
               <h3 className="text-xl font-bold flex items-center gap-2"><TrendingUp className="text-accent" /> Recomendações de Uso</h3>
               <div className="grid gap-4">
                 {data.analysis.recomendacoes.map((rec, idx) => (
                   <div key={idx} className="bg-card border border-white/5 p-4 rounded-xl flex items-center justify-between group hover:border-accent/30 transition-all">
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