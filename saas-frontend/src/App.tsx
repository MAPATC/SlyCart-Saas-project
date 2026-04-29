import { motion, AnimatePresence } from 'motion/react';
import './App.css'
import { useState } from 'react';

type Role = 'customer' | 'owner' | null;

function App() {

  const [role, setRole] = useState<Role>(null); // state for role
  const [isConfirmed, setIsConfirmed] = useState(false); // state for confirmed role

  const sendLog = async (action: string) => {
    console.log(`[LOG]: User performed action: ${action}`);
    // Here you can use axios.post('/api/logs', { action })
  };


  return (
    <div className="flex h-screen items-center justify-center bg-slate-100">
      <AnimatePresence mode='wait'>

        {/* STEP 1: CHOOSE ROLE */}
        {!role && (

          <motion.div
            key="role-selection" // Specific key for the first screen. Using key for smooth animation transitions
            className="flex h-112.5 w-125 flex-col items-center rounded-[2.5rem] bg-white p-12 shadow-2xl shadow-slate-200"
            initial={{ opacity: 0, y: -200 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.1, ease: "easeInOut" }}
          >
            <motion.h2 className="bg-linear-to-r from-blue-600 to-emerald-500 bg-clip-text text-4xl font-black text-transparent mb-auto"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 1, ease: "easeOut" }}
            >
              Выберите роль
            </motion.h2>

            <div className="flex w-full gap-6 mt-auto">

              {/* КНОПКА ПОКУПАТЕЛЬ */}
              <motion.button
                onClick={() => {
                  setRole("customer");
                  sendLog("selected_customer_role")
                }}
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
                <span className="flex flex-col items-center justify-center gap-2">
                  <span className="text-4xl">🛍️</span> Покупатель
                </span>
              </motion.button>

              {/* КНОПКА ПРОДАВЕЦ */}
              <motion.button
                onClick={() => {
                  setRole("owner");
                  sendLog("selected_owner_role")
                }}
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
                <span className="flex flex-col items-center justify-center gap-2">
                  <span className="text-4xl">📦</span> Продавец
                </span>
              </motion.button>

            </div>
          </motion.div>
        )}

        {/* STEP 2: CONFIRMATION */}
        {role && !isConfirmed && (
          <motion.div
            key="confirmation" // Different key triggers the transition
            className="flex h-112.5 w-125 flex-col items-center justify-center rounded-[2.5rem] bg-white p-12 shadow-2xl shadow-slate-200 text-center"
            initial={{ opacity: 0, x: 200 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -200 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <div className="text-6xl mb-6">{role === 'owner' ? '📦' : '🛍️'}</div>
            <h2 className="text-3xl font-black mb-4 text-slate-800">Вы уверены?</h2>
            <p className="text-slate-500 mb-10">
              Вы выбрали роль: <b>{role === 'owner' ? 'Продавец' : 'Покупатель'}</b>
            </p>

            <div className="flex w-full gap-4">
              <motion.button
                onClick={() => setIsConfirmed(true)}
                className="flex-1 py-4 bg-emerald-500 text-white rounded-2xl font-bold shadow-lg"
                style={{
                  background: "linear-gradient(135deg, #10b981 0%, #0d9488 100%)",
                  backgroundSize: "200% 200%"
                }}
                transition={{
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
                Confirm
              </motion.button>
              <motion.button
                onClick={() => setRole(null)}
                className="flex-1 py-4 bg-slate-100 text-slate-600 rounded-2xl font-bold"
                transition={{
                  scale: { duration: 0.2 },
                  y: { duration: 0.2 },
                  boxShadow: { duration: 0.3 },
                }}
                whileHover={{
                  scale: 1.05,
                  y: -3,
                  boxShadow: "0 10px 25px rgba(100, 116, 139, 0.4)",
                  transition: { duration: 0.2 }
                }}
                whileTap={{ scale: 0.95, transition: { duration: 0.1 } }}
              >
                Back
              </motion.button>
            </div>
          </motion.div>
        )}
        {/* STEP 3: MOCK REGISTRATION FORM */}
        {isConfirmed && (
          <motion.div
            key="registration-form"
            className="flex h-112.5 w-125 flex-col items-center rounded-[2.5rem] bg-white p-12 shadow-2xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <h2 className="text-3xl font-black mb-6">Registration</h2>
            <p className="text-slate-400 mb-6">Creating account for {role}</p>
            <input placeholder="Username" className="w-full p-4 mb-4 bg-slate-100 rounded-xl outline-none focus:ring-2 ring-blue-400 transition-all" />
            <button className="w-full py-4 bg-blue-600 text-white rounded-xl font-bold">Register Now</button>
            <button onClick={() => { setRole(null); setIsConfirmed(false) }} className="mt-4 text-slate-400 text-sm underline">Cancel</button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App
