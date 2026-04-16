import { useEffect, useState } from 'react'
import axios from 'axios'
import { motion, useMotionValue, useTransform, useSpring } from 'framer-motion'

// --- 1. ИНТЕРФЕЙСЫ ---
interface Product {
  id: number; title: string; description: string; price: string;
}
interface PaginatedResponse {
  items: Product[]; count: number;
}

// --- 2. КОМПОНЕНТ ЛАМПЫ (ЖИВАЯ ФИЗИКА) ---
const Lamp = ({ isDark, onToggle }: { isDark: boolean; onToggle: () => void }) => {
  const x = useMotionValue(0)
  const y = useMotionValue(0)

  const springConfig = { stiffness: 300, damping: 20 }
  const springX = useSpring(x, springConfig)
  const springY = useSpring(y, springConfig)

  // Магия кривой Безье для веревки
  const pathData = useTransform([springX, springY], ([latestX, latestY]: any) => {
    const startX = 50;
    const startY = 0;
    const endX = 50 + latestX;
    const endY = latestY + 60;
    const controlX = 50 + latestX * 0.3;
    const controlY = endY / 2;
    return `M ${startX},${startY} Q ${controlX},${controlY} ${endX},${endY}`;
  });

  return (
    <div className="absolute top-0 right-10 flex flex-col items-center z-50 pointer-events-none" style={{ width: 100 }}>
      <div className="w-0.5 h-10 bg-gray-600" />
      <div className={`w-12 h-14 rounded-b-full transition-all duration-500 border-t-4 border-gray-800 z-20
        ${isDark ? 'bg-yellow-400 shadow-[0_0_100px_rgba(250,204,21,1)]' : 'bg-gray-300'}`}
      />
      <div className="relative w-full flex flex-col items-center">
        <svg className="absolute top-0 overflow-visible w-full h-75 pointer-events-none">
          <motion.path
            d={pathData}
            fill="transparent"
            stroke={isDark ? "#94a3b8" : "#64748b"}
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
        <motion.div
          drag
          dragConstraints={{ top: 0, left: -80, right: 80, bottom: 200 }}
          dragElastic={0.1}
          style={{ x, y }}
          onDragEnd={(_, info) => {
            if (info.offset.y > 100) onToggle()
          }}
          className="w-8 h-8 bg-zinc-800 rounded-full border-2 border-slate-400 shadow-2xl flex items-center justify-center pointer-events-auto z-30 cursor-grab active:cursor-grabbing mt-15"
        >
          <div className="w-1.5 h-1.5 bg-white/20 rounded-full" />
        </motion.div>
      </div>
    </div>
  )
}

// --- 3. КОМПОНЕНТ ПОЛЗУНКА УДАЛЕНИЯ ---
const DeleteSlider = ({ onTrigger }: { onTrigger: () => void }) => {
  const [value, setValue] = useState(0)
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value)
    setValue(val)
    if (val > 92) { onTrigger(); setValue(0); }
  }

  return (
    <div className="w-full mt-6 h-16 flex items-center justify-center relative bg-gray-100 rounded-2xl overflow-hidden px-2 border border-gray-200">
      <span className="absolute top-2 text-[9px] uppercase font-black text-gray-400 pointer-events-none tracking-widest transition-opacity duration-200"
        style={{ opacity: value > 10 ? 0 : 0.7 }}>Тяни для удаления</span>
      <span className="absolute bottom-2 text-[10px] font-bold text-gray-300 pointer-events-none transition-opacity duration-200"
        style={{ opacity: value > 10 ? 0.8 : 0 }}>{value}%</span>
      <input type="range" min="0" max="100" value={value} onChange={handleChange}
        className="w-full h-full appearance-none bg-transparent cursor-pointer z-10 accent-red-600" />
    </div>
  )
}

// --- 4. ГЛАВНЫЙ КОМПОНЕНТ APP ---
export default function App() {
  const [products, setProducts] = useState<Product[]>([])
  const [confirmDelete, setConfirmDelete] = useState<{ id: number, title: string } | null>(null)
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    axios.get<PaginatedResponse>('http://localhost:8000/api/core/products?limit=10')
      .then(res => setProducts(res.data.items))
      .catch(err => console.error(err))
  }, [])

  const deleteProduct = () => {
    if (confirmDelete) {
      setProducts(prev => prev.filter(p => p.id !== confirmDelete.id))
      setConfirmDelete(null)
    }
  }

  return (
    <div className={`min-h-screen transition-colors duration-700 font-sans relative overflow-hidden
      ${isDark ? 'bg-zinc-950 text-white' : 'bg-gray-50 text-gray-900'}`}>

      <Lamp isDark={isDark} onToggle={() => setIsDark(!isDark)} />

      {confirmDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-md animate-fade" onClick={() => setConfirmDelete(null)} />
          <div className="bg-white rounded-[3rem] p-10 max-w-sm w-full shadow-2xl relative z-50 animate-zoom-fade text-gray-900 text-center">
            <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6"><span className="text-4xl">🗑️</span></div>
            <h2 className="text-3xl font-black uppercase italic mb-3 text-red-600 tracking-tighter">Точно?</h2>
            <p className="text-gray-500 mb-8 leading-relaxed">Товар <span className="font-black italic text-gray-800">"{confirmDelete.title}"</span> будет удален.</p>
            <div className="flex flex-col gap-3">
              <button onClick={deleteProduct} className="w-full bg-red-600 text-white py-5 rounded-2xl font-black uppercase tracking-widest hover:bg-red-700 active:scale-95 transition-all shadow-lg shadow-red-200">Да, снести</button>
              <button onClick={() => setConfirmDelete(null)} className="w-full bg-gray-100 text-gray-400 py-5 rounded-2xl font-black uppercase tracking-widest">Отмена</button>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-5xl mx-auto p-4 md:p-10">
        <h1 className={`text-6xl md:text-8xl font-black uppercase tracking-tighter mb-12 drop-shadow-md transition-colors duration-500
          ${isDark ? 'text-yellow-400' : 'text-red-600'}`}>
          Товары 🔥🤘🏻🫃
        </h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map(p => (
            <div key={p.id} className={`border-2 rounded-[2.5rem] shadow-sm hover:shadow-2xl transition-all duration-500 overflow-hidden flex flex-col
              ${isDark ? 'bg-zinc-900 border-zinc-800 shadow-yellow-500/5' : 'bg-white border-gray-100'}`}>
              <div className="p-8 grow">
                <h3 className={`text-2xl font-black mb-2 truncate ${isDark ? 'text-white' : 'text-gray-900'}`}>{p.title}</h3>
                <p className="text-gray-400 text-sm italic line-clamp-2">{p.description}</p>
              </div>
              <div className="p-8 pt-0 mt-auto">
                <div className="mb-2 flex flex-col">
                  <span className="text-[10px] text-gray-400 font-bold uppercase block mb-1 tracking-widest">Цена</span>
                  <span className={`text-3xl font-black ${isDark ? 'text-yellow-400' : 'text-gray-900'}`}>
                    {p.price} <span className="text-blue-500 font-bold">₽</span>
                  </span>
                </div>
                <DeleteSlider onTrigger={() => setConfirmDelete({ id: p.id, title: p.title })} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
