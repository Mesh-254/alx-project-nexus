"use client"

import { useState } from "react"
import { useAuth } from "./AuthContext"

export function Navbar({ onSignIn, onRegister, onProfile }) {
  const [isOpen, setIsOpen] = useState(false)
  const { isAuthenticated, logout } = useAuth()

  const handleSignOut = () => {
    logout()
    // You can add a toast notification here if needed
    window.location.reload() // Optional: reload the page
  }

  return (
    <nav className="bg-[#1A1A1A] border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex-shrink-0 flex items-center">
            <a href="/" className="flex items-center space-x-2">
              <img src="/placeholder.svg" alt="RJ" className="w-8 h-8" />
              <span className="text-green-400 font-bold text-3xl">RealtimeJobs</span>
            </a>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex md:items-center md:space-x-6">
            <a
              href="/post-job"
              className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-m font-medium transition-colors"
            >
              Post a Job
            </a>

            {isAuthenticated ? (
              <>
                <button
                  className="bg-gray-800 text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium"
                  onClick={onProfile}
                >
                  Profile
                </button>
                <button
                  className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-medium"
                  onClick={handleSignOut}
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <button
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  onClick={onSignIn}
                >
                  Sign In
                </button>
                <button
                  className="bg-[#E97451] hover:bg-[#d66a48] text-white px-4 py-2 rounded-md text-sm font-medium"
                  onClick={onRegister}
                >
                  Register
                </button>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden">
            <button className="text-gray-300 hover:text-white p-2" onClick={() => setIsOpen(!isOpen)}>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <a
                href="/post-job"
                className="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
              >
                Post a Job
              </a>

              {isAuthenticated ? (
                <>
                  <button
                    className="w-full text-left bg-gray-800 text-white hover:bg-gray-700 px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => {
                      onProfile()
                      setIsOpen(false)
                    }}
                  >
                    Profile
                  </button>
                  <button
                    className="w-full text-left bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => {
                      handleSignOut()
                      setIsOpen(false)
                    }}
                  >
                    Sign Out
                  </button>
                </>
              ) : (
                <>
                  <button
                    className="w-full text-left text-gray-300 hover:text-white px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => {
                      onSignIn()
                      setIsOpen(false)
                    }}
                  >
                    Sign In
                  </button>
                  <button
                    className="w-full text-left bg-[#E97451] hover:bg-[#d66a48] text-white px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => {
                      onRegister()
                      setIsOpen(false)
                    }}
                  >
                    Register
                  </button>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

