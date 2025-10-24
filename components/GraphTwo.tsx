"use client";

import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	BarElement,
	Title,
	Tooltip,
	Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { useState, useEffect } from "react";
import { RefreshCw } from "lucide-react";

ChartJS.register(
	CategoryScale,
	LinearScale,
	BarElement,
	Title,
	Tooltip,
	Legend,
);

interface ApiResponse {
	success: boolean;
	message: string;
	data: Array<{
		wilayah: string;
		panen: number;
	}>;
}

export default function BarChart() {
	const [chartData, setChartData] = useState<{
		labels: string[];
		datasets: Array<{
			label: string;
			data: number[];
			backgroundColor: string;
		}>;
	}>({
		labels: [],
		datasets: [
			{
				label: "Panen (ton)",
				data: [],
				backgroundColor: "rgba(34, 197, 94, 0.8)",
			},
		],
	});
	const [isLoading, setIsLoading] = useState(false);

	const fetchData = async () => {
		setIsLoading(true);
		try {
			const response = await fetch(
				"http://localhost:8011/api/charts/harvest-regions",
			);
			const result: ApiResponse = await response.json();

			if (result.success && result.data) {
				// Transform the API data into chart format
				const labels = result.data.map((item) => item.wilayah);
				const data = result.data.map((item) => item.panen);

				setChartData({
					labels: labels,
					datasets: [
						{
							label: "Panen (ton)",
							data: data,
							backgroundColor: "rgba(34, 197, 94, 0.8)",
						},
					],
				});
			}
		} catch (error) {
			console.error("Error fetching data:", error);
			// Fallback to default data if API fails
			setChartData({
				labels: [],
				datasets: [
					{
						label: "Panen (ton)",
						data: [],
						backgroundColor: "rgba(34, 197, 94, 0.8)",
					},
				],
			});
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		fetchData();
	}, []);

	// Skeleton component for bar chart
	const BarSkeleton = () => (
		<div className="w-full h-full flex flex-col">
			{/* Title skeleton */}
			<div className="text-center mb-2">
				<div className="h-3 w-40 bg-gray-200 rounded animate-pulse mx-auto"></div>
			</div>
			{/* Chart area skeleton */}
			<div className="flex-1 relative border-l-2 border-b-2 border-gray-200 ml-8 mb-6">
				{/* Y-axis lines */}
				<div className="absolute left-0 top-0 w-full h-full">
					{[...Array(4)].map((_, i) => (
						<div
							key={i}
							className="absolute left-0 right-0 h-px bg-gray-200 animate-pulse"
							style={{ top: `${(i + 1) * 20}%` }}
						></div>
					))}
				</div>
				{/* Skeleton bars */}
				<div className="absolute bottom-0 left-0 right-0 flex items-end justify-around px-4">
					{[...Array(8)].map((_, i) => (
						<div
							key={i}
							className="bg-gray-200 animate-pulse rounded-t"
							style={{
								width: "8%",
								height: `${Math.random() * 60 + 20}%`,
							}}
						></div>
					))}
				</div>
			</div>
			{/* Legend skeleton */}
			<div className="flex justify-center">
				<div className="h-2 w-24 bg-gray-200 rounded animate-pulse"></div>
			</div>
		</div>
	);

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			legend: {
				position: "bottom" as const,
				labels: {
					font: { size: 8 },
					padding: 8,
					boxWidth: 20,
					boxHeight: 8,
				},
			},
			title: {
				display: true,
				text: "Top 10 Wilayah Panen Terbesar",
				font: { size: 12 },
			},
		},
		scales: {
			x: {
				ticks: {
					font: { size: 8 },
				},
			},
			y: {
				beginAtZero: true,
				ticks: {
					font: { size: 10 },
					stepSize: 50,
				},
			},
		},
	};

	return (
		<div className="relative flex bg-anti-flash-white-900 backdrop-blur-sm border border-indigo-dye-400/20 rounded-xl h-50 justify-center items-center shadow-lg p-1 pt-2">
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
				(chartData.labels.length === 0 &&
					chartData.datasets[0].data.length === 0) ? (
					<BarSkeleton />
				) : (
					<Bar data={chartData} options={options} />
				)}
			</div>
		</div>
	);
}
