"use client";
import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  Settings,
  Plus,
  Package,
  Truck,
  ShoppingCart,
  Zap,
  Home,
  FileText,
  Users,
  Box,
  Wrench,
  BookOpen,
  Shield,
  Package2,
  Search,
} from "lucide-react";

const data = [
  { name: "Sep 22", value: 1 },
  { name: "Oct 6", value: 3 },
];
import { dynamicMetadata } from "@karrio/core/components/metadata";

export const generateMetadata = dynamicMetadata("Orders");
export const description =
  "A page displaying a list of orders using a data table with sorting, filtering, and status tabs.";

export default function Page() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-semibold">Welcome, Dan</h1>
      </div>

      <div className="mb-8">
        <select className="border rounded-lg px-4 py-2">
          <option>15 days</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard icon={Package} title="Total shipments" value="3" chart />
        <StatCard icon={Truck} title="Total trackers" value="1" chart />
        <StatCard
          icon={ShoppingCart}
          title="Fullfilled orders volume"
          value="$ 0"
          chart
        />
        <StatCard
          icon={FileText}
          title="Estimated shipping spend"
          value="$ 121.85"
          chart
        />
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Things to do next</h2>
        <div className="bg-white p-4 rounded-lg shadow inline-block mb-4">
          <ShoppingCart className="inline mr-2" size={20} />
          <span>3 orders to fulfill</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ActionItem
            icon={Package}
            title="Add shipping location address"
            description="Add one or multiple warehouse locations."
          />
          <ActionItem
            icon={Truck}
            title="Set up carrier accounts"
            description="Connect your carrier accounts to start."
          />
          <ActionItem
            icon={FileText}
            title="Print a test label"
            description="Generate a test label for a sample shipment."
          />
          <ActionItem
            icon={Zap}
            title="Add a tracking number"
            description="Add one or multiple shipments to track."
          />
          <ActionItem
            icon={Wrench}
            title="Set up an API connection"
            description="Retrieve your API key to connect via API."
          />
          <ActionItem
            icon={Shield}
            title="Review your API request"
            description="Audit your API requests logs and system health."
          />
        </div>
      </div>
    </main>
  );
}

const StatCard = ({ icon: Icon, title, value, chart }) => (
  <div className="bg-white p-4 rounded-lg shadow">
    <div className="flex items-center mb-2">
      <Icon className="text-gray-500 mr-2" size={20} />
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
    </div>
    <p className="text-2xl font-semibold mb-4">{value}</p>
    <div className="h-24">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
);

const ActionItem = ({ icon: Icon, title, description }) => (
  <div className="flex items-center justify-between bg-white p-4 rounded-lg shadow mb-4">
    <div className="flex items-center">
      <div className="bg-purple-100 p-2 rounded-lg mr-4">
        <Icon className="text-purple-600" size={24} />
      </div>
      <div>
        <h3 className="font-medium">{title}</h3>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
    </div>
    <div className="text-purple-600">&rarr;</div>
  </div>
);
