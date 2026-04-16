import { motion, useMotionValue, useTransform, useSpring } from 'framer-motion'

interface LampProps {
    isDark: boolean;
    onToggle: () => void;
}

export default function Lamp({ isDark, onToggle }: LampProps) {
    const x = useMotionValue(0)
    const y = useMotionValue(0)

    // Пружина для плавного возврата
    const springConfig = { stiffness: 300, damping: 20 }
    const springX = useSpring(x, springConfig)
    const springY = useSpring(y, springConfig)

    // Рисуем кривую веревку через SVG
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
        ${isDark ? 'bg-yellow-400 shadow-[0_0_100px_rgba(250,204,21,1)]' : 'bg-gray-300 shadow-inner'}`}
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
                    className="w-8 h-8 bg-zinc-800 rounded-full border-2 border-slate-400 shadow-2xl flex items-center justify-center pointer-events-auto z-30 cursor-grab active:cursor-grabbing mt-[60px]"
                >
                    <div className="w-1.5 h-1.5 bg-white/20 rounded-full" />
                </motion.div>
            </div>
        </div>
    )
}
