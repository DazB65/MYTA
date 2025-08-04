"use client";

import Image from "next/image";
import React, { useState } from "react";

interface FormData {
  name: string;
  niche: string;
  contentType: string;
  uploadFrequency: string;
  videoLength: string;
  monetisationStatus: string;
  primaryGoal: string;
  additionalNotes: string;
}

export default function CreateProfilePage() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    niche: "",
    contentType: "",
    uploadFrequency: "",
    videoLength: "",
    monetisationStatus: "",
    primaryGoal: "",
    additionalNotes: "",
  });

  const [errors, setErrors] = useState<Partial<FormData>>({});

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormData]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const validateForm = () => {
    const newErrors: Partial<FormData> = {};
    if (!formData.name.trim()) newErrors.name = "Name is required";
    if (!formData.niche) newErrors.niche = "Niche is required";
    if (!formData.contentType)
      newErrors.contentType = "Content type is required";
    if (!formData.uploadFrequency)
      newErrors.uploadFrequency = "Upload frequency is required";
    if (!formData.videoLength)
      newErrors.videoLength = "Video length is required";
    if (!formData.monetisationStatus)
      newErrors.monetisationStatus = "Monetisation status is required";
    if (!formData.primaryGoal)
      newErrors.primaryGoal = "Primary goal is required";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      console.log("Form submitted:", formData);
      // Handle form submission logic here
    }
  };

  const handleConnectYoutube = () => {
    // Handle YouTube connection logic here
    console.log("Connect YouTube account");
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4"
      style={{ backgroundColor: "#2d3748" }}
    >
      <div className="w-full max-w-6xl bg-white rounded-3xl shadow-2xl flex flex-col lg:flex-row overflow-hidden">
        {/* Left: Form Section */}
        <div className="flex-1 p-6 sm:p-8 lg:p-12 flex flex-col justify-center">
          {/* Back Button */}
          <button className="flex items-center text-gray-500 mb-6 hover:text-gray-700 w-fit transition-colors">
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 18l-6-6 6-6"
              />
            </svg>
            Back
          </button>

          {/* Header */}
          <div className="mb-8">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-2">
              Welcome to{" "}
              <span className="inline-flex items-center font-bold text-[#7C3AED]">
                ✨Vidalytics
              </span>
            </h1>
            <p className="text-gray-600 text-sm sm:text-base lg:text-lg">
              Let&apos;s set up your channel profile to get personalised AI
              assistance
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Name Field */}
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                What should I call you? <span className="text-pink-500">*</span>
              </label>
              <input
                type="text"
                id="name"
                name="name"
                className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.name ? "border-red-400" : "border-gray-300"}`}
                placeholder="Enter your name or how you'd like to be called"
                value={formData.name}
                onChange={handleInputChange}
              />
              {errors.name && (
                <span className="text-xs text-red-500 mt-1 block">
                  {errors.name}
                </span>
              )}
            </div>

            {/* Row 1: Niche and Content Type */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="niche"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Niche <span className="text-pink-500">*</span>
                </label>
                <select
                  id="niche"
                  name="niche"
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.niche ? "border-red-400" : "border-gray-300"}`}
                  value={formData.niche}
                  onChange={handleInputChange}
                >
                  <option value="">Select</option>
                  <option value="gaming">Gaming</option>
                  <option value="tech">Technology</option>
                  <option value="lifestyle">Lifestyle</option>
                  <option value="education">Education</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="business">Business</option>
                  <option value="fitness">Fitness & Health</option>
                  <option value="other">Other</option>
                </select>
                {errors.niche && (
                  <span className="text-xs text-red-500 mt-1 block">
                    {errors.niche}
                  </span>
                )}
              </div>
              <div>
                <label
                  htmlFor="contentType"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Content Type <span className="text-pink-500">*</span>
                </label>
                <select
                  id="contentType"
                  name="contentType"
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.contentType ? "border-red-400" : "border-gray-300"}`}
                  value={formData.contentType}
                  onChange={handleInputChange}
                >
                  <option value="">Select</option>
                  <option value="tutorials">Tutorials</option>
                  <option value="reviews">Reviews</option>
                  <option value="vlogs">Vlogs</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="educational">Educational</option>
                  <option value="live-streams">Live Streams</option>
                  <option value="shorts">YouTube Shorts</option>
                  <option value="other">Other</option>
                </select>
                {errors.contentType && (
                  <span className="text-xs text-red-500 mt-1 block">
                    {errors.contentType}
                  </span>
                )}
              </div>
            </div>

            {/* Row 2: Upload Frequency and Video Length */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="uploadFrequency"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Upload Frequency <span className="text-pink-500">*</span>
                </label>
                <select
                  id="uploadFrequency"
                  name="uploadFrequency"
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.uploadFrequency ? "border-red-400" : "border-gray-300"}`}
                  value={formData.uploadFrequency}
                  onChange={handleInputChange}
                >
                  <option value="">Select</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="bi-weekly">Bi-weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="irregular">Irregular</option>
                </select>
                {errors.uploadFrequency && (
                  <span className="text-xs text-red-500 mt-1 block">
                    {errors.uploadFrequency}
                  </span>
                )}
              </div>
              <div>
                <label
                  htmlFor="videoLength"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Typical Video Length <span className="text-pink-500">*</span>
                </label>
                <select
                  id="videoLength"
                  name="videoLength"
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.videoLength ? "border-red-400" : "border-gray-300"}`}
                  value={formData.videoLength}
                  onChange={handleInputChange}
                >
                  <option value="">Select</option>
                  <option value="shorts">Shorts (&lt;1 min)</option>
                  <option value="short">Short (1-5 min)</option>
                  <option value="medium">Medium (5-15 min)</option>
                  <option value="long">Long (15-30 min)</option>
                  <option value="very-long">Very Long (30+ min)</option>
                </select>
                {errors.videoLength && (
                  <span className="text-xs text-red-500 mt-1 block">
                    {errors.videoLength}
                  </span>
                )}
              </div>
            </div>

            {/* Row 3: Monetisation Status and Primary Goal */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="monetisationStatus"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Monetisation Status <span className="text-pink-500">*</span>
                </label>
                <select
                  id="monetisationStatus"
                  name="monetisationStatus"
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.monetisationStatus ? "border-red-400" : "border-gray-300"}`}
                  value={formData.monetisationStatus}
                  onChange={handleInputChange}
                >
                  <option value="">Select</option>
                  <option value="not-monetized">Not Monetized</option>
                  <option value="applying">Applying for Monetization</option>
                  <option value="monetized">Monetized</option>
                  <option value="partner">YouTube Partner</option>
                </select>
                {errors.monetisationStatus && (
                  <span className="text-xs text-red-500 mt-1 block">
                    {errors.monetisationStatus}
                  </span>
                )}
              </div>
              <div>
                <label
                  htmlFor="primaryGoal"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Primary Goal <span className="text-pink-500">*</span>
                </label>
                <select
                  id="primaryGoal"
                  name="primaryGoal"
                  className={`w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 ${errors.primaryGoal ? "border-red-400" : "border-gray-300"}`}
                  value={formData.primaryGoal}
                  onChange={handleInputChange}
                >
                  <option value="">Select</option>
                  <option value="subscribers">Grow Subscribers</option>
                  <option value="views">Increase Views</option>
                  <option value="engagement">Boost Engagement</option>
                  <option value="monetization">Maximize Revenue</option>
                  <option value="brand">Build Brand</option>
                  <option value="education">Educate Audience</option>
                  <option value="entertainment">Entertain Audience</option>
                </select>
                {errors.primaryGoal && (
                  <span className="text-xs text-red-500 mt-1 block">
                    {errors.primaryGoal}
                  </span>
                )}
              </div>
            </div>

            {/* Additional Notes */}
            <div>
              <label
                htmlFor="additionalNotes"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Additional Notes
              </label>
              <textarea
                id="additionalNotes"
                name="additionalNotes"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#7C3AED] focus:border-transparent transition-all duration-200 resize-none"
                placeholder="Write your note here"
                rows={3}
                value={formData.additionalNotes}
                onChange={handleInputChange}
              />
            </div>

            {/* YouTube Connection Section */}
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 text-center">
              <h2 className="font-semibold text-gray-800 text-lg mb-2">
                Connect Your YouTube Channel
              </h2>
              <p className="text-sm text-gray-500 mb-4">
                Connect your YouTube account to automatically import your
                channel statistics
              </p>
              <button
                type="button"
                onClick={handleConnectYoutube}
                className="flex items-center justify-center gap-2 bg-white border border-red-400 text-red-500 font-semibold px-6 py-3 rounded-lg shadow-sm hover:bg-red-50 transition-colors mx-auto mb-2"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M21.8 8.001c-.2-.801-.8-1.401-1.601-1.601C18.2 6 12 6 12 6s-6.2 0-8.2.4c-.8.2-1.4.8-1.6 1.601C2 10 2 12 2 12s0 2 .2 3.999c.2.801.8 1.401 1.6 1.601C5.8 18 12 18 12 18s6.2 0 8.2-.4c.8-.2 1.4-.8 1.6-1.601C22 14 22 12 22 12s0-2-.2-3.999zM10 15.5v-7l6 3.5-6 3.5z" />
                </svg>
                Connect YouTube Account
              </button>
              <p className="text-xs text-gray-400">
                Optional: You can connect later from Settings
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white font-bold py-4 rounded-xl shadow-lg hover:from-pink-600 hover:to-purple-600 transition-all duration-200 text-lg"
            >
              Complete Setup
            </button>
          </form>
        </div>

        {/* Right Side: Robot Image Section */}
        <div
          className="w-1/2 relative rounded-r-2xl overflow-hidden flex flex-col"
          style={{
            background: "linear-gradient(135deg, #0f172a 0%, #020617 100%)",
          }}
        >
          {/* Main Robot - Top Half */}
          <div className="flex-1 relative">
            <Image
              src="/BossAgent.png"
              alt="Friendly robot assistant with analytics charts"
              width={900}
              height={900}
              className="absolute inset-0 w-full h-full object-cover"
            />
          </div>

          {/* Other Agents - Bottom Half */}
          <div className="flex-1 relative flex flex-col justify-between p-6">
            {/* Text - positioned high up, just under Boss Agent */}
            <div className="flex-1 flex items-start justify-center pt-4">
              <h3
                className="text-white font-bold text-center leading-tight"
                style={{ fontSize: "4rem", lineHeight: "1.1" }}
              >
                Meet Boss Agent and his Agentic Workers
              </h3>
            </div>

            {/* Agent Avatars - stay at the bottom */}
            <div className="flex space-x-3 opacity-90 justify-center">
              <Image
                src="/Agent1.png"
                alt="Agent 1"
                width={100}
                height={100}
                className="rounded-full border-2 border-white/30 hover:scale-105 transition-transform"
              />
              <Image
                src="/Agent2.png"
                alt="Agent 2"
                width={100}
                height={100}
                className="rounded-full border-2 border-white/30 hover:scale-105 transition-transform"
              />
              <Image
                src="/Agent3.png"
                alt="Agent 3"
                width={100}
                height={100}
                className="rounded-full border-2 border-white/30 hover:scale-105 transition-transform"
              />
              <Image
                src="/Agent4.png"
                alt="Agent 4"
                width={100}
                height={100}
                className="rounded-full border-2 border-white/30 hover:scale-105 transition-transform"
              />
              <Image
                src="/Agent5.png"
                alt="Agent 5"
                width={100}
                height={100}
                className="rounded-full border-2 border-white/30 hover:scale-105 transition-transform"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
