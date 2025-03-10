export function SubscribeAlert({ position }) {
    return (
      <div className="rounded-xl border bg-white shadow-md dark:bg-gray-800 dark:border-gray-700">
        <div className="p-4 sm:p-6">
          <div className="flex gap-4 items-center flex-col md:flex-row justify-center">
            <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0 dark:bg-orange-900/30">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-6 w-6 text-orange-500"
              >
                <rect width="20" height="16" x="2" y="4" rx="2" />
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
              </svg>
            </div>
  
            <div className="flex flex-col gap-2 md:max-w-[500px] w-full">
              <p className="font-semibold">Subscribe to Job Alerts!</p>
              <div className="flex items-center gap-2 flex-wrap">
                <div className="flex items-center">
                  <p className="text-sm mr-4 text-gray-500 dark:text-gray-400">No filters applied</p>
                  <span className="inline-flex items-center rounded-md bg-orange-500 px-2.5 py-0.5 text-xs font-semibold text-white cursor-pointer">
                    Set Filters
                  </span>
                </div>
              </div>
            </div>
  
            <form className="md:ml-auto flex-col md:flex-row flex gap-2 items-center justify-center w-full md:max-w-[500px]">
              <input
                type="email"
                placeholder="Enter your email"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 bg-white text-black dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
              <button
                type="submit"
                className="w-full md:w-auto xl:w-auto px-4 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>
    )
  }
  
  