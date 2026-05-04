import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle2 } from "lucide-react" // Иконка успеха

export const RegisterSuccess = () => {
    return (
        <div className="flex items-center justify-center min-h-100">
            <Card className="w-full max-w-md border-border bg-secondary/20 backdrop-blur-sm">
                <CardHeader className="text-center">
                    <div className="flex justify-center mb-4">
                        {/* Анимированная иконка (по желанию добавишь потом animate-bounce) */}
                        <CheckCircle2 className="w-16 h-16 text-green-500" />
                    </div>
                    <CardTitle className="text-2xl font-bold text-foreground">
                        Регистрация успешна!
                    </CardTitle>
                </CardHeader>
                <CardContent className="text-center text-muted-foreground">
                    Ваш аккаунт создан. Теперь вы можете войти в систему и начать работу с SlyCart.
                </CardContent>
                <CardFooter>
                    <Button
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-6"
                        onClick={() => window.location.href = '/'} // Или редирект через useRouter
                    >
                        На главную
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}
