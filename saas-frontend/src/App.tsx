import { motion } from 'motion/react';
import './App.css'

function App() {
  return (
    <div className="flex h-screen items-center justify-center bg-slate-50">
      <motion.div
        className="flex h-112.5 w-125 flex-col items-center rounded-[2.5rem] bg-white p-12 shadow-2xl shadow-slate-200"
        initial={{ opacity: 0, y: -200 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.1, ease: "easeInOut" }}
      >
        <motion.h2 className="bg-linear-to-r from-blue-600 to-emerald-500 bg-clip-text text-4xl font-black text-transparent mb-auto"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 1, ease: "easeOut" }}>
          Выберите роль
        </motion.h2>

        <div className="flex w-full gap-6 mt-auto">

          {/* КНОПКА ПОКУПАТЕЛЬ */}
          <motion.button
            className="flex-1 rounded-3xl py-8 text-white font-bold text-lg cursor-pointer shadow-lg"
            style={{
              background: "linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%)",
              backgroundSize: "200% 200%"
            }}
            initial={{
              opacity: 0
            }}
            animate={{
              opacity: 1
            }}
            transition={{
              default: { duration: 0.8, delay: 1.6 },
              scale: { duration: 0.2 },
              background: { duration: 0.4 },
              boxShadow: { duration: 1 },
              y: { duration: 0.2 },
            }}
            whileHover={{
              scale: 1.05,
              y: -3,
              background: "linear-gradient(135deg, #22d3ee 0%, #3b82f6 100%)",
              boxShadow: "0 10px 25px rgba(59, 130, 246, 0.5)",
              transition: { duration: 0.2 }
            }}
            whileTap={{ scale: 0.95, transition: { duration: 0.1 } }}
          >
            <span className="flex items-center justify-center gap-2">
              <span>🛍️</span> Покупатель
            </span>
          </motion.button>

          {/* КНОПКА ПРОДАВЕЦ */}
          <motion.button
            className="flex-1 rounded-3xl py-8 text-white font-bold text-lg cursor-pointer shadow-lg"
            style={{
              background: "linear-gradient(135deg, #10b981 0%, #0d9488 100%)",
              backgroundSize: "200% 200%"
            }}
            initial={{
              opacity: 0
            }}
            animate={{
              opacity: 1
            }}
            transition={{
              default: { duration: 0.8, delay: 1.7 },
              scale: { duration: 0.2 },
              background: { duration: 0.4 },
              boxShadow: { duration: 1 },
              y: { duration: 0.2 },
            }}
            whileHover={{
              scale: 1.05,
              y: -3,
              background: "linear-gradient(135deg, #4ade80 0%, #10b981 100%)",
              boxShadow: "0 10px 25px rgba(16, 185, 129, 0.5)",
              transition: { duration: 0.2 }
            }}
            whileTap={{ scale: 0.95, transition: { duration: 0.1 } }}
          >
            <span className="flex items-center justify-center gap-2">
              <span>📦</span> Продавец
            </span>
          </motion.button>

        </div>
      </motion.div>
    </div>
  )
}

export default App
