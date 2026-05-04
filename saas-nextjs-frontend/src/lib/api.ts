import axios from "axios";

type Role = "customer" | "owner";
// type подходит для Union(объединений). Одно конкретное значение из множества значений

// interface - Merge(слияние). Если я напишу интерфейс с одним и тем же названием, 
// но с разными значениями, то они объединятся в один
export interface TelegramUser {
    user_id: number,
    role: Role,
    phone_number: string,
    brand_name?: string,
    inn?: string
}

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/core",
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const authApi = {
    // register - это ключ. Я могу вызвать его так: authApi.register
    // (userData: TelegramUser) - аргумент функции
    // => стрелочная функция. Мы как будто передаем значение из параметра в тело функции
    // const { data } - деструктуризация. Чтобы сразу получить нужные нам данные
    register: async (userData: TelegramUser) => {
        // <TelegramUser> нужен для того, чтобы TS знал что ожидать внутри data
        const { data, status } = await api.post<TelegramUser>("/register", userData);
        console.log(status);
        return data;
    }
}