"use client"

import { useState, useCallback, useEffect } from "react"
import { ToastContainer } from "./SigninNotification"

export function SignInDialog({ isOpen, onClose, onRegister }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState({})
  const [toasts, setToasts] = useState([])

  const API_URL = import.meta.env.VITE_API_URL

  // Clear toasts when dialog closes
  useEffect(() => {
    if (!isOpen) {
      setToasts([]);
    }
  }, [isOpen]);

  const addToast = useCallback((message, type) => {
    const id = Date.now()
    setToasts((prevToasts) => [...prevToasts, { id, message, type }])
    return id
  }, [])

  const removeToast = useCallback((id) => {
    setToasts((prevToasts) => prevToasts.filter((toast) => toast.id !== id))
  }, [])

  if (!isOpen) return null

  const handleChange = (e) => {
    const { id, value } = e.target
    setFormData({
      ...formData,
      [id]: value,
    })
    
    // Clear error for this field when user starts typing
    if (errors[id]) {
      setErrors({
        ...errors,
        [id]: null
      });
    }
  }

  const validateForm = () => {
    const newErrors = {}

    if (!formData.email) newErrors.email = "Email is required"
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = "Email is invalid"

    if (!formData.password) newErrors.password = "Password is required"

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleLogin = async (e) => {
    e.preventDefault()

    if (!validateForm()) {
      // Show validation errors as toast
      const errorMessages = Object.values(errors).filter(Boolean);
      if (errorMessages.length > 0) {
        addToast(errorMessages.join(". "), "error");
      }
      return;
    }

    setLoading(true)

    try {
      const response = await fetch(`${API_URL}api/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
        credentials: "include", // Include cookies if your API uses session authentication
      })

      const data = await response.json()

      if (!response.ok) {
        // Handle different types of error responses
        if (data.detail) {
          throw new Error(data.detail);
        } else if (data.non_field_errors) {
          throw new Error(data.non_field_errors.join(". "));
        } else if (typeof data === "object" && data !== null) {
          // DRF often returns errors as an object with field names as keys
          const errorMessage = Object.entries(data)
            .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(", ") : value}`)
            .join("; ");
          throw new Error(errorMessage || "Login failed");
        } else {
          throw new Error("Invalid email or password");
        }
      }

      // Store tokens securely
      localStorage.setItem("access_token", data.access)
      localStorage.setItem("refresh_token", data.refresh)

      // Show success toast
      addToast("Successfully signed in!", "success")

      // Close dialog after a short delay
      setTimeout(() => {
        onClose()
        // Refresh to update UI based on authentication
        window.location.reload()
      }, 1500)
    } catch (error) {
      console.error("Login error:", error);
      
      // Show error toast
      addToast(error.message || "Invalid email or password", "error")
      
      // Set field-specific errors if applicable
      if (error.message.toLowerCase().includes("email")) {
        setErrors(prev => ({ ...prev, email: "Invalid email" }));
      }
      if (error.message.toLowerCase().includes("password")) {
        setErrors(prev => ({ ...prev, password: "Invalid password" }));
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-black w-full max-w-md rounded-lg border border-gray-800 p-6">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-white">Sign In</h2>
            <p className="text-gray-400 text-sm mt-1">Enter your credentials to access your account</p>
          </div>

          <form className="space-y-4" onSubmit={handleLogin}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-white mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                className={`w-full px-3 py-2 bg-gray-900 border ${errors.email ? "border-red-500" : "border-gray-700"} rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300`}
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
              />
              {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email}</p>}
            </div>

            <div>
              <div className="flex justify-between">
                <label htmlFor="password" className="block text-sm font-medium text-white mb-1">
                  Password
                </label>
                <a href="#" className="text-sm text-[#E97451] hover:underline">
                  Forgot Password?
                </a>
              </div>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  className={`w-full px-3 py-2 bg-gray-900 border ${errors.password ? "border-red-500" : "border-gray-700"} rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300`}
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                      <path
                        fillRule="evenodd"
                        d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fillRule="evenodd"
                        d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z"
                        clipRule="evenodd"
                      />
                      <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                    </svg>
                  )}
                </button>
              </div>
              {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password}</p>}
            </div>

            <button
              type="submit"
              className="w-full bg-[#E97451] hover:bg-[#d66a48] text-white py-2 rounded-md transition-colors"
              disabled={loading}
            >
              {loading ? "Signing In..." : "Sign In"}
            </button>

            <p className="text-center text-gray-400 text-sm">
              Don't have an account?{" "}
              <button
                type="button"
                className="text-green-400 hover:underline"
                onClick={() => {
                  onClose()
                  onRegister()
                }}
              >
                Sign Up
              </button>
            </p>
          </form>

          <button className="absolute top-4 right-4 text-gray-400 hover:text-white" onClick={onClose}>
            ✕
          </button>
        </div>
      </div>
    </>
  )
}
