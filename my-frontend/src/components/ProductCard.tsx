import { Product } from "../App";

interface Props {
    product: Product;
}

export const ProductCard = ({ product }: Props) => {
    return (
        <div className="p-4 bg-white border border-gray-100 rounded-2xl shadow-sm hover:shadow-md transition-all cursor-pointer flex flex-col gap-2 h-fit">
            {/* Верхний ряд: Заголовок и Статус */}
            <div className="flex justify-between items-start">
                <h3 className="text-sm font-bold text-gray-900 truncate">
                    {product.title}
                </h3>
                <div className="flex gap-1">
                    <span className="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">
                        📦 {product.stock}
                    </span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${product.is_active ? 'text-green-600 bg-green-50' : 'text-gray-400 bg-gray-50'}`}>
                        {product.is_active ? 'В НАЛИЧИИ' : 'ПАУЗА'}
                    </span>
                </div>
            </div>

            {/* Описание — компактно */}
            <p className="text-[11px] text-gray-500 line-clamp-1 leading-relaxed">
                {product.description || 'Без описания'}
            </p>

            {/* Нижний ряд: Цена и кнопка */}
            <div className="flex items-center justify-between mt-1 pt-2 border-t border-gray-50">
                <span className="text-sm font-black text-gray-900">
                    {Number(product.price).toLocaleString()} ₽
                </span>
                <button className="text-[10px] font-black text-blue-600 tracking-tighter hover:text-blue-800">
                    УПРАВЛЯТЬ
                </button>
            </div>
        </div>
    )
};
