"use client"

import { useState, useRef, useEffect } from "react"

const locations = [
  { value: "worldwide", label: "Worldwide" },
  { value: "usa", label: "USA" },
  { value: "uk", label: "UK" },
  { value: "canada", label: "Canada" },
  { value: "australia", label: "Australia" },
  { value: "germany", label: "Germany" },
  { value: "france", label: "France" },
  { value: "spain", label: "Spain" },
  { value: "italy", label: "Italy" },
  { value: "netherlands", label: "Netherlands" },
  { value: "sweden", label: "Sweden" },
  { value: "switzerland", label: "Switzerland" },
  { value: "india", label: "India" },
  { value: "singapore", label: "Singapore" },
  { value: "japan", label: "Japan" },
  { value: "kenya", label: "Kenya" },
]

export function LocationFilter({ selectedLocation, setSelectedLocation }) {
  const [open, setOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const dropdownRef = useRef(null)

  const getLocationLabel = (value) => {
    return locations.find((location) => location.value === value.toLowerCase())?.label || value
  }

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [dropdownRef])

  const filteredLocations = locations.filter((location) =>
    location.label.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <div className="relative w-full" ref={dropdownRef}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between text-white items-center px-4 py-2 text-left border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-orange-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:bg-gray-700"
      >
        {selectedLocation ? getLocationLabel(selectedLocation) : "🌎 Select Location..."}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="ml-2 h-4 w-4 shrink-0 opacity-50"
        >
          <path d="m7 15 5 5 5-5" />
          <path d="m7 9 5-5 5 5" />
        </svg>
      </button>

      {open && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg dark:bg-gray-800 dark:border-gray-700">
          <div className="p-2">
            <input
              type="text"
              placeholder="Search location..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="max-h-64 overflow-y-auto">
            {filteredLocations.length === 0 ? (
              <div className="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">No location found.</div>
            ) : (
              <ul>
                {selectedLocation && (
                  <li
                    className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center text-gray-500 dark:hover:bg-gray-700 dark:text-gray-400"
                    onClick={() => {
                      setSelectedLocation("")
                      setOpen(false)
                    }}
                  >
                    Clear selection
                  </li>
                )}
                {filteredLocations.map((location) => (
                  <li
                    key={location.value}
                    className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center dark:hover:bg-gray-700"
                    onClick={() => {
                      setSelectedLocation(location.value === selectedLocation ? "" : location.value)
                      setOpen(false)
                    }}
                  >
                    <div
                      className={`mr-2 h-4 w-4 flex items-center justify-center ${selectedLocation === location.value ? "text-orange-500" : "text-transparent"}`}
                    >
                      {selectedLocation === location.value && (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </div>
                    {location.label}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

