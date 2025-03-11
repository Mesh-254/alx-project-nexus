"use client";

import { useState, useCallback } from "react";
import { ToastContainer } from "./ToastNotification";

export function RegisterDialog({ isOpen, onClose, onSignIn }) {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [toasts, setToasts] = useState([]);
  const API_URL = import.meta.env.VITE_API_URL;

  const addToast = useCallback((message, type) => {
    const id = Date.now();
    setToasts((prevToasts) => [...prevToasts, { id, message, type }]);
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prevToasts) => prevToasts.filter((toast) => toast.id !== id));
  }, []);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { id, value } = e.target;
    // Map the form field IDs to the backend expected field names
    const fieldMapping = {
      name: "full_name",
      email: "email",
      password: "password",
      confirmPassword: "confirm_password",
    };

    setFormData({
      ...formData,
      [fieldMapping[id] || id]: value,
    });
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.full_name) newErrors.full_name = "Name is required";
    if (!formData.email) newErrors.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(formData.email))
      newErrors.email = "Email is invalid";

    if (!formData.password) newErrors.password = "Password is required";
    else if (formData.password.length < 6)
      newErrors.password = "Password must be at least 6 characters";

    if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = "Passwords must match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError("");

    if (!validateForm()) return;

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}signup/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
        credentials: "include", // Include cookies if your API uses session authentication
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle different types of error responses from DRF
        if (typeof data === "object" && data !== null) {
          // DRF often returns errors as an object with field names as keys
          const errorMessage = Object.entries(data)
            .map(
              ([key, value]) =>
                `${key}: ${Array.isArray(value) ? value.join(", ") : value}`
            )
            .join("; ");
          throw new Error(errorMessage || "Registration failed");
        } else {
          throw new Error(data.message || "Registration failed");
        }
      }

      // Show success toast instead of alert
      addToast("Account created successfully!", "success");

      // Close the register dialog and open sign in
      setTimeout(() => {
        onClose();
        onSignIn();
      }, 1500); // Give user time to see the success message
    } catch (error) {
      setApiError(error.message || "Something went wrong. Please try again.");
      // Show error toast
      addToast(error.message || "Registration failed", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-40">
        <div className="bg-black w-full max-w-md rounded-lg border border-gray-800 p-6">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-white">Sign Up</h2>
            <p className="text-gray-400 text-sm mt-1">
              Create your account to get started
            </p>
          </div>

          {apiError && (
            <div className="bg-red-900 bg-opacity-50 border border-red-500 text-red-200 px-4 py-2 rounded-md mb-4">
              {apiError}
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-white mb-1"
              >
                Name
              </label>
              <input
                type="text"
                id="name"
                className={`w-full px-3 py-2 bg-gray-900 border ${
                  errors.full_name ? "border-red-500" : "border-gray-700"
                } rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300`}
                placeholder="Your name"
                onChange={handleChange}
              />
              {errors.full_name && (
                <p className="text-red-500 text-xs mt-1">{errors.full_name}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-white mb-1"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                className={`w-full px-3 py-2 bg-gray-900 border ${
                  errors.email ? "border-red-500" : "border-gray-700"
                } rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300`}
                placeholder="your-email@example.com"
                onChange={handleChange}
              />
              {errors.email && (
                <p className="text-red-500 text-xs mt-1">{errors.email}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-white mb-1"
              >
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  className={`w-full px-3 py-2 bg-gray-900 border ${
                    errors.password ? "border-red-500" : "border-gray-700"
                  } rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300`}
                  placeholder="Your password"
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-4 w-4"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                      <path
                        fillRule="evenodd"
                        d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  ) : (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-4 w-4"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
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
              {errors.password && (
                <p className="text-red-500 text-xs mt-1">{errors.password}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-medium text-white mb-1"
              >
                Confirm Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="confirmPassword"
                  className={`w-full px-3 py-2 bg-gray-900 border ${
                    errors.confirm_password
                      ? "border-red-500"
                      : "border-gray-700"
                  } rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-300`}
                  placeholder="Confirm your password"
                  onChange={handleChange}
                />
              </div>
              {errors.confirm_password && (
                <p className="text-red-500 text-xs mt-1">
                  {errors.confirm_password}
                </p>
              )}
            </div>

            <button
              type="submit"
              className="w-full bg-[#E97451] hover:bg-[#d66a48] text-white py-2 rounded-md transition-colors"
              disabled={loading}
            >
              {loading ? "Signing Up..." : "Sign Up"}
            </button>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-800 mb-10"></div>
              </div>
            </div>

            <p className="text-center text-gray-400 text-sm">
              Already have an account?{" "}
              <button
                type="button"
                className="text-green-400 hover:underline"
                onClick={() => {
                  onClose();
                  onSignIn();
                }}
              >
                Sign In
              </button>
            </p>
          </form>

          <button
            className="absolute top-4 right-4 text-gray-400 hover:text-white"
            onClick={onClose}
          >
            ✕
          </button>
        </div>
      </div>
    </>
  );
}
