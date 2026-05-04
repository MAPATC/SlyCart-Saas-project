import axios from "axios";
import { components } from "@/types/api";

export type TelegramUserIn = components["schemas"]["TelegramUserIn"]

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
    register: async (userData: TelegramUserIn) => {
        // <TelegramUser> нужен для того, чтобы TS знал что ожидать внутри data
        const { data, status } = await api.post<TelegramUserIn>("/register", userData);
        console.log(status);
        return data;
    }
}