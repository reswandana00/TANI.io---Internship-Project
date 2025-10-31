"use client";

import {
	Chart as ChartJS,
	RadialLinearScale,
	PointElement,
	LineElement,
	Filler,
	Tooltip,
	Legend,
	Title,
} from "chart.js";
import { Radar } from "react-chartjs-2";
import { useState, useEffect } from "react";
import { RefreshCw } from "lucide-react";

// Registrasi komponen Chart.js
ChartJS.register(
	RadialLinearScale,
	PointElement,
	LineElement,
	Filler,
	Tooltip,
	Legend,
	Title,
);

interface ClimateData {
	tempat: string;
	curah_hujan: number;
	suhu: number;
	kelembaban: number;
	lama_penyinaran: number;
}

interface ApiResponse {
	success: boolean;
	message: string;
	data: {
		labels: string[];
		datasets: Array<{
			label: string;
			data: number[];
			backgroundColor: string;
			borderColor: string;
			borderWidth: number;
		}>;
	};
}

export default function RadarChart() {
	const [chartData, setChartData] = useState<{
		labels: string[];
		datasets: Array<{
			label: string;
			data: number[];
			backgroundColor: string;
			borderColor: string;
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
			const response = await fetch(`${apiUrl}/api/charts/climate`);
			const result = await response.json();

			if (result.success && Array.isArray(result.data)) {
				const data: ClimateData[] = result.data;

				// Transform the API data to match the chart.js format
				const labels = data.map((item) => item.tempat);
				const datasets = [
					{
						label: "Curah Hujan (mm)",
						data: data.map((item) => item.curah_hujan),
						backgroundColor: "rgba(54, 162, 235, 0.2)",
						borderColor: "rgba(54, 162, 235, 1)",
						borderWidth: 1,
					},
					{
						label: "Kelembaban (%)",
						data: data.map((item) => item.kelembaban),
						backgroundColor: "rgba(75, 192, 192, 0.2)",
						borderColor: "rgba(75, 192, 192, 1)",
						borderWidth: 1,
					},
					{
						label: "Suhu (°C)",
						data: data.map((item) => item.suhu),
						backgroundColor: "rgba(255, 99, 132, 0.2)",
						borderColor: "rgba(255, 99, 132, 1)",
						borderWidth: 1,
					},
					{
						label: "Lama Penyinaran (jam)",
						data: data.map((item) => item.lama_penyinaran),
						backgroundColor: "rgba(153, 102, 255, 0.2)",
						borderColor: "rgba(153, 102, 255, 1)",
						borderWidth: 1,
					},
				];

				setChartData({ labels, datasets });
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

	// Skeleton component for radar chart
	const RadarSkeleton = () => (
		<div className="w-full h-full flex flex-col items-center justify-center">
			<div className="w-48 h-48 relative">
				{/* Outer circle */}
				<div className="absolute inset-0 border-2 border-gray-200 rounded-full animate-pulse"></div>
				{/* Middle circle */}
				<div className="absolute inset-6 border border-gray-200 rounded-full animate-pulse"></div>
				{/* Inner circle */}
				<div className="absolute inset-12 border border-gray-200 rounded-full animate-pulse"></div>
				{/* Grid lines */}
				<div className="absolute top-1/2 left-0 right-0 h-px bg-gray-200 animate-pulse"></div>
				<div className="absolute top-0 bottom-0 left-1/2 w-px bg-gray-200 animate-pulse"></div>
				{/* Diagonal lines */}
				<div className="absolute top-2 bottom-2 left-2 right-2 border border-gray-200 rounded-full animate-pulse opacity-50"></div>
			</div>
			<div className="mt-4 flex gap-4">
				<div className="h-2 w-16 bg-gray-200 rounded animate-pulse"></div>
				<div className="h-2 w-16 bg-gray-200 rounded animate-pulse"></div>
			</div>
		</div>
	);

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			title: {
				display: true,
				text: "Iklim di Beberapa Tempat",
				font: { size: 12 },
			},
			legend: {
				position: "bottom" as const,
				labels: {
					font: { size: 8 },
					padding: 8,
					boxWidth: 20,
					boxHeight: 8,
				},
			},
		},
		scales: {
			r: {
				angleLines: { color: "#e5e7eb" },
				grid: { color: "#e5e7eb" },
				suggestedMin: 0,
				suggestedMax: 100,
				pointLabels: {
					font: { size: 10 },
				},
				ticks: {
					font: { size: 8 },
				},
			},
		},
	};

	return (
		<div className="relative flex bg-anti-flash-white-900 backdrop-blur-sm border border-indigo-dye-400/20 rounded-xl w-80 h-84.5 justify-center items-center shadow-lg p-4">
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
					<RadarSkeleton />
				) : (
					<Radar data={data} options={options} />
				)}
			</div>
		</div>
	);
}
