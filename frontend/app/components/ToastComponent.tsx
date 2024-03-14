"use client";
import { useTheme } from "next-themes";
import { ToastContainer } from "react-toastify";

export default function ToastComponent() {
  const { theme } = useTheme();
  return (
    <ToastContainer
      position="bottom-right"
      className="text-black dark:text-white"
      theme={theme}
    ></ToastContainer>
  );
}
