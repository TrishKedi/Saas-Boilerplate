import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { loginUser, registerUser, getCurrentUser } from "../services/auth";
import { useState } from "react";
import axios from "axios";
import { access } from "fs";

// export function useLogin() {
//   const queryClient = useQueryClient();
//   return useMutation({
//     mutationFn: loginUser,
//     onSuccess: (data) => {
//       localStorage.setItem("token", data.access_token);
//       queryClient.invalidateQueries({ queryKey: ["user"] });
//     },
//   });
// }

export function useLogin() {
    const queryClient = useQueryClient();
    return useMutation({
      mutationFn: loginUser,
      onSuccess: (data) => {
        console.log(data.access_token);
        localStorage.setItem('token', data.access_token);
        queryClient.invalidateQueries({ queryKey: ["user"]})
      }
    });
  }

export function useRegister() {
  return useMutation({
    mutationFn: registerUser,
  });
}

export function useUser() {
    const access_token = localStorage.getItem("token")
  return useQuery({
    queryKey: ["user"],
    queryFn: () => getCurrentUser(access_token),
    retry: false,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  return () => {
    localStorage.removeItem("token");
    queryClient.invalidateQueries({ queryKey: ["user"] });
  };
}
