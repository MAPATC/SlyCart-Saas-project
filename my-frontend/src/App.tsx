import { useEffect, useState } from 'react'
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { ProductCard } from './components/ProductCard'

const queryClient = new QueryClient()


// 1. Описываем интерфейс (наш контракт)
export interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  stock: number;
  is_active: boolean;
  shop_id: string;
}

// 2. Объявляем функцию с именем App (именно это имя ищет экспорт)
export default function App() {

  return (
    <QueryClientProvider client={queryClient}>
      <Products />
    </QueryClientProvider>
  )
}

const fetchProducts = async () => {
  const response = await axios.get("http://127.0.0.1:8000/api/core/products?limit=5");
  return response.data.items;
}

function Products() {
  // хуки нельзя использовать вне функции

  const { data, isError, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  });

  return (
    <div className="flex flex-col items-center w-full bg-gray-50 min-h-screen p-4">
      {/* Контейнер, который ограничивает ширину всего контента */}
      <div className="w-full max-w-3xl">
        <h1 className="text-2xl font-black mb-6 text-gray-800">
          Список товаров CRM
        </h1>

        {isLoading && <p className="text-gray-500">Загрузка данных...</p>}
        {isError && <p className="text-red-500">Ошибка при получении данных!</p>}

        {/* Список карточек в одну колонку */}
        <div className="flex flex-col gap-4">
          {data && data.map((product: Product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </div>
  );
};




// && условный рендеринг, и если условно iserror - true, то все после него отобразится, а иначе игнор