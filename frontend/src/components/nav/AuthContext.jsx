"use client"

import { createContext, useContext, useState, useEffect } from "react"

// Create the authentication context
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Check for authentication on initial load
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem("access_token")

      if (token) {
        // Optionally validate token or fetch user data here
        setIsAuthenticated(true)

        // You can fetch user profile data here if needed
        // fetchUserProfile(token).then(userData => setUser(userData))
      } else {
        setIsAuthenticated(false)
        setUser(null)
      }

      setLoading(false)
    }

    checkAuth()
  }, [])

  // Login function
  const login = (tokens, userData = null) => {
    localStorage.setItem("access_token", tokens.access)
    localStorage.setItem("refresh_token", tokens.refresh)
    setIsAuthenticated(true)
    setUser(userData)
  }

  // Logout function
  const logout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    setIsAuthenticated(false)
    setUser(null)
  }

  // Provide the authentication context to children components
  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading }}>{children}</AuthContext.Provider>
  )
}

// Custom hook to use the auth context
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === null) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

