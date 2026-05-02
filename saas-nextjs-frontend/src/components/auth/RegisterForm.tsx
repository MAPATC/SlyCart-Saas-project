"use client"
import { PatternFormat } from 'react-number-format';
import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';
import axios from 'axios';

type Role = 'customer' | 'owner' | null;
type Confirmed = true | false;

function Register() {
    const [role, setRole] = useState<Role>(null);
    const [isConfirmed, setIsConfirmed] = useState<Confirmed>(false);
    const [phone, setPhone] = useState('');

    const sendLog = async (action: string) => {
        console.log(`[LOG]: User performed action: ${action}`);
    };

    return (
        <div className="relative flex h-screen w-full items-center justify-center bg-slate-100 overflow-hidden">

            {/* ФОНОВЫЙ ПАТТЕРН */}
            <div
                className="fixed inset-0 z-0 pointer-events-none"
                style={{
                    backgroundImage: `url('/logo.png')`,
                    backgroundSize: '135px 135px',
                    backgroundRepeat: 'repeat',
                    backgroundPosition: 'center',
                    opacity: 0.05, // Чуть увеличил для видимости
                    filter: 'blur(1px)',
                }}
            />

            <div className="relative z-10 w-full flex justify-center">
                <AnimatePresence mode='wait'>

                    {/* STEP 1: CHOOSE ROLE */}
                    {!role && (
                        <motion.div
                            key="role-selection"
                            className="flex h-112.5 w-125 flex-col items-center rounded-[2.5rem] bg-white/80 backdrop-blur-xl p-12 shadow-2xl shadow-slate-300/50 border border-white"
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: -20 }}
                            transition={{ duration: 0.4, ease: "easeOut" }}
                        >
                            <motion.h2
                                className="bg-linear-to-r from-blue-600 to-emerald-500 bg-clip-text text-4xl font-bold text-transparent mb-auto"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 }}
                            >
                                Выберите роль
                            </motion.h2>

                            <div className="flex w-full gap-6 mt-auto">
                                {/* Кнопки вынес бы в отдельный компонент, если их будет больше */}
                                <RoleButton
                                    label="Покупатель"
                                    emoji="🛍️"
                                    color="from-blue-500 to-indigo-600"
                                    hoverColor="from-cyan-400 to-blue-500"
                                    onClick={() => { setRole("customer"); sendLog("selected_customer_role"); }}
                                />
                                <RoleButton
                                    label="Продавец"
                                    emoji="📦"
                                    color="from-emerald-500 to-teal-600"
                                    hoverColor="from-green-400 to-emerald-500"
                                    onClick={() => { setRole("owner"); sendLog("selected_owner_role"); }}
                                />
                            </div>
                        </motion.div>
                    )}

                    {/* STEP 2: CONFIRMATION */}
                    {role && !isConfirmed && (
                        <motion.div
                            key="confirmation"
                            className="flex h-112.5 w-125 flex-col items-center justify-center rounded-[2.5rem] bg-white p-12 shadow-2xl text-center border border-slate-100"
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -50 }}
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        >
                            <div className="text-7xl mb-6 drop-shadow-lg">
                                {role === 'owner' ? '📦' : '🛍️'}
                            </div>
                            <h2 className="text-3xl font-black mb-2 text-slate-800">Вы уверены?</h2>
                            <p className="text-slate-500 mb-10">
                                Ваш выбор: <span className="font-bold text-slate-700">{role === 'owner' ? 'Продавец' : 'Покупатель'}</span>
                            </p>

                            <div className="flex w-full gap-4">
                                <button
                                    onClick={() => setIsConfirmed(true)}
                                    className="flex-2 py-4 bg-linear-to-r from-emerald-500 to-teal-600 text-white rounded-2xl font-bold shadow-lg hover:brightness-110 transition-all active:scale-95"
                                >
                                    Подтвердить
                                </button>
                                <button
                                    onClick={() => setRole(null)}
                                    className="flex-1 py-4 bg-slate-100 text-slate-600 rounded-2xl font-bold hover:bg-slate-200 transition-all active:scale-95"
                                >
                                    Назад
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {/* STEP 3: REGISTRATION */}
                    {isConfirmed && (
                        <motion.div
                            key="registration-form"
                            className="flex h-112.5 w-125 flex-col items-center rounded-[2.5rem] bg-white p-12 shadow-2xl border border-slate-100"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 1.1 }}
                        >
                            <h2 className="text-3xl font-black mb-2 italic">SlyCart</h2>
                            <p className="text-slate-400 mb-8 text-center">Регистрация для роли {role === 'owner' ? 'продавца' : 'покупателя'}</p>

                            <div className="w-full space-y-4">
                                <input
                                    type="number"
                                    placeholder="Телеграм ID"
                                    className="w-full p-4 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-400 focus:ring-4 ring-blue-50/50 transition-all"
                                />
                                <PatternFormat
                                    format="+7 (###) ###-##-##"
                                    allowEmptyFormatting
                                    mask="_"
                                    value={phone}
                                    onValueChange={(values) => setPhone(values.value)} // Сохранит только цифры: 79991234567
                                    className="w-full p-4 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-400 focus:ring-4 ring-blue-50/50 transition-all text-slate-700"
                                    placeholder="Номер телефона"
                                />
                                <button className="w-full py-4 bg-blue-600 text-white rounded-xl font-bold shadow-lg shadow-blue-200 hover:bg-blue-700 transition-colors">
                                    Создать аккаунт
                                </button>
                            </div>

                            <div className="m-auto py-6">
                                <button
                                    onClick={() => { setRole(null); setIsConfirmed(false); }}
                                    className="mt-auto bg-slate-100 text-slate-600 rounded-2xl font-bold hover:bg-slate-200 transition-all active:scale-95 p-4"
                                >
                                    Отменить
                                </button>

                            </div>

                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}

// Вспомогательный компонент для кнопок выбора роли
function RoleButton({ label, emoji, color, onClick }: any) {
    return (
        <motion.button
            onClick={onClick}
            className={`flex-1 rounded-3xl py-8 text-white font-bold text-lg cursor-pointer shadow-lg bg-linear-to-br ${color}`}
            whileHover={{
                scale: 1.05,
                y: -5,
                backgroundImage: `linear-gradient(135deg, var(--tw-gradient-from), var(--tw-gradient-to))`
            }}
            whileTap={{ scale: 0.95 }}
        >
            <span className="flex flex-col items-center gap-2">
                <span className="text-4xl">{emoji}</span>
                {label}
            </span>
        </motion.button>
    );
}

//TODO: 1) Unactive create button, 2) useMutation, 3) Success screen  

export default Register;