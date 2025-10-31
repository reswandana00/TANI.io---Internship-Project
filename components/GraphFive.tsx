"use client";

import React, { useState, useEffect } from "react";
import { RefreshCw } from "lucide-react";

interface TableRow {
	id: number;
	provinsi: string;
	kabupaten: string;
	kecamatan: string;
	perkiraan_panen_september: number;
	perkiraan_panen_oktober: number;
	alsintan_september: number;
	alsintan_oktober: number;
	bera: number;
	penggenangan: number;
	tanam: number;
	vegetatif_1: number;
	vegetatif_2: number;
	max_vegetatif: number;
	generatif_1: number;
	generatif_2: number;
	panen: number;
	standing_crop: number;
	luas_baku_sawah: number;
}

interface ApiResponse {
	success: boolean;
	message: string;
	data: TableRow[];
}

function GraphFive() {
	const [tableData, setTableData] = useState<TableRow[]>([]);
	const [isLoading, setIsLoading] = useState(false);

	const fetchData = async () => {
		setIsLoading(true);
		try {
			const apiUrl =
				process.env.NEXT_PUBLIC_TOOL_API_URL || "http://10.11.1.207:8011";
			const response = await fetch(`${apiUrl}/api/charts/general-data`);
			const result: ApiResponse = await response.json();

			if (result.success && result.data) {
				setTableData(result.data);
			}
		} catch (error) {
			console.error("Error fetching data:", error);
			// Keep empty data if API fails
			setTableData([]);
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		fetchData();
	}, []);

	// Skeleton component for table
	const TableSkeleton = () => (
		<table className="min-w-full text-[0.6rem]">
			<thead className="bg-white border-b border-gray-800 sticky top-0">
				<tr>
					<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
						Provinsi
					</th>
					<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
						Panen Sep
					</th>
					<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
						Panen Okt
					</th>
					<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
						Alsintan
					</th>
					<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
						Tanam
					</th>
					<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap ">
						Panen
					</th>
				</tr>
			</thead>
			<tbody className="bg-white/60 divide-y divide-gray-200">
				{[...Array(7)].map((_, i) => (
					<tr key={i} className="hover:bg-gray-50/50">
						<td className="px-2 py-1 whitespace-nowrap text-gray-900 border-r border-gray-400">
							<div className="h-3 w-4 bg-gray-200 rounded animate-pulse"></div>
						</td>
						<td className="px-2 py-1 whitespace-nowrap text-gray-900 border-r border-gray-400">
							<div className="h-3 w-16 bg-gray-200 rounded animate-pulse"></div>
						</td>
						<td className="px-2 py-1 whitespace-nowrap text-gray-600 border-r border-gray-400">
							<div className="h-3 w-12 bg-gray-200 rounded animate-pulse"></div>
						</td>
						<td className="px-2 py-1 whitespace-nowrap text-gray-900 font-medium border-r border-gray-400">
							<div className="h-3 w-10 bg-gray-200 rounded animate-pulse"></div>
						</td>
						<td className="px-2 py-1 whitespace-nowrap border-r border-gray-400">
							<div className="h-3 w-8 bg-gray-200 rounded animate-pulse"></div>
						</td>
						<td className="px-2 py-1 whitespace-nowrap text-gray-600">
							<div className="h-3 w-12 bg-gray-200 rounded animate-pulse"></div>
						</td>
					</tr>
				))}
			</tbody>
		</table>
	);

	return (
		<div className="relative flex bg-anti-flash-white-900 backdrop-blur-sm border border-indigo-dye-400/20 rounded-xl w-80 h-48 justify-center items-center shadow-lg p-1">
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

			<div className="w-full h-full overflow-x-auto">
				{isLoading || tableData.length === 0 ? (
					<TableSkeleton />
				) : (
					<table className="min-w-full text-[0.6rem]">
						<thead className="bg-white border-b border-gray-800 sticky top-0 shadow-sm">
							<tr>
								<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
									Wilayah
								</th>
								<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
									Panen Sep
								</th>
								<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
									Panen Okt
								</th>
								<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
									Alsintan Okt
								</th>
								<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap border-r border-gray-400">
									Tanam
								</th>
								<th className="px-2 py-1 text-left font-medium text-gray-700 whitespace-nowrap ">
									Panen
								</th>
							</tr>
						</thead>
						<tbody className="bg-white/60 divide-y divide-gray-200">
							{tableData.map((row) => (
								<tr key={row.id} className="hover:bg-gray-50/50">
									<td className="px-2 py-1 whitespace-nowrap text-gray-900 border-r border-gray-400 font-medium">
										{row.provinsi}
									</td>
									<td className="px-2 py-1 whitespace-nowrap text-gray-900 border-r border-gray-400">
										{row.perkiraan_panen_september.toLocaleString()}
									</td>
									<td className="px-2 py-1 whitespace-nowrap text-gray-600 border-r border-gray-400">
										{row.perkiraan_panen_oktober.toLocaleString()}
									</td>
									<td className="px-2 py-1 whitespace-nowrap text-gray-900 border-r border-gray-400">
										{row.alsintan_oktober.toLocaleString()}
									</td>
									<td className="px-2 py-1 whitespace-nowrap border-r border-gray-400">
										<span className="text-blue-700 font-medium">
											{row.tanam.toLocaleString()}
										</span>
									</td>
									<td className="px-2 py-1 whitespace-nowrap text-gray-600">
										<span className="text-green-700 font-medium">
											{row.panen.toLocaleString()}
										</span>
									</td>
								</tr>
							))}
						</tbody>
					</table>
				)}
			</div>
		</div>
	);
}

export default GraphFive;
