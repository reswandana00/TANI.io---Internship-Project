"use client";

import {
	Chart as ChartJS,
	ArcElement,
	Tooltip,
	Legend,
	Title,
	TooltipItem,
} from "chart.js";
import { Pie } from "react-chartjs-2";
import { useState, useEffect } from "react";
import { RefreshCw } from "lucide-react";

// Registrasi komponen Chart.js
ChartJS.register(ArcElement, Tooltip, Legend, Title);

interface ApiResponse {
	success: boolean;
	message: string;
	data: Array<{
		wilayah: string;
		efektivitas_hasil: number;
	}>;
}

export default function PolarChart() {
	const [chartData, setChartData] = useState<{
		labels: string[];
		datasets: Array<{
			label: string;
			data: number[];
			backgroundColor: string[];
			borderColor: string[];
			borderWidth: number;
		}>;
	}>({
		labels: [],
		datasets: [],
	});
	const [isLoading, setIsLoading] = useState(false);

	const fetchData = async () => {
		setIsLoading(true);
		try {
			const apiUrl =
				process.env.NEXT_PUBLIC_TOOL_API_URL || "http://10.11.1.207:8011";
			const response = await fetch(
				`${apiUrl}/api/charts/machinery-effectiveness`,
				{
					method: "GET",
					headers: {
						Accept: "application/json",
						"Content-Type": "application/json",
					},
				},
			);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const result: ApiResponse = await response.json();

			if (result.success && result.data) {
				// Transform API data into pie chart format
				const labels = result.data.map((item) => item.wilayah);
				const data = result.data.map(
					(item) => Math.round(item.efektivitas_hasil * 100) / 100,
				); // Round to 2 decimal places

				// Generate soft/muted colors for pie segments
				const colors = [
					"rgba(34, 197, 94, 0.6)", // soft green
					"rgba(59, 130, 246, 0.6)", // soft blue
					"rgba(245, 158, 11, 0.6)", // soft amber
					"rgba(239, 68, 68, 0.6)", // soft red
					"rgba(139, 92, 246, 0.6)", // soft violet
					"rgba(249, 115, 22, 0.6)", // soft orange
					"rgba(6, 182, 212, 0.6)", // soft cyan
					"rgba(132, 204, 22, 0.6)", // soft lime
					"rgba(236, 72, 153, 0.6)", // soft pink
					"rgba(99, 102, 241, 0.6)", // soft indigo
				];

				const borderColors = [
					"rgba(34, 197, 94, 0.8)", // slightly more opaque borders
					"rgba(59, 130, 246, 0.8)",
					"rgba(245, 158, 11, 0.8)",
					"rgba(239, 68, 68, 0.8)",
					"rgba(139, 92, 246, 0.8)",
					"rgba(249, 115, 22, 0.8)",
					"rgba(6, 182, 212, 0.8)",
					"rgba(132, 204, 22, 0.8)",
					"rgba(236, 72, 153, 0.8)",
					"rgba(99, 102, 241, 0.8)",
				];

				setChartData({
					labels: labels,
					datasets: [
						{
							label: "Efektivitas (%)",
							data: data,
							backgroundColor: colors.slice(0, data.length),
							borderColor: borderColors.slice(0, data.length),
							borderWidth: 1,
						},
					],
				});
			} else {
				console.error("GraphFour: API returned unsuccessful or no data");
			}
		} catch (error) {
			console.error("GraphFour: Error fetching data:", error);
			// Keep empty data if API fails
			setChartData({
				labels: [],
				datasets: [],
			});
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		fetchData();
	}, []);

	const data = chartData;

	// Skeleton component for pie chart
	const PieSkeleton = () => (
		<div className="w-full h-full flex items-center">
			{/* Left side - Title */}
			<div className="flex-shrink-0 w-16">
				<div className="h-3 w-12 bg-gray-200 rounded animate-pulse"></div>
			</div>
			{/* Center - Pie chart skeleton */}
			<div className="flex-1 flex justify-center">
				<div className="relative w-32 h-32">
					{/* Pie segments skeleton */}
					<div className="absolute inset-0 border-4 border-gray-200 rounded-full animate-pulse"></div>
					<div className="absolute inset-2 border-2 border-gray-300 rounded-full animate-pulse"></div>
					<div className="absolute inset-4 border border-gray-200 rounded-full animate-pulse"></div>
					{/* Center dot */}
					<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-gray-200 rounded-full animate-pulse"></div>
				</div>
			</div>
			{/* Right side - Legend */}
			<div className="flex-shrink-0 w-20 space-y-1">
				{[...Array(6)].map((_, i) => (
					<div key={i} className="flex items-center space-x-1">
						<div className="w-2 h-2 bg-gray-200 rounded animate-pulse"></div>
						<div className="h-1.5 w-12 bg-gray-200 rounded animate-pulse"></div>
					</div>
				))}
			</div>
		</div>
	);

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			title: {
				position: "left" as const,
				display: true,
				text: "Efektivitas pemanfaatan Alsintan",
				font: { size: 12 },
			},
			legend: {
				position: "right" as const,
				labels: {
					font: { size: 8 },
					padding: 8,
					boxWidth: 8,
					boxHeight: 8,
				},
			},
			tooltip: {
				callbacks: {
					label: function (context: TooltipItem<"pie">) {
						return `${context.label}: ${context.parsed}%`;
					},
				},
			},
		},
	};

	return (
		<div className="relative flex bg-anti-flash-white-900 backdrop-blur-sm border border-indigo-dye-400/20 rounded-xl w-80 h-48 justify-center items-center shadow-lg p-3">
			{/* Refresh Button */}
			<button
				onClick={fetchData}
				disabled={isLoading}
				className="absolute top-2 right-2 p-1.5 bg-white hover:bg-gray-50 rounded-full cursor-pointer shadow-sm border border-gray-200 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed z-10"
				title="Refresh data"
			>
				<RefreshCw
					size={10}
					className={`text-gray-600 ${isLoading ? "animate-spin" : ""}`}
				/>
			</button>

			<div className="w-full h-full">
				{isLoading ||
				(chartData.labels.length === 0 && chartData.datasets.length === 0) ? (
					<PieSkeleton />
				) : (
					<Pie data={data} options={options} />
				)}
			</div>
		</div>
	);
}
