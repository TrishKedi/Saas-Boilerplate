"use client";

import { useEffect, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useLogout, useUser } from "../hooks/useAuth";
import { motion } from "framer-motion";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import axios from "axios";

const mockData = [
  { date: "Mon", usage: 12 },
  { date: "Tue", usage: 20 },
  { date: "Wed", usage: 35 },
  { date: "Thu", usage: 28 },
  { date: "Fri", usage: 42 },
];

const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

export default function Dashboard() {
  const router = useRouter();
  const { data: user, isLoading, error } = useUser();

  const TOKEN = localStorage.getItem("token"); // ✅ Get token from localStorage

  console.log("JWT Token:", TOKEN);

  const AUTH_HEADER = {
    headers: {
        Authorization: `Bearer ${TOKEN}`, // ✅ Pass JWT token
      }

  };

  // ✅ Verify Before Making API Call
    if (!TOKEN) {
        console.error("❌ No token found. User is not authenticated.");
        toast.error("Unauthorized: No token found");
    }

  const { mutate: createStripeUser, status: userStatus } = useMutation({
    mutationFn: async () => {
      
  
      if (!TOKEN) {
        throw new Error("Unauthorized: No token found");
      }
  
      const res = await axios.post(`${BASE_URL}/payments/create-customer`, null, AUTH_HEADER);
  
      return res.data;
    },
    onSuccess: () => {
      subscribe();
    },
    onError: (error) => {
      console.error("Failed to create Stripe customer:", error);
      toast.error("Failed to register subscriber");
    },
  });
  

  const { mutate: subscribe, status: subscribStatus } = useMutation({
    mutationFn: async () => {
        const res = await axios.post(`${BASE_URL}/payments/create-checkout-session`, {}, AUTH_HEADER);
       
        return res.data;

    },

    onSuccess: (data) => {
        toast.success(" Redirecting to Checkout")
        window.location.href = data.checkout_url

    },

    onError: (error) => {
        toast.error('Subscription Failed')
    }
  }
    
  )

  const handleLogout = () => {
        useLogout
        router.push("/")
    }

    if(error){
        toast.error("Failed to load user");
    }

  return (

    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-gray-900 p-6">

      <motion.h1
        className="text-4xl font-bold"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Welcome to Your Dashboard
      </motion.h1>

      {isLoading ? (<p>Loading user data</p>) :

      user ?
      (
        <motion.div
          className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Account Info</CardTitle>
            </CardHeader>
            <CardContent>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Subscription:</strong> {user.subscription}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Manage Account</CardTitle>
            </CardHeader>
            <CardContent>
              <Button variant="outline" onClick={() => router.push("/settings")}>Settings</Button>
              <Button variant="destructive" className="ml-4" onClick={handleLogout}>Logout</Button>
              <Button variant="outline" onClick={() => createStripeUser()}>{ subscribStatus === "pending" ? "Processing..." : "Subscribe Now"}</Button>
            </CardContent>
          </Card>
        </motion.div>
      ) : (
        <p className="mt-4">User data Unavailable...</p>
      )}

      <div className="mt-12 w-full max-w-3xl p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">AI Usage Analytics</h2>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={mockData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="usage" stroke="#8884d8" fill="#8884d8" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
