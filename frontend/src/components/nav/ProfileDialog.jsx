"use client"

import { useState } from "react"

export function ProfileDialog({ isOpen, onClose, defaultValues }) {
  const [activeTab, setActiveTab] = useState("account")

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-black w-full max-w-md rounded-lg border border-gray-800 p-6 relative">
        <button className="absolute top-4 right-4 text-gray-400 hover:text-white" onClick={onClose}>
          ✕
        </button>

        <div className="text-center mb-6">
          <h2 className="text-xl font-bold text-white">Profile</h2>
          <p className="text-gray-400 text-sm">Make changes to your account here.</p>
        </div>

        <div className="flex justify-center mb-6">
          <div className="w-32 h-32 rounded-full overflow-hidden">
            <img
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Screenshot%20From%202025-03-10%2017-18-04-QYxtVZ53wtiMN8Eq5DphPoDKN6GDkW.png"
              alt="Profile"
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        <div className="mb-4">
          <div className="flex border-b border-gray-800">
            <button
              className={`py-2 px-4 ${
                activeTab === "account" ? "border-b-2 border-[#E97451] text-white" : "text-gray-400"
              }`}
              onClick={() => setActiveTab("account")}
            >
              Account
            </button>
            <button
              className={`py-2 px-4 ${
                activeTab === "password" ? "border-b-2 border-[#E97451] text-white" : "text-gray-400"
              }`}
              onClick={() => setActiveTab("password")}
            >
              Password
            </button>
          </div>
        </div>

        {activeTab === "account" ? (
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-white mb-1">
                Name
              </label>
              <input
                type="text"
                id="name"
                defaultValue={defaultValues?.name}
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#E97451]"
                placeholder="Enter your name"
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-white mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                defaultValue={defaultValues?.email}
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#E97451]"
                placeholder="Enter your email"
              />
            </div>
            <div className="flex items-center justify-between">
              <label className="block text-sm font-medium text-white">Change Theme</label>
              <button className="p-2 text-gray-400 hover:text-white rounded-full bg-gray-800">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label htmlFor="current" className="block text-sm font-medium text-white mb-1">
                Current Password
              </label>
              <input
                type="password"
                id="current"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#E97451]"
                placeholder="Enter current password"
              />
            </div>
            <div>
              <label htmlFor="new" className="block text-sm font-medium text-white mb-1">
                New Password
              </label>
              <input
                type="password"
                id="new"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#E97451]"
                placeholder="Enter new password"
              />
            </div>
            <div>
              <label htmlFor="confirm" className="block text-sm font-medium text-white mb-1">
                Confirm Password
              </label>
              <input
                type="password"
                id="confirm"
                className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#E97451]"
                placeholder="Confirm new password"
              />
            </div>
          </div>
        )}

        <button className="w-full bg-[#E97451] hover:bg-[#d66a48] text-white py-2 rounded-md mt-6">
          Update Profile
        </button>
      </div>
    </div>
  )
}

