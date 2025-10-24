"use client";

import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
	TooltipItem,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { useState, useEffect } from "react";
import { RefreshCw } from "lucide-react";

// Registrasi komponen Chart.js (wajib di Next.js)
ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
);

interface ApiResponse {
	success: boolean;
	message: string;
	data: {
		harvest_data: Array<{
			provinsi: string;
			panen: number;
		}>;
		ksa_data: Array<{
			id: number;
			provinsi: string;
			kabupaten: string;
			bulan: string;
			tahun: number;
			luas_panen: number;
			produksi_beras: number;
			produksi_padi: number;
		}>;
	};
}

export default function LineChart() {
	const [chartData, setChartData] = useState<{
		labels: string[];
		datasets: Array<{
			label: string;
			data: number[];
			borderColor: string;
			backgroundColor: string;
			borderWidth: number;
			pointRadius?: number;
			pointHoverRadius?: number;
			tension?: number;
		}>;
	}>({
		labels: [],
		datasets: [],
	});
	const [isLoading, setIsLoading] = useState(false);

	const fetchData = async () => {
		setIsLoading(true);
		try {
			const response = await fetch(
				"http://localhost:8011/api/charts/harvest-vs-ksa",
			);
			const result: ApiResponse = await response.json();

			if (result.success && result.data) {
				// Get top 10 provinces from harvest data
				const harvestData = result.data.harvest_data.slice(0, 10);
				const labels = harvestData.map((item) => item.provinsi);

				// Create harvest dataset (convert to thousands for better scale)
				const harvestValues = harvestData.map((item) =>
					Math.round(item.panen / 1000),
				);

				// Create KSA dataset by matching provinces and summing produksi_padi (convert to thousands)
				const ksaValues = labels.map((provinsi) => {
					const ksaItems = result.data.ksa_data.filter(
						(item) => item.provinsi === provinsi,
					);
					const total = ksaItems.reduce(
						(sum, item) => sum + item.produksi_padi,
						0,
					);
					return Math.round(total / 1000);
				});

				setChartData({
					labels: labels,
					datasets: [
						{
							label: "Data Panen (ribu ton)",
							data: harvestValues,
							borderColor: "rgba(34, 197, 94, 0.8)",
							backgroundColor: "rgba(34, 197, 94, 0.1)",
							borderWidth: 3,
							pointRadius: 4,
							pointHoverRadius: 6,
							tension: 0.1,
						},
						{
							label: "Produksi Padi KSA (ribu ton)",
							data: ksaValues,
							borderColor: "rgba(59, 130, 246, 0.8)",
							backgroundColor: "rgba(59, 130, 246, 0.1)",
							borderWidth: 3,
							pointRadius: 4,
							pointHoverRadius: 6,
							tension: 0.1,
						},
					],
				});
			}
		} catch (error) {
			console.error("Error fetching data:", error);
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

	// Skeleton component for line chart
	const LineSkeleton = () => (
		<div className="w-full h-full flex flex-col">
			{/* Title skeleton */}
			<div className="text-center mb-2">
				<div className="h-3 w-32 bg-gray-200 rounded animate-pulse mx-auto"></div>
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
				{/* Skeleton line path */}
				<svg className="absolute inset-0 w-full h-full">
					<path
						d="M 10,80 Q 50,60 90,70 T 170,50 T 250,65"
						stroke="#e5e7eb"
						strokeWidth="2"
						fill="none"
						className="animate-pulse"
					/>
					{/* Data points */}
					{[10, 90, 170, 250].map((x, i) => (
						<circle
							key={i}
							cx={x}
							cy={[80, 70, 50, 65][i]}
							r="3"
							fill="#e5e7eb"
							className="animate-pulse"
						/>
					))}
				</svg>
			</div>
			{/* Legend skeleton */}
			<div className="flex justify-center">
				<div className="h-2 w-16 bg-gray-200 rounded animate-pulse"></div>
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
				text: "Perbandingan Panen vs KSA (dalam ribu ton)",
				font: {
					size: 10,
				},
			},
			tooltip: {
				mode: "index" as const,
				intersect: false,
				callbacks: {
					label: function (context: TooltipItem<"line">) {
						const value = context.parsed.y || 0;
						return `${
							context.dataset.label || "Unknown"
						}: ${value.toLocaleString()} ribu ton`;
					},
				},
			},
		},
		interaction: {
			mode: "nearest" as const,
			axis: "x" as const,
			intersect: false,
		},
		scales: {
			x: {
				ticks: {
					display: false,
				},
			},
			y: {
				beginAtZero: true,
				ticks: {
					font: {
						size: 8,
					},
					callback: function (value: string | number) {
						return value + "k";
					},
				},
				grid: {
					display: true,
					color: "rgba(0, 0, 0, 0.1)",
				},
			},
		},
	};

	return (
		<div className="relative flex bg-anti-flash-white-900 backdrop-blur-sm border border-indigo-dye-400/20 rounded-xl h-32.5 justify-center items-center shadow-lg p-1">
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
					<LineSkeleton />
				) : (
					<Line options={options} data={data} />
				)}
			</div>
		</div>
	);
}
