import { useState, useMemo } from 'react';

// This is the standard "React way" to build a component.
// We use state to manage dynamic data, which is much safer and cleaner.
const PricingPage = () => {
  // State for the billing toggle (monthly vs. yearly)
  const [isYearly, setIsYearly] = useState(false);
  
  // State for the number of seats in the Team Mates plan
  const [teamSeats, setTeamSeats] = useState(2);

  // Price configuration is stored in a constant object
  const prices = useMemo(() => ({
      mate: { monthly: 9, yearly: (9 * 12 * 0.8) },
      bestMate: { monthly: 29, yearly: (29 * 12 * 0.8) },
      extraSeat: { monthly: 15, yearly: (15 * 12 * 0.8) },
      teamMates: {
          perSeat: { monthly: 25, yearly: (25 * 12 * 0.8) },
          tokensPerSeat: 5000,
          minSeats: 2
      }
  }), []);

  // Helper function to format numbers with commas
  const formatNumber = (num: number) => new Intl.NumberFormat('en-US').format(num);

  // Calculate prices dynamically based on the current state
  const matePrice = isYearly ? prices.mate.yearly : prices.mate.monthly;
  const bestMatePrice = isYearly ? prices.bestMate.yearly : prices.bestMate.monthly;
  const extraSeatPrice = isYearly ? prices.extraSeat.yearly / 12 : prices.extraSeat.monthly;
  const teamMatesPrice = (isYearly ? prices.teamMates.perSeat.yearly / 12 : prices.teamMates.perSeat.monthly) * teamSeats;
  const teamMatesTotalTokens = teamSeats * prices.teamMates.tokensPerSeat;
  const periodText = isYearly ? '/ year' : '/ month';

  return (
    <div className="antialiased">
        <div className="px-4 pt-12 pb-24 sm:px-6 lg:px-8">
            {/* Header & Free Trial Section */}
            <div className="max-w-4xl mx-auto text-center">
                <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
                    Pricing that grows with you
                </h1>
                <p className="mt-6 text-xl text-slate-600">
                    Experience the full power of Vidalytics with a free trial of our Best Mate plan. No credit card required.
                </p>
                <a href="#" className="mt-8 inline-block w-full sm:w-auto bg-teal-500 hover:bg-teal-600 text-white rounded-lg px-10 py-4 text-lg font-bold transition-all duration-300 shadow-lg shadow-teal-500/20 transform hover:scale-105">
                    Start Your 5-Day Free Trial
                </a>
            </div>

            {/* Billing Toggle */}
            <div className="mt-20 flex justify-center items-center space-x-4">
                <span className="text-lg font-medium text-slate-800">Monthly</span>
                <label htmlFor="billing-toggle" className="relative inline-flex items-center cursor-pointer">
                    {/* The input now directly controls the 'isYearly' state */}
                    <input 
                      type="checkbox" 
                      id="billing-toggle" 
                      className="sr-only peer" 
                      checked={isYearly}
                      onChange={(e) => setIsYearly(e.target.checked)}
                    />
                    <div className="w-14 h-8 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-1 after:left-1 after:bg-white after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-teal-500"></div>
                </label>
                <div className="flex items-center">
                    <span className="text-lg font-medium text-slate-800">Yearly</span>
                    <span className="ml-3 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-teal-100 text-teal-800">
                        Save 20%
                    </span>
                </div>
            </div>

            {/* Subscription Tiers */}
            <div className="mt-12 max-w-7xl mx-auto space-y-8 lg:grid lg:grid-cols-3 lg:gap-x-8 lg:space-y-0">
                {/* Mate Plan */}
                <div className="relative flex flex-col bg-white/70 backdrop-blur-sm border border-slate-200/80 rounded-2xl p-8 shadow-sm">
                    <div className="flex-1">
                        <h3 className="text-2xl font-semibold text-slate-900">Mate</h3>
                        <p className="mt-4 text-slate-500">The essentials to get you started and scheduled.</p>
                        <p className="mt-8">
                            {/* Price is now rendered directly from state */}
                            <span className="text-5xl font-extrabold text-slate-900">${Math.round(matePrice)}</span>
                            <span className="text-base font-medium text-slate-500">{periodText}</span>
                        </p>
                        <ul className="mt-8 space-y-5">
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700"><span className="font-semibold text-slate-900">1 Seat</span></p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700">Core Scheduling & Analytics</p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg></div><p className="ml-3 text-base text-slate-500">No monthly AI tokens included</p></li>
                        </ul>
                    </div>
                    <a href="#" className="mt-10 block w-full bg-slate-100 hover:bg-slate-200 text-slate-800 text-center rounded-lg px-6 py-4 text-lg font-semibold transition-colors duration-200">Get Started</a>
                </div>

                {/* Best Mate Plan */}
                <div className="relative flex flex-col bg-white/70 backdrop-blur-sm border-2 border-rose-400 rounded-2xl p-8 shadow-lg shadow-rose-500/10">
                    <div className="absolute top-0 -translate-y-1/2 transform px-4 py-1.5 text-sm font-semibold text-white bg-rose-400 rounded-full">Most Popular</div>
                    <div className="flex-1">
                        <h3 className="text-2xl font-semibold text-slate-900">Best Mate</h3>
                        <p className="mt-4 text-slate-500">The complete toolkit for the professional creator.</p>
                        <p className="mt-8">
                            <span className="text-5xl font-extrabold text-slate-900">${Math.round(bestMatePrice)}</span>
                            <span className="text-base font-medium text-slate-500">{periodText}</span>
                        </p>
                        <ul className="mt-8 space-y-5">
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700"><span className="font-semibold text-slate-900">1 Seat</span> (add more below)</p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700">Advanced Analytics & Reporting</p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700">Priority Support</p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700"><span className="font-semibold text-slate-900">5,000 AI Tokens</span> / month</p></li>
                        </ul>
                    </div>
                    <a href="#" className="mt-10 block w-full bg-teal-500 hover:bg-teal-600 text-white text-center rounded-lg px-6 py-4 text-lg font-semibold transition-all duration-300 shadow-lg shadow-teal-500/20 transform hover:scale-105">Choose Plan</a>
                </div>

                {/* Team Mates Plan */}
                <div className="relative flex flex-col bg-white/70 backdrop-blur-sm border border-slate-200/80 rounded-2xl p-8 shadow-sm">
                    <div className="flex-1">
                        <h3 className="text-2xl font-semibold text-slate-900">Team Mates</h3>
                        <p className="mt-4 text-slate-500">For agencies and collaborative teams.</p>
                        <p className="mt-8">
                            <span className="text-5xl font-extrabold text-slate-900">${formatNumber(Math.round(teamMatesPrice))}</span>
                            <span className="text-base font-medium text-slate-500">{periodText}</span>
                        </p>
                        <p className="mt-1 text-sm text-slate-500">from $25 / seat / month</p>
                        <div className="mt-8">
                            <label htmlFor="seat-count" className="font-semibold text-slate-900">Number of Seats</label>
                            <div className="flex items-center mt-2 seat-selector">
                                {/* Buttons now directly update the 'teamSeats' state */}
                                <button onClick={() => setTeamSeats(prev => Math.max(prices.teamMates.minSeats, prev - 1))} className="p-2 bg-slate-200 hover:bg-slate-300 rounded-md text-slate-800">-</button>
                                <span className="w-16 text-center text-lg font-semibold text-slate-900">{teamSeats}</span>
                                <button onClick={() => setTeamSeats(prev => prev + 1)} className="p-2 bg-slate-200 hover:bg-slate-300 rounded-md text-slate-800">+</button>
                            </div>
                        </div>
                        <ul className="mt-8 space-y-5">
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700"><span className="font-semibold text-slate-900">Minimum {prices.teamMates.minSeats} Seats</span></p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700">Shared Workspaces & Workflows</p></li>
                            <li className="flex items-start"><div className="flex-shrink-0"><svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg></div><p className="ml-3 text-base text-slate-700"><span className="font-semibold text-slate-900">{formatNumber(teamMatesTotalTokens)} AI Tokens</span> (Shared Pool)</p></li>
                        </ul>
                    </div>
                    <a href="#" className="mt-10 block w-full bg-slate-100 hover:bg-slate-200 text-slate-800 text-center rounded-lg px-6 py-4 text-lg font-semibold transition-colors duration-200">Choose Plan</a>
                </div>
            </div>

            {/* À La Carte Add-ons Section */}
            <div className="mt-24 max-w-5xl mx-auto">
                <div className="text-center">
                    <h2 className="text-3xl font-extrabold text-slate-900 sm:text-4xl">Customize Your Plan</h2>
                    <p className="mt-4 text-lg text-slate-600">Flexibly add more power to any plan, anytime.</p>
                </div>
                <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
                    {/* Add Extra Seat */}
                    <div className="lg:col-span-1 flex flex-col text-center bg-white/70 backdrop-blur-sm border border-slate-200/80 rounded-2xl p-8 shadow-sm">
                        <h3 className="text-xl font-semibold text-slate-900">Extra Seat</h3>
                        <div className="mt-2 flex justify-center items-center">
                           <svg className="w-12 h-12 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M15 21v-2a6 6 0 00-12 0v2"></path></svg>
                        </div>
                        <p className="mt-2 text-slate-500">For Best Mate plan</p>
                        <div className="mt-4 text-3xl font-bold text-slate-900">${Math.round(extraSeatPrice)}</div>
                        <p className="text-slate-500">{periodText}</p>
                        <a href="#" className="mt-4 w-full bg-teal-500 hover:bg-teal-600 text-white rounded-lg py-3 text-base font-semibold transition-colors duration-200 shadow-lg shadow-teal-500/20">Add to Plan</a>
                    </div>
                    {/* Token Packs */}
                    <div className="lg:col-span-3 grid grid-cols-1 sm:grid-cols-3 gap-8">
                        <div className="flex flex-col text-center bg-white/70 backdrop-blur-sm border border-slate-200/80 rounded-2xl p-8 shadow-sm"><h3 className="text-xl font-semibold text-slate-900">Starter Pack</h3><p className="mt-2 text-5xl font-bold gradient-text">1,000</p><p className="text-slate-500">AI Tokens</p><div className="mt-6 text-3xl font-bold text-slate-900">$10</div><a href="#" className="mt-4 w-full bg-teal-500 hover:bg-teal-600 text-white rounded-lg py-3 text-base font-semibold transition-colors duration-200 shadow-lg shadow-teal-500/20">Purchase</a></div>
                        <div className="flex flex-col text-center bg-white/70 backdrop-blur-sm border border-slate-200/80 rounded-2xl p-8 shadow-sm"><h3 className="text-xl font-semibold text-slate-900">Value Pack</h3><p className="mt-2 text-5xl font-bold gradient-text">3,000</p><p className="text-slate-500">AI Tokens</p><div className="mt-6 text-3xl font-bold text-slate-900">$25</div><a href="#" className="mt-4 w-full bg-teal-500 hover:bg-teal-600 text-white rounded-lg py-3 text-base font-semibold transition-colors duration-200 shadow-lg shadow-teal-500/20">Purchase</a></div>
                        <div className="flex flex-col text-center bg-white/70 backdrop-blur-sm border border-slate-200/80 rounded-2xl p-8 shadow-sm"><h3 className="text-xl font-semibold text-slate-900">Power Pack</h3><p className="mt-2 text-5xl font-bold gradient-text">10,000</p><p className="text-slate-500">AI Tokens</p><div className="mt-6 text-3xl font-bold text-slate-900">$75</div><a href="#" className="mt-4 w-full bg-teal-500 hover:bg-teal-600 text-white rounded-lg py-3 text-base font-semibold transition-colors duration-200 shadow-lg shadow-teal-500/20">Purchase</a></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
};

export default PricingPage;