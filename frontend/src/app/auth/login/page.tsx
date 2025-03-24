"use client";

import { useForm } from "react-hook-form";
import { useLogin } from "../../hooks/useAuth";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

export default function Login() {
  const router = useRouter();
  const { register, handleSubmit } = useForm<{ username: string; password: string }>();
  const login = useLogin();

  const onSubmit = (data: { username: string; password: string }) => {
    login.mutate(data, {
      onSuccess: () => {
        toast.success("Login successful! Redirecting...");
        router.push("/dashboard");
      },
      onError: (error) => {
        toast.error(`Login failed: ${(error as any)?.message}`);
      },
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
      <motion.div
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Card className="w-[400px] shadow-xl rounded-2xl">
          <CardHeader>
            <CardTitle className="text-center text-2xl font-semibold text-indigo-600">
              Login to Your Account
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700">Email</label>
                <Input
                  {...register("username")}
                  type="text"
                  placeholder="Enter your email"
                  className="mt-1"
                  required
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700">Password</label>
                <Input
                  {...register("password")}
                  type="password"
                  placeholder="Enter your password"
                  className="mt-1"
                  required
                />
              </div>

              <Button type="submit" className="w-full mt-4" disabled={login.isPending}>
                {login.isPending ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="animate-spin w-4 h-4" /> Logging in...
                  </span>
                ) : (
                  "Login"
                )}
              </Button>
            </form>

            <div className="mt-4 text-center text-sm">
                       
                       <p>
                           Don’t have an account? <a href="/auth/register" className="text-blue-500">Register</a>
                       </p>
                       
            </div>

          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
