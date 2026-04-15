import { useEffect, useState } from 'react'
import axios from 'axios'

// 1. Описываем структуру твоего товара (Тот самый "Бетон")
interface Product {
  id: number;
  title: string;
  description: string;
  price: string; // В Django Decimal приходит как строка в JSON
}

// 2. Описываем ответ от Django Ninja (с пагинацией)
interface PaginatedResponse {
  items: Product[];
  count: number;
}

function App() {
  // Указываем, что в стейте будет массив объектов типа Product
  const [products, setProducts] = useState<Product[]>([])

  useEffect(() => {
    // Делаем запрос к твоему Django
    axios.get<PaginatedResponse>('http://localhost:8000/api/core/products')
      .then(res => {
        // Теперь TS знает, что в res.data.items лежат товары!
        setProducts(res.data.items)
      })
      .catch(err => console.error("Error", err))
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>ПАЛУНДРА НАХУЙ 🔥</h1>
      <div style={{ display: 'grid', gap: '10px' }}>
        {products.map(p => (
          <div key={p.id} style={{ border: '1px solid #ccc', padding: '10px', borderRadius: '8px' }}>
            <h3>{p.title}</h3>
            <p>{p.description}</p>
            <p>Цена: <b>{p.price} руб.</b></p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
