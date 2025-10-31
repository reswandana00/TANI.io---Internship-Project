"use client";

import React, { useState, useEffect } from "react";

interface ApiResponse {
	success: boolean;
	data: {
		nasional?: string;
		provinsi?: string;
		kabupaten?: string;
		kota?: string;
		kecamatan?: string;
		parent: string | null;
	};
	message: string;
}

function State({ region }: { region?: string }) {
	const [nasional, setNasional] = useState<string | null>(null);
	const [provinsi, setProvinsi] = useState<string | null>(null);
	const [kabupaten, setKabupaten] = useState<string | null>(null);
	const [kota, setKota] = useState<string | null>(null);
	const [kecamatan, setKecamatan] = useState<string | null>(null);
	const [parentLocation, setParentLocation] = useState<string | null>(null);
	const [isLoading, setIsLoading] = useState(false);

	const fetchParentData = async () => {
		setIsLoading(true);
		try {
			const apiUrl =
				process.env.NEXT_PUBLIC_TOOL_API_URL || "http://10.11.1.207:8011";
			const url = region
				? `${apiUrl}/api/data/parent?region=${encodeURIComponent(region)}`
				: `${apiUrl}/api/data/parent`;

			const response = await fetch(url);
			const result: ApiResponse = await response.json();

			if (result.success && result.data) {
				// Set all location levels from API response
				setNasional(result.data.nasional || null);
				setProvinsi(result.data.provinsi || null);
				setKabupaten(result.data.kabupaten || null);
				setKota(result.data.kota || null);
				setKecamatan(result.data.kecamatan || null);
				setParentLocation(result.data.parent);
			}
		} catch (error) {
			console.error("Error fetching parent data:", error);
			// Keep default values if API fails
			setNasional("Indonesia");
			setProvinsi(null);
			setKabupaten(null);
			setKota(null);
			setKecamatan(null);
			setParentLocation(null);
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		fetchParentData();
	}, [region]);
	// Get current location (most specific level available)
	const getCurrentLocation = () => {
		return (
			kecamatan || kota || kabupaten || provinsi || nasional || "Indonesia"
		);
	};

	// Get breadcrumb hierarchy
	const getBreadcrumb = () => {
		const breadcrumb = [];
		if (nasional) breadcrumb.push({ level: "nasional", name: nasional });
		if (provinsi) breadcrumb.push({ level: "provinsi", name: provinsi });
		if (kabupaten) breadcrumb.push({ level: "kabupaten", name: kabupaten });
		if (kota) breadcrumb.push({ level: "kota", name: kota });
		if (kecamatan) breadcrumb.push({ level: "kecamatan", name: kecamatan });
		return breadcrumb;
	};

	return (
		<main>
			<div className="flex space-x-2 items-center">
				{isLoading ? (
					<div className="bg-tea-green-600/80 p-1 rounded-lg px-4 text-green-700">
						<div className="flex items-center space-x-2">
							<div className="animate-pulse bg-green-600 rounded w-16 h-4"></div>
						</div>
					</div>
				) : (
					<>
						{getBreadcrumb().map((item, index) => (
							<div key={item.level} className="flex items-center space-x-2">
								{index > 0 && <span className="text-gray-400 text-xs">→</span>}
								<div
									className={`p-1 rounded-lg px-3 text-sm ${
										index === getBreadcrumb().length - 1
											? "bg-tea-green-600/80 text-green-700 font-medium"
											: "bg-gray-200/80 text-gray-600"
									}`}
								>
									{item.name}
								</div>
							</div>
						))}
					</>
				)}
			</div>
		</main>
	);
}

export default State;
